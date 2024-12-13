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
    def __init__(self, game_interface):
        self.serial_receiver = serial.Serial('COM22', 9600, timeout=10)  
        self.serial_sender = serial.Serial('COM21', 115200, timeout=10)
        self.melodies_file = os.path.join(os.path.dirname(base_dir), "melodies.json")
        print(f"Caminho do arquivo de melodias: {self.melodies_file}")
        self.game_interface = game_interface
        self.difficulty = None
        
        # Mapeamento de dificuldades
        self.difficulty_map = {
            "facil": 1,
            "medio": 2,
            "dificil": 3
        }

        self.tempos = {
            1: 60,
            2: 30,
            3: 15
        }

        self.alturas = {
            "dó": 3,
            "ré": 4,
            "mi": 5,
            "fá": 6,
            "sol": 7,
            "lá": 8,
            "si": 9
        }

        self.is_sending_frequency = False
        self.frequency_thread = None
        self.is_monitoring = False

    def read_serial(self):
        def print_frequency():
            while True:
                if self.is_monitoring: 
                    #print(f"Frequência atual: {get_current_frequency()}")
                    frequency = get_current_frequency()
                    mapped_frequency = int(self.map(frequency, 200, 1100, 0, 200))
                    #print(f"Frequência mapeada enviada: {mapped_frequency}")
                    
                    #print(f"Frequência original: {frequency}, Frequência mapeada: {mapped_frequency}")
                    
                    comando = f"setpoint {mapped_frequency}\n"

                    self.serial_sender.reset_output_buffer()
                    if mapped_frequency > 0:
                        self.serial_sender.write(comando.encode("utf-8"))
                        #print(comando, end="")
                sleep(0.5) 
        
        # Inicia o thread de monitoramento
        threading.Thread(target=print_frequency, daemon=True).start()
        
        
        self.serial_sender.write("conectei".encode("utf-8"))
        # Loop principal de leitura serial
        while True:
            if self.game_interface.win:
                self.serial_sender.write("ganhou".encode("utf-8"))

            if self.serial_receiver.in_waiting:
                command = self.serial_receiver.readline().decode('utf-8').strip()
                print(f"Comando recebido: {command}")
                self.process_command(command)

            if self.serial_sender.in_waiting:
                command = self.serial_sender.readline().decode('utf-8').strip()
                print(f"Comando sender recebido: {command}")
                self.process_command(command)

    def process_command(self, command):
        try:
            # Verifica primeiro se é o comando CriarMelodia
            if command.strip().lower() == "criarmelodia":
                print("Iniciando gravação de melodia")
                self.record_melody()
                return

            elif command.strip().lower() == "próxima nota":
                print("proxima nota")
                if self.game_interface:
                    self.current_note = self.game_interface.melody_data[self.game_interface.current_note_index]
                    comando = f"altura meta {self.alturas[self.current_note[1]]}\n"
                    self.serial_sender.write(comando.encode("utf-8"))
                    print(comando)

            elif len(command.split()) == 3 and command.split()[0].lower() == "iniciar":
                parts = command.split()
                difficulty_name = parts[1].lower()
                melody_number = int(parts[2]) - 1

                if difficulty_name not in self.difficulty_map:
                    print(f"Dificuldade inválida: {difficulty_name}")
                    return
                
                self.difficulty = self.difficulty_map[difficulty_name]
                print(f"Iniciando jogo com dificuldade {difficulty_name} e melodia {melody_number + 1}")
                
                #self.game_interface = GameInterface(melody_number, self.difficulty, self.melodies_file)
                self.current_note = self.game_interface.melody_data[self.game_interface.current_note_index]
                self.start_frequency_monitoring()
                
                self.serial_sender.write("conectei".encode("utf-8"))
                print("iniciei")
                #tkinter_thread = threading.Thread(target=self.game_interface.start_game, daemon=True)
                #tkinter_thread.start()
                print("criei a interface")
                #self.stop_frequency_monitoring()

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
    game_interface = GameInterface(1, 1, os.path.join(os.path.dirname(base_dir), "melodies.json"))
    arduino = ArduinoCommunication(game_interface)
    threading.Thread(target=arduino.read_serial, daemon=True).start()
    game_interface.start_game()

