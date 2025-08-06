import matplotlib.pyplot as plt
import numpy as np

def plot_poles(poles):
    """
    Affiche les pôles dans le plan complexe

    Args:
        poles (array-like): liste des pôles (valeurs propres)
    """
    poles = np.array(poles)
    plt.figure()
    plt.axhline(0, color='gray', linestyle='--')
    plt.axvline(0, color='gray', linestyle='--')
    plt.plot(poles.real, poles.imag, 'rx', markersize=10)
    plt.title("Pôles du système dans le plan complexe")
    plt.xlabel("Partie réelle")
    plt.ylabel("Partie imaginaire")
    plt.grid(True)
    plt.axis('equal')
    plt.show()
