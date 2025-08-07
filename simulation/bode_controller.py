# controller/bode_controller.py

import matplotlib.pyplot as plt
import numpy as np
from control import frequency_response

def plot_bode(system, save_path=None):
    """
    Trace et sauvegarde (optionnellement) le diagramme de Bode.

    Args:
        system (TransferFunction): système à analyser
        save_path (str): chemin d’enregistrement si souhaité
    """
    # Fréquence log-spacée
    omega = np.logspace(-2, 2, 1000)  # de 0.01 à 100 rad/s

    # Calcul manuel de la réponse fréquentielle
    _, mag, phase = frequency_response(system, omega)

    # Diagramme
    fig, (ax_mag, ax_phase) = plt.subplots(2, 1, figsize=(8, 6))

    ax_mag.semilogx(omega, 20 * np.log10(abs(mag)))
    ax_mag.set_title("Diagramme de Bode - Magnitude")
    ax_mag.set_ylabel("Gain (dB)")
    ax_mag.grid(True, which='both')

    ax_phase.semilogx(omega, np.degrees(np.angle(phase)))
    ax_phase.set_title("Diagramme de Bode - Phase")
    ax_phase.set_ylabel("Phase (°)")
    ax_phase.set_xlabel("Fréquence (rad/s)")
    ax_phase.grid(True, which='both')

    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Diagramme de Bode enregistré : {save_path}")
        plt.close(fig)
    else:
        plt.show()
