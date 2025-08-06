# controller/state_feedback_controller.py

"""
Contrôleur pour la commande par retour d’état :
- Calcul du gain K pour placement de pôles
- Simulation boucle ouverte et boucle fermée
"""

from modules.state_feedback import StateFeedbackController

def compute_state_feedback(A, B, desired_poles, x0, t_span):
    """
    Calcule la commande état et simule la réponse

    Args:
        A, B : matrices système
        desired_poles : liste des pôles souhaités
        x0 : état initial
        t_span : tuple (t0, tf)

    Returns:
        dict contenant :
            - gain K
            - temps et sorties pour boucle ouverte et boucle fermée
    """
    controller = StateFeedbackController(A, B)
    K = controller.compute_gain(desired_poles)
    t_ol, y_ol = controller.simulate_open_loop(x0, t_span)
    t_cl, y_cl = controller.simulate_closed_loop(x0, t_span)

    return {
        "K": K,
        "t_open": t_ol,
        "y_open": y_ol,
        "t_closed": t_cl,
        "y_closed": y_cl
    }
