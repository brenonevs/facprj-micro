import pyaudio
import struct
import numpy as np
from time import sleep  

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

# Abrir stream do microfone
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* Gravando áudio do microfone...")

i = 0
try:
    while True:  # Loop infinito (pressione Ctrl+C para parar)
        sleep(2)
        i += 1
        data = stream.read(CHUNK)
        data_unpacked = struct.unpack('{n}h'.format(n=CHUNK), data)
        data_np = np.array(data_unpacked)
        data_fft = np.fft.fft(data_np)
        data_freq = np.abs(data_fft)/len(data_fft)
        print("Chunk: {} max_freq: {}".format(i, np.argmax(data_freq)))

except KeyboardInterrupt:
    print("* Gravação finalizada")

# Limpar recursos
stream.stop_stream()
stream.close()
p.terminate()