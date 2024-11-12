import sounddevice as sd
import numpy as np
import time
from .note_recognizer import NoteRecognizer

FIXED_DURATION = 0.5  # Duração fixa para reprodução de cada nota

class MelodyRecorder:
    """Gerencia a gravação de uma sequência de notas.

    Usa o NoteRecognizer para capturar e identificar notas e armazena a sequência de notas.

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

    def record_note(self):
        """Captura e grava uma única nota com sua frequência.

        Returns:
            tuple: Frequência e nota identificada.
        """
        frequency, note = self.recognizer.get_note_from_frequency()
        self.melody.append((frequency, note))
        return frequency, note

    def save_melody_to_file(self, filename="melody.txt"):
        """Salva a sequência de notas em um arquivo .txt.

        Args:
            filename (str): Nome do arquivo onde a melodia será salva.

        Returns:
            str: Nome do arquivo salvo.
        """
        with open(filename, 'w', encoding='utf-8') as file:
            for frequency, note in self.melody:
                file.write(f"Frequência: {frequency:.2f} Hz - Nota: {note}\n")
        return filename

    def clear_melody(self):
        """Limpa a sequência de notas gravadas."""
        self.melody.clear()

class MelodyPlayer:
    """Reproduz uma sequência de notas em uma melodia.

    Métodos:
        play_note: Toca uma única nota com a frequência e duração especificadas.
        play_melody: Reproduz a sequência de notas em uma melodia.
    """

    def play_note(self, frequency, duration=FIXED_DURATION):
        """Toca uma única nota sintetizada.

        Args:
            frequency (float): A frequência da nota em Hertz (Hz).
            duration (float): A duração da nota em segundos.
        """
        t = np.linspace(0, duration, int(44100 * duration), endpoint=False)
        wave = 0.5 * np.sin(2 * np.pi * frequency * t)
        sd.play(wave, samplerate=44100)
        sd.wait()

    def play_melody(self, melody, interval=0.5):
        """Reproduz uma sequência de notas com um intervalo fixo entre cada nota.

        Args:
            melody (list): Lista de tuplas contendo frequência e nota para reprodução.
            interval (float): Tempo em segundos entre as notas.
        """
        for frequency, note in melody:
            self.play_note(frequency)
            time.sleep(interval)  # Pausa fixa entre as notas
