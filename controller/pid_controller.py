"""
Contrôleur pour la régulation PID :
- Définition d’un système par fonction de transfert
- Application d’un PID
- Calculs : réponse temporelle, erreur, Bode, pôles
"""

from modules.pid_design import PIDModel

def simulate_pid(num, den, Kp, Ki, Kd):
    """
    Simule un système en boucle fermée avec PID

    Args:
        num, den : numérateur et dénominateur de la FT
        Kp, Ki, Kd : gains PID

    Returns:
        dict contenant :
            - t, y       : réponse temporelle (temps, sortie)
            - t_err, err : erreur de suivi
            - omega, magnitude, phase : données pour Bode
            - system_open_loop : FT PID * FT du système
            - poles : pôles de la FT en boucle ouverte
    """
    sys = PIDModel(num, den)
    sys.set_pid_gains(Kp, Ki, Kd)

    # Réponse temporelle
    t, y = sys.closed_loop_response()

    # Erreur de suivi
    t_err, e = sys.compute_tracking_error()

    # Réponse en fréquence
    omega, mag, phase = sys.bode_plot_data()

    # Fonction de transfert en boucle ouverte
    system_open_loop = sys.pid * sys.sys

    return {
        "t": t,
        "y": y,
        "t_err": t_err,
        "err": e,
        "omega": omega,
        "magnitude": mag,
        "phase": phase,
        "system_open_loop": system_open_loop,
        "poles": system_open_loop.poles()
    }
