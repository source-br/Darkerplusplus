import os
import sys

def resource_path(relative_path):
    """ Retorna o caminho correto para arquivos dentro do exe """
    if getattr(sys, 'frozen', False):  # Se estiver rodando no .exe
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)