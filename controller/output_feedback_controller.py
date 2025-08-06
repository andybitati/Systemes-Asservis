# controller/output_feedback_controller.py

"""
Contrôleur pour la commande par sortie observée :
- Calcul des gains K et L
- Simulation du système avec estimation d’état
"""

from modules.output_feedback import OutputFeedbackSystem

def simulate_output_feedback(A, B, C, K, observer_poles, x0, xhat0, t_span):
    """
    Simule le système avec retour de sortie (observateur)

    Args:
        A, B, C : matrices du système
        K : gain de feedback état
        observer_poles : pôles souhaités pour l’observateur
        x0 : état initial réel
        xhat0 : état initial estimé
        t_span : tuple (t0, tf)

    Returns:
        dict contenant :
            - gain L
            - temps, états réels et estimés
    """
    sys = OutputFeedbackSystem(A, B, C)
    sys.set_state_feedback_gain(K)
    L = sys.compute_observer_gain(observer_poles)
    t, x, xhat = sys.simulate_output_feedback(x0, xhat0, t_span)

    return {
        "L": L,
        "t": t,
        "x": x,
        "x_hat": xhat
    }
