import pyaudio
import numpy as np

RATE = 44100          # Taxa de amostragem
CHUNK = 1024          # Tamanho do buffer

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
