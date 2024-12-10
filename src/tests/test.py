# Read in a WAV and find the freq's
import pyaudio
import wave
import numpy as np

chunk = 2048

# Definir taxa de amostragem para microfone
RATE = 44100  # Taxa de amostragem padrão

# use a Blackman window
window = np.blackman(chunk)
# open stream
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,  # Formato de áudio do microfone
                channels=1,  # Normalmente, o microfone é mono
                rate=RATE,
                input=True,  # Define como entrada
                frames_per_buffer=chunk)

# Adicione estas constantes no início do arquivo
NUM_HARMONICOS = 4  # Número de harmônicos a considerar
MIN_FREQ = 60
MAX_FREQ = 300  # Limite para frequência fundamental

try:
    while True:
        try:
            # Lê dados do microfone
            data = stream.read(chunk, exception_on_overflow=False)
        except IOError as e:
            print(f"Erro de E/S: {e}")
            continue
        # Converte os dados para um array numpy
        data_np = np.frombuffer(data, dtype=np.int16)  # Altera para int16 para dados de microfone
        
        # Aplica a janela de Blackman
        data_np = data_np * window
        
        # Calcula a FFT
        fft_data = abs(np.fft.rfft(data_np))**2
        
        # Encontra os picos mais significativos
        picos = []
        threshold = np.max(fft_data) * 0.1  # 10% do valor máximo

        for i in range(1, len(fft_data)-1):
            if fft_data[i] > threshold and fft_data[i] > fft_data[i-1] and fft_data[i] > fft_data[i+1]:
                freq = i * RATE/chunk
                if MIN_FREQ <= freq <= 2000:  # Ainda mantemos um filtro amplo
                    picos.append((freq, fft_data[i]))

        # Ordena os picos por amplitude
        picos.sort(key=lambda x: x[1], reverse=True)

        if picos:
            # Analisa os primeiros picos para encontrar harmônicos
            freq_fundamental = picos[0][0]
            for pico in picos[1:min(len(picos), NUM_HARMONICOS)]:
                # Verifica se este pico pode ser a frequência fundamental
                freq_atual = pico[0]
                for n in range(2, NUM_HARMONICOS + 1):
                    if abs(picos[0][0] / n - freq_atual) < 10:  # Tolerância de 10 Hz
                        freq_fundamental = freq_atual
                        break
            
            if MIN_FREQ <= freq_fundamental <= MAX_FREQ:
                print(f"Frequência fundamental: {freq_fundamental:.1f} Hz")

except KeyboardInterrupt:
    print("\n* Gravação finalizada")

stream.close()
p.terminate()