import matplotlib.pyplot as plt
from control import impulse_response

def plot_impulse_response(system):
    """
    Affiche la réponse impulsionnelle du système

    Args:
        system (control.TransferFunction or StateSpace): Système LTI
    """
    t, y = impulse_response(system)
    plt.figure()
    plt.plot(t, y)
    plt.title("Réponse impulsionnelle du système")
    plt.xlabel("Temps (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.show()
