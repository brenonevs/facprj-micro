import pyaudio
import numpy as np
import sounddevice as sd

# Configurações de áudio globais
RATE = 44100          # Taxa de amostragem
CHUNK = 1024          # Tamanho do buffer
FIXED_DURATION = 0.5  # Duração fixa para reprodução de cada nota

# Frequências para várias oitavas no formato dó, ré, mi...
NOTE_FREQUENCIES = {
    "dó": [261.63, 523.25, 1046.5], "dó#": [277.18, 554.37, 1108.73],
    "ré": [293.66, 587.33, 1174.66], "ré#": [311.13, 622.25, 1244.51],
    "mi": [329.63, 659.26, 1318.51], "fá": [349.23, 698.46, 1396.91],
    "fá#": [369.99, 739.99, 1479.98], "sol": [392.00, 783.99, 1567.98],
    "sol#": [415.30, 830.61, 1661.22], "lá": [440.00, 880.00, 1760.00],
    "lá#": [466.16, 932.33, 1864.66], "si": [493.88, 987.77, 1975.53]
}

class NoteRecognizer:
    """Captura e identifica notas musicais a partir de áudio.

    Esta classe captura áudio usando PyAudio, aplica uma transformada rápida de Fourier (FFT) para determinar
    a frequência dominante e identifica a nota musical correspondente.

    Attributes:
        p (pyaudio.PyAudio): Instância do PyAudio.
        stream (pyaudio.Stream): Stream de entrada para captura de áudio.
    """

    def __init__(self):
        """Inicializa o reconhecedor de notas e configura o stream de áudio."""
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)

    def capture_frequency(self):
        """Captura a frequência dominante do áudio.

        Lê dados de áudio, aplica FFT e retorna a frequência dominante.

        Returns:
            float: A frequência dominante em Hertz (Hz).
        """
        data = np.frombuffer(self.stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
        fft = np.fft.fft(data)
        freqs = np.fft.fftfreq(len(fft))
        peak_idx = np.argmax(np.abs(fft))
        peak_freq = abs(freqs[peak_idx] * RATE)
        return peak_freq

    def closest_note(self, frequency):
        """Encontra a nota musical mais próxima para uma frequência dada.

        Args:
            frequency (float): A frequência em Hertz.

        Returns:
            str: A nota musical mais próxima.
        """
        closest_note, min_diff = None, float("inf")
        for note, freqs in NOTE_FREQUENCIES.items():
            for freq in freqs:
                diff = abs(freq - frequency)
                if diff < min_diff:
                    min_diff, closest_note = diff, note
        return closest_note

    def get_note_from_frequency(self):
        """Obtém a nota musical a partir da frequência dominante.

        Returns:
            tuple: Uma tupla contendo a frequência e a nota identificada.
        """
        frequency = self.capture_frequency()
        note = self.closest_note(frequency)
        return frequency, note

    def close(self):
        """Fecha o stream de áudio e libera os recursos."""
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

class MelodyRecorder:
    """Gerencia a gravação de uma sequência de notas.

    Esta classe usa o `NoteRecognizer` para capturar e identificar notas e armazena a sequência.

    Attributes:
        recognizer (NoteRecognizer): Instância do reconhecedor de notas.
        melody (list): Lista de notas capturadas.
    """

    def __init__(self, recognizer):
        """Inicializa o gravador de melodia.

        Args:
            recognizer (NoteRecognizer): Instância do reconhecedor de notas.
        """
        self.recognizer = recognizer
        self.melody = []

    def record_melody(self):
        """Inicia a gravação de uma sequência de notas, capturando uma nota por vez até a interrupção do usuário."""
        print("Inicie a gravação. Pressione 'Enter' para gravar cada nota.")
        try:
            while True:
                input("Pressione 'Enter' para gravar a próxima nota ou Ctrl+C para finalizar...")
                frequency, note = self.recognizer.get_note_from_frequency()
                self.melody.append((frequency, note))
                print(f"Frequência: {frequency:.2f} Hz - Nota gravada: {note}")
        except KeyboardInterrupt:
            print("Gravação encerrada.")

    def get_melody(self):
        """Retorna a sequência de notas gravadas.

        Returns:
            list: Lista de tuplas contendo a frequência e a nota capturadas.
        """
        return self.melody

    def save_melody_to_file(self, filename="melody.txt"):
        """Salva a sequência de notas em um arquivo .txt.

        Args:
            filename (str): Nome do arquivo onde a melodia será salva.
        """
        with open(filename, 'w', encoding='utf-8') as file:
            for frequency, note in self.melody:
                file.write(f"Frequência: {frequency:.2f} Hz - Nota: {note}\n")
        print(f"Melodia salva em {filename}")

class MelodyPlayer:
    """Reproduz uma sequência de notas em uma melodia.

    A classe sintetiza e reproduz cada nota usando sounddevice.

    Methods:
        play_note: Toca uma única nota com a frequência e duração especificadas.
        play_melody: Reproduz a sequência de notas em uma melodia.
    """

    def play_note(self, frequency, duration=FIXED_DURATION):
        """Toca uma única nota sintetizada.

        Args:
            frequency (float): A frequência da nota em Hertz (Hz).
            duration (float): A duração da nota em segundos.
        """
        t = np.linspace(0, duration, int(RATE * duration), endpoint=False)
        wave = 0.5 * np.sin(2 * np.pi * frequency * t)
        sd.play(wave, samplerate=RATE)
        sd.wait()

    def play_melody(self, melody):
        """Reproduz uma sequência de notas com duração fixa.

        Args:
            melody (list): Lista de tuplas contendo frequência e nota para reprodução.
        """
        print("Reproduzindo a melodia...")
        for frequency, note in melody:
            print(f"Tocando: Nota {note} com frequência {frequency:.2f} Hz")
            self.play_note(frequency)

class AudioProcessor:
    """Gerencia o processo de gravação e reprodução de melodia.

    Esta classe coordena o `NoteRecognizer`, `MelodyRecorder`, e `MelodyPlayer` para capturar, armazenar e reproduzir uma melodia.

    Attributes:
        recognizer (NoteRecognizer): Instância do reconhecedor de notas.
        recorder (MelodyRecorder): Instância do gravador de melodia.
        player (MelodyPlayer): Instância do reprodutor de melodia.
    """

    def __init__(self):
        """Inicializa o processador de áudio e configura os componentes de gravação e reprodução."""
        self.recognizer = NoteRecognizer()
        self.recorder = MelodyRecorder(self.recognizer)
        self.player = MelodyPlayer()

    def run(self):
        """Executa o processo de gravação e reprodução da melodia."""
        self.recorder.record_melody()
        
        melody = self.recorder.get_melody()
        if melody:
            self.recorder.save_melody_to_file()  # Salva a melodia em um arquivo .txt
            self.player.play_melody(melody)
        else:
            print("Nenhuma melodia foi detectada.")
        
        self.recognizer.close()

if __name__ == "__main__":
    processor = AudioProcessor()
    processor.run()
