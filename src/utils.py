import os
import sys

def resource_path(relative_path):
    # Returns the correct path for files inside the exe
    if getattr(sys, 'frozen', False):  # If running in the .exe
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)