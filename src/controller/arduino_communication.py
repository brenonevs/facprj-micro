import serial
import sys
import os
import json

sys.stdout.reconfigure(encoding='utf-8')

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(base_dir)

from services.melody_recorder import MelodyRecorder
from services.melody_preview import MelodyPreview

class ArduinoCommunication:
    def __init__(self):
        self.commands = {
           "record": "record_melody",
           "preview": "preview_melody",
           "select_difficulty": "select_difficulty",
           "stop_melody": "stop_melody",
           "clear_melody": "clear_melody"
        }


        #TODO: Essa parte vai virar uma nova classe GameConfig
        self.selected_melody = None
        self.selected_difficulty = None

        self.melodies_file = os.path.join(os.path.dirname(base_dir), "melodies.json")
        print(f"Caminho do arquivo de melodias: {self.melodies_file}")  # Debug)

    def send_command(self):
        while True:
            message = input("Enter a command: ")
            if message in self.commands.keys():
                self.process_command(message)
            else:
                print("Invalid command")

    def process_command(self, command):
        if command == "record": 
            self.record_melody()

        elif command == "preview":
            self.preview_melody()

        elif command == "select_difficulty":
            self.select_difficulty()

        elif command == "clear_melody":
            self.clear_melody()

    def record_melody(self):
        print("Recording melody")
        melody_recorder = MelodyRecorder()
        melody_recorder.record_melody()

    def preview_melody(self):
        if not os.path.exists(self.melodies_file):
            print("Arquivo de melodias não encontrado.")
            return

        try:
            with open(self.melodies_file, 'r', encoding='utf-8') as f:
                melodias = json.load(f)
            
            if not melodias:
                print("Nenhuma melodia encontrada no arquivo.")
                return

            print("\nMelodias disponíveis:")
            for i, nome_melodia in enumerate(melodias.keys(), 1):
                print(f"{i}. {nome_melodia}")

            try:
                self.selected_melody = int(input("\nEscolha o número da melodia que deseja tocar: ")) - 1
                nomes_melodias = list(melodias.keys())
                
                if 0 <= self.selected_melody < len(nomes_melodias):
                    melodia_selecionada = nomes_melodias[self.selected_melody]
                    dados_melodia = melodias[melodia_selecionada]
                    print(f"Tocando melodia: {melodia_selecionada}")
                    
                    melody_preview = MelodyPreview()
                    melody_preview.preview_melody(dados_melodia)
                else:
                    print("Número inválido. Por favor, escolha um número válido da lista.")
            except ValueError:
                print("Entrada inválida. Por favor, digite um número.")
                
        except json.JSONDecodeError:
            print("Erro ao ler o arquivo de melodias. Formato JSON inválido.")
        except Exception as e:
            print(f"Erro ao processar melodias: {str(e)}")

    def select_difficulty(self):
        print("Select difficulty")
        self.difficulty = int(input("Digite a dificuldade (1, 2, 3): "))
        if self.difficulty not in [1, 2, 3]:
            print("Dificuldade inválida. Por favor, digite um número válido.")
            self.select_difficulty()
    
    def start_game(self):
        print("Starting game")

if __name__ == "__main__":
    arduino = ArduinoCommunication()
    arduino.send_command()