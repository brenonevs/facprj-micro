# views/audio_app.py

import customtkinter as ctk
from tkinter import messagebox
from controller.audio_recorder import MelodyRecorder, MelodyPlayer
from controller.note_recognizer import NoteRecognizer
import threading

class AudioApp(ctk.CTk):
    """Interface gráfica do aplicativo de gravação e reprodução de melodia.

    Contém botões para capturar notas, reproduzir a melodia, salvar a melodia e limpar a gravação.

    Attributes:
        recognizer (NoteRecognizer): Instância para reconhecimento de notas.
        recorder (MelodyRecorder): Instância para gravação de melodia.
        player (MelodyPlayer): Instância para reprodução de melodia.
    """

    def __init__(self):
        """Inicializa a interface do aplicativo."""
        super().__init__()
        self.title("Gravador de Melodia")
        self.geometry("400x400")

        # Configurações de aparência
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Componentes de áudio
        self.recognizer = NoteRecognizer()
        self.recorder = MelodyRecorder(self.recognizer)
        self.player = MelodyPlayer()

        # Interface gráfica
        self.label = ctk.CTkLabel(self, text="Gravador de Melodia", font=("Arial", 16, "bold"))
        self.label.pack(pady=15)

        self.note_label = ctk.CTkLabel(self, text="Frequência e Nota Capturada:", font=("Arial", 12))
        self.note_label.pack(pady=10)

        self.record_button = ctk.CTkButton(self, text="Capturar Nota", command=self.start_recording_thread)
        self.record_button.pack(pady=10)

        self.play_button = ctk.CTkButton(self, text="Reproduzir Melodia", command=self.start_playing_thread, state="disabled")
        self.play_button.pack(pady=10)

        self.save_button = ctk.CTkButton(self, text="Salvar Melodia", command=self.save_melody, state="disabled")
        self.save_button.pack(pady=10)

        self.clear_button = ctk.CTkButton(self, text="Limpar Melodia", command=self.clear_melody)
        self.clear_button.pack(pady=10)

    def start_recording_thread(self):
        """Inicia uma nova thread para capturar uma nota sem travar a interface."""
        threading.Thread(target=self.record_note).start()

    def record_note(self):
        """Captura uma nota e exibe a frequência e nome da nota na interface."""
        frequency, note = self.recorder.record_note()
        self.note_label.configure(text=f"Frequência: {frequency:.2f} Hz - Nota: {note}")
        self.play_button.configure(state="normal")
        self.save_button.configure(state="normal")

    def start_playing_thread(self):
        """Inicia uma nova thread para reproduzir a melodia sem travar a interface."""
        threading.Thread(target=self.play_melody).start()

    def play_melody(self):
        """Reproduz a sequência de notas gravadas."""
        self.player.play_melody(self.recorder.melody)

    def save_melody(self):
        """Salva a sequência de notas em um arquivo e exibe uma mensagem de confirmação."""
        filename = self.recorder.save_melody_to_file()
        messagebox.showinfo("Melodia Salva", f"Melodia salva em {filename}")

    def clear_melody(self):
        """Limpa a sequência de notas gravadas e atualiza a interface."""
        self.recorder.clear_melody()
        self.note_label.configure(text="Frequência e Nota Capturada:")
        self.play_button.configure(state="disabled")
        self.save_button.configure(state="disabled")
        messagebox.showinfo("Melodia Limpa", "A melodia foi limpa.")
