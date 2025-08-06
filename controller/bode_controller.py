import matplotlib.pyplot as plt
from control import bode

def plot_bode(system):
    """
    Affiche le diagramme de Bode du système

    Args:
        system (control.TransferFunction or StateSpace): Système LTI
    """
    plt.figure()
    bode(system, dB=True)
    plt.suptitle("Diagramme de Bode")
    plt.grid(True)
    plt.show()
