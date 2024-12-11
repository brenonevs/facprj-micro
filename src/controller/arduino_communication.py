import serial
import sys
import os
import json
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(base_dir)

from views.game_view import GameInterface
from services.melody_recorder import MelodyRecorder
from controller.frequency_state import current_frequency

class ArduinoCommunication:
    def __init__(self):
        self.serial_receiver = serial.Serial('COM7', 9600, timeout=1)  
        self.serial_sender = serial.Serial('COM8', 9600, timeout=1) 
        self.melodies_file = os.path.join(os.path.dirname(base_dir), "melodies.json")
        print(f"Caminho do arquivo de melodias: {self.melodies_file}")
        
        # Mapeamento de dificuldades
        self.difficulty_map = {
            "facil": 1,
            "medio": 2,
            "dificil": 3
        }

    def read_serial(self):
        while True:
            if self.serial_receiver.in_waiting:
                command = self.serial_receiver.readline().decode('utf-8').strip()
                print(f"Comando recebido: {command}")
                self.process_command(command)
    
    def send_command(self, command):
        try:
            command = f"{command}\n"
            self.serial_sender.write(command.encode('utf-8'))
            print(f"Comando enviado: {command.strip()}")
        except Exception as e:
            print(f"Erro ao enviar comando: {str(e)}")

    def send_command_frequency(self, frequency):
        # Mapeia a frequência (80-1100) para potência do motor (0-255)
        potencia = int(np.interp(frequency, [80, 1100], [0, 255]))
        self.send_command(f"setpoint {potencia}")

    def process_command(self, command):
        try:
            # Verifica primeiro se é o comando CriarMelodia
            if command.strip().lower() == "criarmelodia":
                print("Iniciando gravação de melodia")
                self.record_melody()
                return

            # Formato esperado: "Iniciar dificuldade numero_melodia"
            parts = command.split()
            if len(parts) == 3 and parts[0].lower() == "iniciar":
                difficulty_name = parts[1].lower()
                melody_number = int(parts[2]) - 1  # Converte para índice base-0
                
                # Valida e configura a dificuldade
                if difficulty_name not in self.difficulty_map:
                    print(f"Dificuldade inválida: {difficulty_name}")
                    return
                
                difficulty = self.difficulty_map[difficulty_name]
                
                # Inicia o jogo
                print(f"Iniciando jogo com dificuldade {difficulty_name} e melodia {melody_number + 1}")
                game_interface = GameInterface(melody_number, difficulty, self.melodies_file)
                game_interface.start_game()
            else:
                print("Formato de comando inválido")
                
        except Exception as e:
            print(f"Erro ao processar comando: {str(e)}")

    def record_melody(self):
        print("Recording melody")
        melody_recorder = MelodyRecorder()
        melody_recorder.record_melody()

if __name__ == "__main__":
    arduino = ArduinoCommunication()
    arduino.read_serial()