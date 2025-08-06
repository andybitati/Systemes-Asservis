# controller/pid_controller.py

"""
Contrôleur pour la régulation PID :
- Définition d’un système par fonction de transfert
- Application d’un PID
- Calculs : réponse, erreur, Bode
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
            - réponse temporelle
            - erreur de suivi
            - données Bode (omega, magnitude, phase)
    """
    sys = PIDModel(num, den)
    sys.set_pid_gains(Kp, Ki, Kd)
    t, y = sys.closed_loop_response()
    t_err, e = sys.compute_tracking_error()
    omega, mag, phase = sys.bode_plot_data()

    return {
        "t": t,
        "y": y,
        "t_err": t_err,
        "err": e,
        "omega": omega,
        "magnitude": mag,
        "phase": phase
    }
