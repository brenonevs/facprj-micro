import serial
import sys
import os
import json
import numpy as np
import threading
from time import sleep

sys.stdout.reconfigure(encoding='utf-8')

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(base_dir)

from views.game_view import GameInterface
from services.melody_recorder import MelodyRecorder
from controller.frequency_state import get_current_frequency

class ArduinoCommunication:
    def __init__(self):
        self.serial_receiver = serial.Serial('COM7', 9600, timeout=1)  
        self.serial_sender = serial.Serial('COM9', 9600, timeout=1)
        self.melodies_file = os.path.join(os.path.dirname(base_dir), "melodies.json")
        print(f"Caminho do arquivo de melodias: {self.melodies_file}")
        
        # Mapeamento de dificuldades
        self.difficulty_map = {
            "facil": 1,
            "medio": 2,
            "dificil": 3
        }

        self.is_sending_frequency = False
        self.frequency_thread = None
        self.is_monitoring = False

    def read_serial(self):
        # Criar thread separada para monitorar a frequência
        def print_frequency():
            while True:
                if self.is_monitoring:  # Só envia frequência quando o monitoramento estiver ativo
                    print(f"Frequência atual: {get_current_frequency()}")
                    frequency = get_current_frequency()
                    mapped_frequency = int(self.map(frequency, 80, 1100, 70, 200))
                    print(f"Frequência mapeada enviada: {mapped_frequency}")
                    command = f"setpoint {mapped_frequency}\n"
                    
                    print(f"Frequência original: {frequency}, Frequência mapeada: {mapped_frequency}")
                    self.serial_sender.write(command.encode('utf-8'))
                sleep(0.1)  # Atualiza a cada 0.1 segundos
        
        # Inicia o thread de monitoramento
        threading.Thread(target=print_frequency, daemon=True).start()
        
        # Loop principal de leitura serial
        while True:
            if self.serial_receiver.in_waiting:
                command = self.serial_receiver.readline().decode('utf-8').strip()
                print(f"Comando recebido: {command}")
                self.process_command(command)

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
                melody_number = int(parts[2]) - 1

                if difficulty_name not in self.difficulty_map:
                    print(f"Dificuldade inválida: {difficulty_name}")
                    return
                
                difficulty = self.difficulty_map[difficulty_name]
                print(f"Iniciando jogo com dificuldade {difficulty_name} e melodia {melody_number + 1}")
                
                game_interface = GameInterface(melody_number, difficulty, self.melodies_file)
                self.start_frequency_monitoring()
                game_interface.start_game()
                self.stop_frequency_monitoring()
            else:
                print("Formato de comando inválido")
                
        except Exception as e:
            print(f"Erro ao processar comando: {str(e)}")

    def record_melody(self):
        print("Recording melody")
        melody_recorder = MelodyRecorder()
        melody_recorder.record_melody()

    def start_frequency_monitoring(self):
        self.is_monitoring = True
        
    def stop_frequency_monitoring(self):
        self.is_monitoring = False

    def map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

if __name__ == "__main__":
    arduino = ArduinoCommunication()
    arduino.read_serial()
