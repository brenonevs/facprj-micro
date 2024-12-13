import sounddevice as sd
import numpy as np
import time
import json
from .note_recognizer import NoteRecognizer

FIXED_DURATION = 0.5  

class MelodyRecorder:
    def __init__(self, recognizer):
        self.recognizer = recognizer
        self.melody = []
        self.is_recording = False
        self.start_time = None
        self.recorded_samples = []  # Para armazenar as amostras durante a gravação

    def start_stop_recording(self):
        """Inicia ou para a gravação e retorna os resultados."""
        if not self.is_recording:
            # Inicia gravação
            self.is_recording = True
            self.start_time = time.time()
            self.recorded_samples = []
            return None, None, 0, True  # O último True indica que começou a gravar
        else:
            # Para gravação
            self.is_recording = False
            duration = time.time() - self.start_time
            frequency, note = self.recognizer.get_note_from_frequency()
            self.melody.append((frequency, note, duration))
            return frequency, note, duration, False  # O False indica que parou de gravar

    def record_note(self):
        """Captura e grava uma única nota com sua frequência.

        Returns:
            tuple: Frequência e nota identificada.
        """
        frequency, note = self.recognizer.get_note_from_frequency()
        self.melody.append((frequency, note))
        return frequency, note

    def save_melody_to_file(self, filename="melodies.json"):
        """Salva a sequência de notas em um arquivo .json com identificadores de melodia."""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                melodies = json.load(file)
        except FileNotFoundError:
            melodies = {}

        # Determina o próximo identificador de melodia
        melody_id = f"melodia {len(melodies) + 1}"

        # Adiciona a nova melodia ao dicionário de melodias
        melodies[melody_id] = self.melody

        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(melodies, file, ensure_ascii=False, indent=4)
        
        return filename

    def clear_melody(self):
        """Limpa a melodia atual e remove do arquivo JSON."""
        self.melody.clear()

        try:
            with open("melodies.json", 'r', encoding='utf-8') as file:
                melodies = json.load(file)
        except FileNotFoundError:
            melodies = {}

        # Determina o identificador da última melodia
        if melodies:
            last_melody_id = f"melodia {len(melodies)}"
            if last_melody_id in melodies:
                del melodies[last_melody_id]

        with open("melodies.json", 'w', encoding='utf-8') as file:
            json.dump(melodies, file, ensure_ascii=False, indent=4)

class MelodyPlayer:
    def __init__(self):
        self.sample_rate = 44100  # Adiciona o sample_rate no init

    def play_note(self, frequency, duration):
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

    def play_melody(self, melody_id, filename="melodies.json"):
        """Reproduz uma sequência de notas identificada por melody_id."""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                melodies = json.load(file)
        except FileNotFoundError:
            print("Arquivo de melodias não encontrado.")
            return

        melody = melodies.get(melody_id)
        if not melody:
            print(f"Melodia {melody_id} não encontrada.")
            return

        for frequency, note, duration in melody:
            self.play_note(frequency, duration)
            time.sleep(0.1)  # Pequena pausa entre notas
