import customtkinter as ctk
from tkinter import messagebox
from controller.audio_recorder import MelodyRecorder, MelodyPlayer
from controller.note_recognizer import NoteRecognizer
import threading


class AudioApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gravador de Melodias")
        self.geometry("600x370")
        
        # Configuração do tema
        ctk.set_appearance_mode("dark")  # Tema escuro
        ctk.set_default_color_theme("blue")  # Tema azul
        
        # Inicializa componentes
        self.recognizer = NoteRecognizer()
        self.recorder = MelodyRecorder(self.recognizer)
        self.player = MelodyPlayer()
        
        # Título
        self.title_label = ctk.CTkLabel(
            self,
            text="🎵 Gravador de Melodias 🎶",
            font=("Arial", 26, "bold"),
            fg_color="#1a1a1a",
            text_color="#00ace6",
            corner_radius=10,
            pady=10,
        )
        self.title_label.pack(pady=20, padx=10, fill="x")
        
        # Frame principal para os botões
        self.main_buttons_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_buttons_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Botão de gravação
        self.record_button = ctk.CTkButton(
            self.main_buttons_frame,
            text="🎤 Iniciar Gravação",
            font=("Arial", 16),
            command=self.handle_recording,
            corner_radius=10,
            fg_color="#00cc66",
            hover_color="#00994d",
            height=40,
            text_color="#ffffff"  
        )
        self.record_button.pack(pady=15, padx=10)
        
        # Label para mostrar a nota
        self.note_label = ctk.CTkLabel(
            self.main_buttons_frame,
            text="Frequência e Nota Capturada:",
            font=("Arial", 14),
            text_color="#ffffff",
            anchor="w",
            corner_radius=8,
            fg_color="#333333",
            padx=10,
            pady=5,
        )
        self.note_label.pack(pady=10, padx=10, fill="x")
        
        # Frame para botões secundários
        self.secondary_buttons_frame = ctk.CTkFrame(self.main_buttons_frame, corner_radius=15)
        self.secondary_buttons_frame.pack(pady=15, padx=10, fill="x")
        
        # Botão de reprodução
        self.play_button = ctk.CTkButton(
            self.secondary_buttons_frame,
            text="▶ Reproduzir",
            font=("Arial", 14),
            command=self.start_playing_thread,
            corner_radius=10,
            fg_color="#1e90ff",
            hover_color="#005cbf",
            state="disabled",
            height=35,
            text_color="#ffffff"  
        )
        self.play_button.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        
        # Botão de salvar
        self.save_button = ctk.CTkButton(
            self.secondary_buttons_frame,
            text="💾 Salvar",
            font=("Arial", 14),
            command=self.save_melody,
            corner_radius=10,
            fg_color="#ffcc00",
            hover_color="#e6b800",
            state="disabled",
            height=35,
            text_color="#ffffff"  
        )
        self.save_button.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        
        # Botão de limpar
        self.clear_button = ctk.CTkButton(
            self.secondary_buttons_frame,
            text="🧹 Limpar",
            font=("Arial", 14),
            command=self.clear_melody,
            corner_radius=10,
            fg_color="#ff6666",
            hover_color="#e63939",
            height=35,
            text_color="#ffffff"  
        )
        self.clear_button.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        
        # Configurações da janela
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.resizable(False, False)
    
    def on_closing(self):
        """Fecha a aplicação e libera recursos."""
        self.recognizer.close()
        self.destroy()

    def handle_recording(self):
        """Gerencia o início e fim da gravação."""
        frequency, note, duration, is_starting = self.recorder.start_stop_recording()
        
        if is_starting:
            # Começou a gravar
            self.record_button.configure(text="⏹ Parar Gravação", fg_color="#cc0000", hover_color="#990000")
            self.note_label.configure(text="🎤 Gravando...")
            self.play_button.configure(state="disabled")
            self.save_button.configure(state="disabled")
        else:
            # Parou de gravar
            self.record_button.configure(text="🎤 Iniciar Gravação", fg_color="#00cc66", hover_color="#00994d")
            self.note_label.configure(
                text=f"Frequência: {frequency:.2f} Hz - Nota: {note} - Duração: {duration:.2f}s"
            )
            self.play_button.configure(state="normal")
            self.save_button.configure(state="normal")

    def start_playing_thread(self):
        """Inicia uma nova thread para reproduzir a melodia sem travar a interface."""
        threading.Thread(target=self.play_melody, daemon=True).start()

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