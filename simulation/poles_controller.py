# controller/poles_controller.py

import matplotlib.pyplot as plt
import numpy as np

def plot_poles(poles, save_path=None):
    """
    Affiche ou sauvegarde le diagramme des pôles dans le plan complexe.

    Args:
        poles (array-like): liste ou tableau des pôles complexes
        save_path (str): si spécifié, sauvegarde le graphique à ce chemin (PNG)
    """
    poles = np.array(poles)
    fig, ax = plt.subplots()
    ax.plot(poles.real, poles.imag, 'rx', markersize=10)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_title("Pôles dans le plan complexe")
    ax.set_xlabel("Partie réelle")
    ax.set_ylabel("Partie imaginaire")
    ax.grid(True)

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Diagramme des pôles enregistré : {save_path}")
        plt.close(fig)
    else:
        plt.show()
