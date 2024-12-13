import serial
import time
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(base_dir)

from controller.frequency_state import get_current_frequency
from controller.arduino_communication import ArduinoCommunication

class FrequencySender:
    def __init__(self):
        self.porta_serial = serial.Serial('COM9', 9600, timeout=1)
        self.porta_serial.reset_input_buffer()
        time.sleep(2)
        
        # Instancia o ArduinoCommunication para monitorar frequências
        self.arduino_comm = ArduinoCommunication()
        
    def iniciar_envio(self):
        print("Iniciando envio automático de frequência para COM9...")
        
        # Inicia o monitoramento de frequência do Arduino
        self.arduino_comm.read_serial()
        
        try:
            while True:
                frequencia = get_current_frequency()
                if frequencia > 0:
                    print(f"Frequência enviada: {frequencia}")
                    self.enviar_frequencia(frequencia)
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\nEncerrando o envio de frequência...")
        finally:
            self.fechar()
    
    def enviar_frequencia(self, frequencia):
        try:
            print(f"Frequência enviada: {frequencia}")
            comando = f"setpoint {frequencia}\n"
            self.porta_serial.write(comando.encode('utf-8'))
            
            if self.porta_serial.in_waiting:
                resposta = self.porta_serial.readline().decode().strip()
                print(f"Resposta do Arduino: {resposta}")
                
        except Exception as e:
            print(f"Erro ao enviar frequência: {e}")
    
    def fechar(self):
        if self.porta_serial.is_open:
            self.porta_serial.close()

if __name__ == "__main__":
    sender = FrequencySender()
    sender.iniciar_envio()