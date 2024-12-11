import json
import time
import customtkinter as ctk
import controller.frequency_state
from controller.note_recognizer import NoteRecognizer
from controller.audio_recorder import MelodyRecorder

class GameInterface:
    def __init__(self, selected_melody, difficulty, melodies_file):
        self.selected_melody = selected_melody
        self.difficulty = difficulty
        self.melodies_file = melodies_file
        self.current_note_index = 0
        self.melody_data = None
        
        # Definir as cores antes de setup_window
        self.colors = {
            "success": "#28a745",
            "warning": "#ffc107",
            "error": "#dc3545",
            "primary": "#007bff",
            "background": "#1a1a1a"
        }
        
        # Inicializa o reconhecedor de notas e o gravador
        self.note_recognizer = NoteRecognizer()
        self.melody_recorder = MelodyRecorder(self.note_recognizer)
        
        self.load_melody()
        self.setup_window()
        self.is_recording = False
        self.correct_note_time = 0
        self.time_required = 1.0
        self.is_note_correct = False

        # Ajustar tolerância e tempo baseado na dificuldade
        if difficulty == 1:
            self.frequency_tolerance = 130
            self.time_required = 0.8
        elif difficulty == 2:
            self.frequency_tolerance = 80
            self.time_required = 1.0
        else: 
            self.frequency_tolerance = 60
            self.time_required = 1.2

        # Adicione isso junto com os outros labels na inicialização da interface
        self.note_label = ctk.CTkLabel(self.window, text="♪", font=("Arial", 24))
        self.note_label.pack(pady=10)

    def load_melody(self):
        with open(self.melodies_file, 'r', encoding='utf-8') as f:
            melodies = json.load(f)
            self.melody_name = list(melodies.keys())[self.selected_melody]
            self.melody_data = melodies[self.melody_name]

    def setup_window(self):
        self.window = ctk.CTk()
        self.window.title("Jogo de Melodias")
        self.window.geometry("900x700")  # Aumentado para mais espaço
        
        # Configurações visuais
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Configurar frame principal com gradiente
        self.main_frame = ctk.CTkFrame(
            self.window,
            fg_color=self.colors["background"],
            corner_radius=15
        )
        self.main_frame.pack(pady=30, padx=30, fill="both", expand=True)

        # Título com destaque
        title_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )
        title_frame.pack(pady=20, fill="x")

        self.title_label = ctk.CTkLabel(
            title_frame, 
            text="🎵 Jogo de Melodias 🎵",
            font=("Roboto", 32, "bold"),
            text_color=self.colors["primary"]
        )
        self.title_label.pack()

        # Informações da melodia com estilo
        self.melody_info = ctk.CTkLabel(
            self.main_frame,
            text=f"🎼 Melodia: {self.melody_name}\n⭐ Dificuldade: {self.difficulty}",
            font=("Roboto", 18),
            corner_radius=8,
            fg_color=("#2d2d2d", "#2d2d2d"),
            padx=20,
            pady=10
        )
        self.melody_info.pack(pady=15)

        # Frame para frequências com visual melhorado
        self.freq_frame = ctk.CTkFrame(
            self.main_frame,
            corner_radius=10,
            fg_color=("#333333", "#333333")
        )
        self.freq_frame.pack(pady=15, fill="x", padx=40)

        # Label para frequência esperada com nota
        self.expected_freq_label = ctk.CTkLabel(
            self.freq_frame,
            text="♪ Dó | Frequência esperada: 129.20 Hz",
            font=("Roboto", 16),
            anchor="center"
        )
        self.expected_freq_label.pack(pady=(10, 5), fill="x")

        # Label para frequência atual
        self.current_freq_label = ctk.CTkLabel(
            self.freq_frame,
            text="Sua frequência: -",
            font=("Roboto", 16),
            anchor="center"
        )
        self.current_freq_label.pack(pady=(5, 10), fill="x")

        # Adicionar frame para a barra de frequência
        self.frequency_bar_frame = ctk.CTkFrame(
            self.main_frame,
            corner_radius=10,
            fg_color=("#333333", "#333333")
        )
        self.frequency_bar_frame.pack(pady=15, fill="x", padx=40)

        # Label para a barra
        self.frequency_bar_label = ctk.CTkLabel(
            self.frequency_bar_frame,
            text="Frequência",
            font=("Roboto", 14)
        )
        self.frequency_bar_label.pack(pady=(10,5))

        # Canvas para desenhar a barra de frequência
        self.frequency_canvas = ctk.CTkCanvas(
            self.frequency_bar_frame,
            height=60,
            bg="#333333",
            highlightthickness=0
        )
        self.frequency_canvas.pack(fill="x", padx=20, pady=(0,10))

        # Adicionar frame para barra de progresso após a barra de frequência
        self.progress_frame = ctk.CTkFrame(
            self.main_frame,
            corner_radius=10,
            fg_color=("#333333", "#333333")
        )
        self.progress_frame.pack(pady=(15,5), fill="x", padx=40)

        # Label para a barra de progresso
        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="Progresso da Nota",
            font=("Roboto", 14)
        )
        self.progress_label.pack(pady=(10,5))

        # Canvas para desenhar a barra de progresso
        self.progress_canvas = ctk.CTkCanvas(
            self.progress_frame,
            height=30,
            bg="#333333",
            highlightthickness=0
        )
        self.progress_canvas.pack(fill="x", padx=20, pady=(0,10))

        # Frame para botões e status
        self.controls_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )
        self.controls_frame.pack(pady=15, fill="x", padx=40)

        # Botão de gravação estilizado (agora dentro do controls_frame)
        self.record_button = ctk.CTkButton(
            self.controls_frame,
            text="Iniciar Gravação",
            command=self.start_recording,
            font=("Roboto", 18, "bold"),
            height=50,
            corner_radius=25,
            fg_color=self.colors["primary"],
            hover_color="#0056b3"
        )
        self.record_button.pack(pady=10)

        # Status com visual melhorado (agora dentro do controls_frame)
        self.status_label = ctk.CTkLabel(
            self.controls_frame,
            text="Clique em 'Iniciar Gravação' para começar",
            font=("Roboto", 16),
            corner_radius=8,
            fg_color=("#2d2d2d", "#2d2d2d"),
            pady=12
        )
        self.status_label.pack(pady=5)

        # Após criar todos os widgets, adicione:
        # Inicializa a primeira nota e frequência
        first_note = self.melody_data[0]
        self.expected_freq_label.configure(
            text=f"♪ {first_note[1]} | Frequência esperada: {first_note[0]:.2f} Hz"
        )

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

            # Atualizar a barra de frequência
            self.update_frequency_bar(frequency, expected_freq)
            
            if abs(frequency - expected_freq) <= self.frequency_tolerance:
                if not self.is_note_correct:
                    self.is_note_correct = True
                    self.correct_note_time = time.time()
                
                progress = (time.time() - self.correct_note_time) / self.time_required
                self.update_progress_bar(progress)
                
                if progress >= 1.0:
                    self.process_recording()
                    self.is_note_correct = False
                    return
                
                self.status_label.configure(
                    fg_color=self.colors["success"],
                    text_color="white",
                    text=f"Mantenha a nota! {progress*100:.0f}% (±{self.frequency_tolerance}Hz)"
                )
            else:
                self.is_note_correct = False
                self.correct_note_time = 0
                self.update_progress_bar(0)  # Zerar a barra de progresso
                self.status_label.configure(
                    fg_color=self.colors["warning"],
                    text_color="black",
                    text=f"Tente chegar mais perto da frequência esperada (±{self.frequency_tolerance}Hz)"
                )
            
            self.window.after(100, self.update_frequency)

    def update_frequency_bar(self, current_freq, target_freq):
        # Limpar o canvas
        self.frequency_canvas.delete("all")
        
        # Configurações da barra
        canvas_width = self.frequency_canvas.winfo_width()
        canvas_height = self.frequency_canvas.winfo_height()
        bar_height = 20
        
        # Calcular range de frequência para visualização
        freq_range = self.frequency_tolerance * 4
        # Garantir que a frequência mínima nunca seja negativa
        min_freq = max(1, target_freq - freq_range/2)  # Usar 1 como mínimo absoluto
        max_freq = target_freq + freq_range/2
        
        # Converter frequências para posições no canvas
        def freq_to_x(freq):
            # Garantir que a frequência de entrada também não seja negativa
            safe_freq = max(1, freq)
            return ((safe_freq - min_freq) / (max_freq - min_freq)) * canvas_width
        
        # Desenhar fundo da barra
        self.frequency_canvas.create_rectangle(
            0, canvas_height/2 - bar_height/2,
            canvas_width, canvas_height/2 + bar_height/2,
            fill="#444444", outline=""
        )
        
        # Desenhar zona alvo
        target_x = freq_to_x(target_freq)
        tolerance_left = freq_to_x(target_freq - self.frequency_tolerance)
        tolerance_right = freq_to_x(target_freq + self.frequency_tolerance)
        
        self.frequency_canvas.create_rectangle(
            tolerance_left, canvas_height/2 - bar_height/2,
            tolerance_right, canvas_height/2 + bar_height/2,
            fill=self.colors["success"], outline=""
        )
        
        # Desenhar linha da frequência atual
        current_x = freq_to_x(current_freq)
        if current_x >= 0 and current_x <= canvas_width:
            marker_height = bar_height * 1.5
            self.frequency_canvas.create_line(
                current_x, canvas_height/2 - marker_height/2,
                current_x, canvas_height/2 + marker_height/2,
                fill="white", width=3
            )
        
        # Desenhar marcador da frequência alvo
        self.frequency_canvas.create_line(
            target_x, canvas_height/2 - bar_height,
            target_x, canvas_height/2 + bar_height,
            fill="#ffffff", width=2
        )
        
        # Adicionar labels de frequência
        font_size = 10
        self.frequency_canvas.create_text(
            10, canvas_height - 5,
            text=f"{min_freq:.0f}Hz",
            fill="white",
            anchor="sw",
            font=("Roboto", font_size)
        )
        self.frequency_canvas.create_text(
            canvas_width - 10, canvas_height - 5,
            text=f"{max_freq:.0f}Hz",
            fill="white",
            anchor="se",
            font=("Roboto", font_size)
        )
        self.frequency_canvas.create_text(
            target_x, 5,
            text=f"{target_freq:.0f}Hz",
            fill="white",
            anchor="n",
            font=("Roboto", font_size)
        )

    def update_progress_bar(self, progress):
        # Limpar o canvas
        self.progress_canvas.delete("all")
        
        # Configurações da barra
        canvas_width = self.progress_canvas.winfo_width()
        canvas_height = self.progress_canvas.winfo_height()
        
        # Desenhar fundo da barra
        self.progress_canvas.create_rectangle(
            0, 0, canvas_width, canvas_height,
            fill="#444444", outline=""
        )
        
        # Desenhar progresso
        progress = min(1.0, max(0, progress))  # Garantir que fique entre 0 e 1
        progress_width = canvas_width * progress
        
        if progress_width > 0:
            self.progress_canvas.create_rectangle(
                0, 0, progress_width, canvas_height,
                fill=self.colors["success"], outline=""
            )
        
        # Adicionar texto de porcentagem
        percentage = progress * 100
        self.progress_canvas.create_text(
            canvas_width/2, canvas_height/2,
            text=f"{percentage:.0f}%",
            fill="white",
            font=("Roboto", 12, "bold")
        )

    def process_recording(self):
        if self.is_note_correct:
            current_note = self.melody_data[self.current_note_index]
            self.status_label.configure(
                fg_color=self.colors["success"],
                text_color="white",
                text=f"Parabéns! Você acertou a nota!"
            )
            
            self.current_note_index += 1
            if self.current_note_index >= len(self.melody_data):
                self.finish_game()
            else:
                # Prepara para a próxima nota
                next_note = self.melody_data[self.current_note_index]
                self.note_label.configure(text=f"♪ {next_note[1]}")
                self.expected_freq_label.configure(
                    text=f"♪ {next_note[1]} | Frequência esperada: {next_note[0]:.2f} Hz"
                )
                self.current_freq_label.configure(text="Sua frequência: -")
                
                # Atualiza o texto do botão
                self.record_button.configure(text="Próxima Nota")

    def finish_game(self):
        self.status_label.configure(text="Jogo concluído!")
        self.record_button.configure(state="disabled")
        self.note_label.configure(text="Fim do jogo!")

    def start_game(self):
        print("Iniciando Jogo...")
        self.window.mainloop()