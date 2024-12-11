import serial
import time
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(base_dir)

from controller.frequency_state import get_current_frequency

class ComandoSerial:
    def __init__(self):
        # Configurar a conexão serial
        self.porta_serial = serial.Serial('COM9', 9600, timeout=1)
        self.porta_serial.reset_input_buffer()  # Limpa o buffer na inicialização
        time.sleep(2)
        
    def enviar_comando(self, comando):
        try:
            # Limpa os buffers antes de enviar novo comando
            self.porta_serial.reset_input_buffer()
            self.porta_serial.reset_output_buffer()
            
            # Formatar e enviar comando
            comando_completo = f"{comando}\n"
            self.porta_serial.write(comando_completo.encode('utf-8'))
            print(f"Comando enviado: {comando_completo.strip()}")
            
            # Aumenta o tempo de espera para resposta
            time.sleep(0.5)
            if self.porta_serial.in_waiting:
                resposta = self.porta_serial.readline().decode().strip()
                print(f"Resposta do Arduino: {resposta}")
                
        except Exception as e:
            print(f"Erro: {e}")
    
    def fechar(self):
        self.porta_serial.close()

if __name__ == "__main__":
    comunicacao = ComandoSerial()
    
    try:
        print("Iniciando envio automático de frequência...")
        while True:
            frequencia = get_current_frequency()
            comando = f"setpoint {frequencia}"
            comunicacao.enviar_comando(comando)
            time.sleep(1)  # Aguarda 1 segundo entre os envios
            
    except KeyboardInterrupt:
        print("\nEncerrando o programa...")
    finally:
        comunicacao.fechar()