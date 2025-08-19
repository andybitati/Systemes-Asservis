# main.py
import sys
import os
import tkinter as tk
from gui.Test_window import MainWindow
# Ajoute le dossier racine du projet aux chemins de recherche
sys.path.append(os.path.dirname(os.path.abspath(__file__)))



if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()