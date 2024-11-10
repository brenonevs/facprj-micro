import pyaudio
import numpy as np
import time
import sounddevice as sd

# Configurações de áudio
RATE = 44100          # Taxa de amostragem
CHUNK = 1024          # Tamanho do buffer

# Frequências aproximadas para notas musicais no formato dó, ré, mi...
NOTE_FREQUENCIES = {
    "dó": 261.63, "dó#": 277.18, "ré": 293.66, "ré#": 311.13, "mi": 329.63,
    "fá": 349.23, "fá#": 369.99, "sol": 392.00, "sol#": 415.30, "lá": 440.00,
    "lá#": 466.16, "si": 493.88
}

# Função para encontrar a nota mais próxima
def closest_note(frequency):
    note = min(NOTE_FREQUENCIES, key=lambda k: abs(NOTE_FREQUENCIES[k] - frequency))
    return note

# Função para sintetizar som de uma nota
def play_note(frequency, duration=0.5):
    t = np.linspace(0, duration, int(RATE * duration), endpoint=False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    sd.play(wave, samplerate=RATE)
    sd.wait()

# Inicializando o PyAudio para captura
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)

print("Gravação de melodia iniciada. Pressione 'Enter' para gravar cada nota individualmente.")

melody = []  # Lista para salvar as notas e seus tempos

try:
    while True:
        input("Pressione 'Enter' para gravar a próxima nota ou Ctrl+C para finalizar...")
        
        # Captura de áudio para uma única nota
        print("Gravando... Fale uma nota.")
        data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
        
        # Aplicação da FFT
        fft = np.fft.fft(data)
        freqs = np.fft.fftfreq(len(fft))
        
        # Identificação da frequência dominante
        peak_idx = np.argmax(np.abs(fft))
        peak_freq = abs(freqs[peak_idx] * RATE)
        
        # Identificação da nota musical mais próxima no formato dó, ré, mi...
        note = closest_note(peak_freq)
        print(f"Frequência: {peak_freq:.2f} Hz - Nota detectada: {note}")
        
        # Armazena a nota e o tempo de captura
        melody.append((note, time.time()))
        print("Nota gravada.")

except KeyboardInterrupt:
    print("Gravação encerrada.")

# Processamento para determinar intervalos de tempo entre as notas
if len(melody) > 1:
    melody_sequence = []
    for i in range(1, len(melody)):
        note, timestamp = melody[i]
        prev_note, prev_timestamp = melody[i - 1]
        duration = timestamp - prev_timestamp
        melody_sequence.append((prev_note, duration))
    melody_sequence.append((melody[-1][0], 0.5))  # Última nota com duração padrão

    # Reproduz a melodia gravada
    print("Reproduzindo a melodia...")
    for note, duration in melody_sequence:
        play_note(NOTE_FREQUENCIES[note], duration)
        time.sleep(duration)
else:
    print("Nenhuma melodia foi detectada.")

# Finalizando o stream de áudio
stream.stop_stream()
stream.close()
p.terminate()

