import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import time

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
        # Adiciona buffers para armazenar o histórico temporal
        self.time_points = []
        self.freq_history = []
        self.start_time = time.time()

    def capture_frequency(self):
        """Captura a frequência dominante do áudio.

        Lê dados de áudio, aplica FFT e retorna a frequência dominante média.

        Returns:
            float: A frequência dominante em Hertz (Hz).
        """
        # Captura várias amostras para ter uma média mais estável
        num_samples = 10
        frequencies = []
        
        for _ in range(num_samples):
            data = np.frombuffer(self.stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
            fft = np.fft.fft(data)
            freqs = np.fft.fftfreq(len(fft)) * RATE
            
            positive_freqs_mask = freqs >= 0
            magnitude = np.abs(fft)[positive_freqs_mask]
            freqs = freqs[positive_freqs_mask]
            
            peak_idx = np.argmax(magnitude)
            peak_freq = abs(freqs[peak_idx])
            
            if peak_freq > 50:
                frequencies.append(peak_freq)
        
        current_freq = np.mean(frequencies) if frequencies else 0.0
        
        # Adiciona o ponto temporal e a frequência aos históricos
        current_time = time.time() - self.start_time
        self.time_points.append(current_time)
        self.freq_history.append(current_freq)
        
        # Mantém apenas os últimos 5 segundos de dados
        cutoff_time = current_time - 5
        while self.time_points and self.time_points[0] < cutoff_time:
            self.time_points.pop(0)
            self.freq_history.pop(0)
            
        return current_freq

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

    def plot_spectrogram(self, data, detected_freq):
        """Plota o espectro de frequências do sinal de áudio ao longo do tempo.
        
        Args:
            data (numpy.ndarray): Dados do áudio capturado
            detected_freq (float): Frequência dominante detectada
        """
        plt.figure(figsize=(12, 6))
        
        # Subplot superior para o espectro de frequências atual
        plt.subplot(2, 1, 1)
        fft_data = np.fft.fft(data)
        freqs = np.fft.fftfreq(len(data)) * RATE
        magnitude = np.abs(fft_data)
        
        positive_freqs_mask = freqs >= 0
        plt.plot(freqs[positive_freqs_mask], magnitude[positive_freqs_mask])
        plt.axvline(x=detected_freq, color='r', linestyle='--', 
                   label=f'Frequência atual: {detected_freq:.2f} Hz')
        plt.xlabel('Frequência [Hz]')
        plt.ylabel('Magnitude')
        plt.title('Espectro de Frequências (Atual)')
        plt.grid(True)
        plt.legend()
        plt.xlim(0, 2000)
        
        # Subplot inferior para o histórico temporal
        plt.subplot(2, 1, 2)
        plt.plot(self.time_points, self.freq_history, '-b', label='Histórico de frequências')
        plt.axhline(y=detected_freq, color='r', linestyle='--')
        plt.xlabel('Tempo [s]')
        plt.ylabel('Frequência [Hz]')
        plt.title('Histórico de Frequências Detectadas')
        plt.grid(True)
        plt.ylim(0, 2000)
        
        plt.tight_layout()
        plt.draw()
        plt.pause(0.1)
        plt.clf()

    def get_note_from_frequency(self):
        """Obtém a nota musical a partir da frequência dominante e plota o espectrograma.

        Returns:
            tuple: Uma tupla contendo a frequência e a nota identificada.
        """
        data = np.frombuffer(self.stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
        frequency = self.capture_frequency()
        note = self.closest_note(frequency)
        
        # Passa a frequência detectada para o plot
        self.plot_spectrogram(data, frequency)
        
        return frequency, note

    def close(self):
        """Fecha o stream de áudio e libera os recursos."""
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
