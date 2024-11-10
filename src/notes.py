import pyaudio
import numpy as np

# Configurações de áudio
RATE = 44100          # Taxa de amostragem
CHUNK = 1024          # Tamanho do buffer

# Tabela de frequências para notas musicais
NOTE_FREQUENCIES = {
    "C": 261.63, "C#": 277.18, "D": 293.66, "D#": 311.13, "E": 329.63, 
    "F": 349.23, "F#": 369.99, "G": 392.00, "G#": 415.30, "A": 440.00, 
    "A#": 466.16, "B": 493.88
}

def closest_note(frequency):
    """Encontra a nota mais próxima para a frequência dada"""
    note = min(NOTE_FREQUENCIES, key=lambda k: abs(NOTE_FREQUENCIES[k] - frequency))
    return note

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)

print("Iniciando a detecção de notas musicais. Pressione Ctrl+C para interromper.")

try:
    while True:
        # Lendo os dados do microfone
        data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
        
        # Aplicando FFT para análise de frequência
        fft = np.fft.fft(data)
        freqs = np.fft.fftfreq(len(fft))

        # Encontrando a frequência dominante
        peak_idx = np.argmax(np.abs(fft))
        peak_freq = abs(freqs[peak_idx] * RATE)

        # Identificando a nota musical mais próxima
        note = closest_note(peak_freq)
        print(f"Frequência detectada: {peak_freq:.2f} Hz - Nota aproximada: {note}")

except KeyboardInterrupt:
    print("Detecção encerrada.")

# Finalizando o stream de áudio
stream.stop_stream()
stream.close()
p.terminate()
