import os
import sys

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

sys.path.append(base_dir)

from src.views.recorder_view import AudioApp

class MelodyRecorder:
    def __init__(self):
        self.app = AudioApp()
    
    def record_melody(self):
        self.app.mainloop()
