import json
import time
import customtkinter as ctk
from controller.note_recognizer import NoteRecognizer
from controller.audio_recorder import MelodyRecorder

class GameInterface:
    def __init__(self, selected_melody, difficulty, melodies_file):
        self.selected_melody = selected_melody
        self.difficulty = difficulty
        self.melodies_file = melodies_file
        self.current_note_index = 0
        self.melody_data = None
        
        # Inicializa o reconhecedor de notas e o gravador
        self.note_recognizer = NoteRecognizer()
        self.melody_recorder = MelodyRecorder(self.note_recognizer)
        
        self.load_melody()
        self.setup_window()
        self.is_recording = False
        self.correct_note_time = 0
        self.time_required = 1.0  # Tempo em segundos que precisa manter a nota correta
        self.is_note_correct = False

        # Ajustar tolerância e tempo baseado na dificuldade
        if difficulty == 1:
            self.frequency_tolerance = 130  # Hz
            self.time_required = 0.8      # segundos
        elif difficulty == 2:
            self.frequency_tolerance = 80  # Hz
            self.time_required = 1.0      # segundos
        else: 
            self.frequency_tolerance = 60  # Hz
            self.time_required = 1.2      # segundos

    def load_melody(self):
        with open(self.melodies_file, 'r', encoding='utf-8') as f:
            melodies = json.load(f)
            self.melody_name = list(melodies.keys())[self.selected_melody]
            self.melody_data = melodies[self.melody_name]

    def setup_window(self):
        self.window = ctk.CTk()
        self.window.title("Jogo de Melodias")
        self.window.geometry("800x600")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Título
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Jogo de Melodias",
            font=("Roboto", 24, "bold")
        )
        self.title_label.pack(pady=10)

        # Informações da melodia
        self.melody_info = ctk.CTkLabel(
            self.main_frame,
            text=f"Melodia: {self.melody_name}\nDificuldade: {self.difficulty}",
            font=("Roboto", 16)
        )
        self.melody_info.pack(pady=10)

        # Frame para frequências
        self.freq_frame = ctk.CTkFrame(self.main_frame)
        self.freq_frame.pack(pady=10, fill="x", padx=20)

        self.expected_freq_label = ctk.CTkLabel(
            self.freq_frame,
            text="Frequência esperada: -",
            font=("Roboto", 14)
        )
        self.expected_freq_label.pack(pady=5)

        self.current_freq_label = ctk.CTkLabel(
            self.freq_frame,
            text="Sua frequência: -",
            font=("Roboto", 14)
        )
        self.current_freq_label.pack(pady=5)

        # Nota atual
        self.note_label = ctk.CTkLabel(
            self.main_frame,
            text="Prepare-se!",
            font=("Roboto", 32, "bold")
        )
        self.note_label.pack(pady=20)

        # Botão de gravação
        self.record_button = ctk.CTkButton(
            self.main_frame,
            text="Iniciar Gravação",
            command=self.start_recording,
            font=("Roboto", 16),
            height=40
        )
        self.record_button.pack(pady=20)

        # Status
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="Clique em 'Iniciar Gravação' para começar",
            font=("Roboto", 14)
        )
        self.status_label.pack(pady=10)

        # Após criar todos os widgets, adicione:
        # Inicializa a primeira nota e frequência
        first_note = self.melody_data[0]
        self.note_label.configure(text=f"Nota: {first_note[1]}")
        self.expected_freq_label.configure(text=f"Frequência esperada: {first_note[0]:.2f} Hz")

    def start_recording(self):
        if not self.is_recording:
            self.is_recording = True
            self.record_button.configure(text="Parar Gravação")
            self.status_label.configure(
                text=f"Gravando... (Tolerância: ±{self.frequency_tolerance}Hz)"
            )
            self.update_frequency()
        else:
            self.is_recording = False
            self.record_button.configure(text="Iniciar Gravação")
            self.status_label.configure(text="Gravação parada")
            self.is_note_correct = False
            self.correct_note_time = 0

    def update_frequency(self):
        if self.is_recording:
            frequency, note = self.melody_recorder.recognizer.get_note_from_frequency()
            self.current_freq_label.configure(text=f"Sua frequência: {frequency:.2f} Hz")
            
            current_note = self.melody_data[self.current_note_index]
            expected_freq = current_note[0]
            
            if abs(frequency - expected_freq) <= self.frequency_tolerance:
                if not self.is_note_correct:
                    self.is_note_correct = True
                    self.correct_note_time = time.time()
                
                if time.time() - self.correct_note_time >= self.time_required:
                    self.process_recording()
                    self.is_note_correct = False
                    return
                
                progress = (time.time() - self.correct_note_time) / self.time_required * 100
                self.status_label.configure(
                    text=f"Mantenha a nota! {progress:.0f}% (±{self.frequency_tolerance}Hz)"
                )
            else:
                self.is_note_correct = False
                self.correct_note_time = 0
                self.status_label.configure(
                    text=f"Tente chegar mais perto da frequência esperada (±{self.frequency_tolerance}Hz)"
                )
            
            self.window.after(100, self.update_frequency)

    def process_recording(self):
        if self.is_note_correct:
            current_note = self.melody_data[self.current_note_index]
            self.status_label.configure(text=f"Parabéns! Você acertou a nota: {current_note[1]}")
            
            self.current_note_index += 1
            if self.current_note_index >= len(self.melody_data):
                self.finish_game()
            else:
                # Prepara para a próxima nota
                next_note = self.melody_data[self.current_note_index]
                self.note_label.configure(text=f"Próxima nota: {next_note[1]}")
                self.expected_freq_label.configure(text=f"Frequência esperada: {next_note[0]:.2f} Hz")
                self.current_freq_label.configure(text="Sua frequência: -")
                
                # Atualiza o texto do botão
                self.record_button.configure(text="Próxima Nota")

    def finish_game(self):
        self.status_label.configure(text="Jogo concluído!")
        self.record_button.configure(state="disabled")
        self.note_label.configure(text="Fim do jogo!")

    def start_game(self):
        self.window.mainloop()