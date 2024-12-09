import customtkinter as ctk
from tkinter import messagebox
from controller.audio_recorder import MelodyRecorder, MelodyPlayer
from controller.note_recognizer import NoteRecognizer
import threading
import json


class AudioApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gravador de Melodias")
        self.geometry("600x450")
        
        # Configuração do tema
        ctk.set_appearance_mode("dark")  # Tema escuro
        ctk.set_default_color_theme("blue")  # Tema azul
        
        # Lista para armazenar IDs de eventos after
        self._after_ids = []

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
        
        # Botão de gravar nova melodia (inicialmente escondido)
        self.new_recording_button = ctk.CTkButton(
            self.main_buttons_frame,
            text="🎵 Gravar Nova Melodia",
            font=("Arial", 14),
            command=self.start_new_recording,
            corner_radius=10,
            fg_color="#ff9900",
            hover_color="#e68a00",
            state="disabled",  # Inicialmente desativado
            height=35,
            text_color="#ffffff"
        )
        self.new_recording_button.pack(pady=5, padx=10, fill="x")

        # Botão de fechar aplicativo
        self.close_button = ctk.CTkButton(
            self.main_buttons_frame,
            text="❌ Fechar Aplicativo",
            font=("Arial", 14),
            command=self.on_closing,
            corner_radius=10,
            fg_color="#cc0000",
            hover_color="#990000",
            height=35,
            text_color="#ffffff"
        )
        self.close_button.pack(pady=5, padx=10, fill="x")

        # Configurações da janela
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.resizable(False, False)
    
    def on_closing(self):
        """Fecha apenas a interface gráfica, mantendo o programa em execução."""
        try:
            # Primeiro, desativa todos os botões e eventos
            for widget in self.winfo_children():
                try:
                    if hasattr(widget, 'configure'):
                        widget.configure(state="disabled")
                    if hasattr(widget, 'unbind_all'):
                        widget.unbind_all()
                except Exception:
                    pass

            # Libera recursos do recognizer
            if hasattr(self.recognizer, 'close'):
                try:
                    self.recognizer.close()
                except Exception as e:
                    print(f"Erro ao fechar recognizer: {e}")
            
            # Encerra threads relacionadas à interface
            self._stop_threads()

            # Remove todos os widgets filhos primeiro
            for widget in self.winfo_children():
                try:
                    widget.pack_forget()
                except Exception:
                    pass

            # Destrói apenas a janela
            try:
                self.withdraw()  # Esconde a janela
                self.after(100, self.destroy)  # Agenda a destruição da janela
            except Exception as e:
                print(f"Erro ao destruir janela: {e}")

        except Exception as e:
            print(f"Erro durante fechamento: {e}")

    def _stop_threads(self):
        """Encerra threads em execução."""
        for thread in threading.enumerate():
            if thread.is_alive() and thread != threading.main_thread():
                try:
                    thread.join(timeout=1)
                except RuntimeError:
                    pass

    def handle_recording(self):
        """Gerencia o início e fim da gravação."""
        frequency, note, duration, is_starting = self.recorder.start_stop_recording()
        
        if is_starting:
            # Começou a gravar
            self.record_button.configure(text="⏹ Parar Gravação", fg_color="#cc0000", hover_color="#990000")
            self.note_label.configure(text="🎤 Gravando...")
            self.play_button.configure(state="disabled")
            self.save_button.configure(state="disabled")
            self.new_recording_button.configure(state="disabled")
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
        try:
            with open("melodies.json", 'r', encoding='utf-8') as file:
                melodies = json.load(file)
            last_melody_id = f"melodia {len(melodies)}"
            self.player.play_melody(last_melody_id)
        except FileNotFoundError:
            messagebox.showerror("Erro", "Arquivo de melodias não encontrado.")
        except KeyError:
            messagebox.showerror("Erro", "Nenhuma melodia encontrada para reprodução.")

    def save_melody(self):
        """Salva a sequência de notas em um arquivo e exibe uma mensagem de confirmação."""
        filename = self.recorder.save_melody_to_file()
        messagebox.showinfo("Melodia Salva", f"Melodia salva em {filename}")
        self.new_recording_button.configure(state="normal")
        self.record_button.configure(state="disabled")

    def clear_melody(self):
        """Limpa a sequência de notas gravadas e atualiza a interface."""
        self.recorder.clear_melody()
        self.note_label.configure(text="Frequência e Nota Capturada:")
        self.play_button.configure(state="disabled")
        self.save_button.configure(state="disabled")
        messagebox.showinfo("Melodia Limpa", "A melodia foi limpa.")

    def start_new_recording(self):
        """Prepara a interface para iniciar uma nova gravação, sem apagar melodias anteriores."""
        try:
            # Lê o arquivo existente
            with open("melodies.json", 'r', encoding='utf-8') as file:
                melodies = json.load(file)
        except FileNotFoundError:
            # Se o arquivo não existir, cria um dicionário vazio
            melodies = {}
        
        # Define o próximo ID da melodia
        next_melody_number = len(melodies) + 1
        next_melody_id = f"melodia {next_melody_number}"
        
        # Adiciona apenas a nova entrada no JSON, mantendo as existentes
        with open("melodies.json", 'w', encoding='utf-8') as file:
            melodies[next_melody_id] = []  # Inicializa a nova melodia como uma lista vazia
            json.dump(melodies, file, ensure_ascii=False, indent=4)

        # Prepara a interface para a nova gravação
        self.recorder.clear_melody()  # Limpa apenas a gravação atual em memória
        self.note_label.configure(text="Frequência e Nota Capturada:")
        self.play_button.configure(state="disabled")
        self.save_button.configure(state="disabled")
        self.new_recording_button.configure(state="disabled")
        self.record_button.configure(state="normal")  # Ativa o botão de gravação novamente
        self.record_button.configure(
            text="🎤 Iniciar Gravação", fg_color="#00cc66", hover_color="#00994d"
        )
        messagebox.showinfo("Nova Gravação", f"Pronto para gravar {next_melody_id}.")
