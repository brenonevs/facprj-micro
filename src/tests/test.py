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
        
        # Encontra a frequência dominante
        which = fft_data[1:].argmax() + 1
        
        if which != len(fft_data)-1:
            y0, y1, y2 = np.log(fft_data[which-1:which+2:])
            x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
            freq = (which + x1) * RATE/chunk
            if freq > 60 and freq < 2000:  # Filtra frequências fora da faixa vocal típica
                print(f"Frequência detectada: {freq:.1f} Hz")

except KeyboardInterrupt:
    print("\n* Gravação finalizada")

stream.close()
p.terminate()