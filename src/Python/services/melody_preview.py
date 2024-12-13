# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

import numpy as np
import sounddevice as sd
import json
import time

class MelodyPreview:
    def __init__(self):
        self.sample_rate = 44100
    
    def preview_melody(self, dados_melodia):
        """Reproduz uma sequência de notas."""
        
        for nota in dados_melodia:
            frequencia, nome_nota, duracao = nota
            print(f"Tocando nota {nome_nota} (freq: {frequencia:.2f}Hz) por {duracao:.2f}s")
            self.preview_note(frequencia, duracao)
            time.sleep(0.1)  # Pequena pausa entre notas

    def preview_note(self, frequency, duration):
        """Reproduz uma nota com a frequência e duração especificadas."""
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        note = np.sin(2 * np.pi * frequency * t)
        
        # Aplica um envelope ADSR simples para suavizar o som
        envelope = np.ones_like(note)
        attack = int(0.1 * len(note))
        decay = int(0.1 * len(note))
        envelope[:attack] = np.linspace(0, 1, attack)
        envelope[-decay:] = np.linspace(1, 0, decay)
        
        # Aplica o envelope e normaliza
        note = note * envelope * 0.5
        
        # Reproduz a nota
        sd.play(note, self.sample_rate)
        sd.wait()  # Espera a nota terminar de tocar