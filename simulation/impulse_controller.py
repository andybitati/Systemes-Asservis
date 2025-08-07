# controller/impulse_controller.py

import matplotlib.pyplot as plt
from control import impulse_response
import numpy as np

def plot_impulse_response(system, save_path=None):
    """
    Affiche ou sauvegarde la réponse impulsionnelle du système.

    Args:
        system (TransferFunction ou StateSpace): système linéaire à analyser
        save_path (str): chemin pour enregistrer l’image PNG (optionnel)
    """
    t, y = impulse_response(system)
    fig, ax = plt.subplots()
    ax.plot(t, y)
    ax.set_title("Réponse impulsionnelle du système")
    ax.set_xlabel("Temps (s)")
    ax.set_ylabel("Amplitude")
    ax.grid(True)

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Réponse impulsionnelle enregistrée : {save_path}")
        plt.close(fig)
    else:
        plt.show()
