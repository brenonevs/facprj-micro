import serial
import sys
import os

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(base_dir)

from services.melody_recorder import MelodyRecorder

class ArduinoCommunication:
    def __init__(self):
        self.commands = {
           "record_melody": "record_melody",
           "play_melody": "play_melody",
           "stop_melody": "stop_melody",
           "clear_melody": "clear_melody"
        }

    def send_command(self):
        while True:
            message = input("Enter a command: ")
            if message in self.commands:
                self.process_command(message)
            else:
                print("Invalid command")

    def receive_command(self, command):
        if command in self.commands:
            return self.commands[command]
        else:
            return "Invalid command"
    
    def process_command(self, command):
        if command == self.commands["record_melody"]:
            self.record_melody()
        elif command == self.commands["play_melody"]:
            self.play_melody()
        elif command == self.commands["stop_melody"]:
            self.stop_melody()
        elif command == self.commands["clear_melody"]:
            self.clear_melody()

    def record_melody(self):
        print("Recording melody")
        melody_recorder = MelodyRecorder()
        melody_recorder.record_melody()

    def play_melody(self):
        print("Playing melody")
    
    def stop_melody(self):
        print("Stopping melody")

    def clear_melody(self):
        print("Clearing melody")

if __name__ == "__main__":
    arduino = ArduinoCommunication()
    arduino.send_command()
