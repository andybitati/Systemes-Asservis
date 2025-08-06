# main.py
import sys
import os

# Ajoute le dossier racine du projet aux chemins de recherche
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controller.main_controller import run_all

if __name__ == "__main__":
    run_all()
