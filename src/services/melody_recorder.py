import os
import sys

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

sys.path.append(base_dir)

from views.audio_app import AudioApp

if __name__ == "__main__":
    app = AudioApp()
    app.mainloop()
