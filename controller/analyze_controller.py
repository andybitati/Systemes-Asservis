# controller/analyze_controller.py

"""
Contrôleur pour l’analyse des systèmes dynamiques linéaires :
- Calcul des pôles
- Vérification de la stabilité
- Analyse de la contrôlabilité et de l’observabilité
"""

from modules.system_analysis import StateSpaceSystem
from modules.controllability import ControlObservabilityAnalyzer

def analyze_system(A, B, C, D):
    """
    Analyse un système à partir de ses matrices (A, B, C, D)

    Args:
        A, B, C, D : listes ou matrices numpy représentant le système

    Returns:
        dict contenant les pôles, la stabilité, et un résumé de contrôlabilité / observabilité
    """
    system = StateSpaceSystem(A, B, C, D)
    poles = system.get_poles()
    stable = system.is_stable()

    analyzer = ControlObservabilityAnalyzer(A, B, C)
    summary = analyzer.summary()

    return {
        "poles": poles,
        "is_stable": stable,
        "summary": summary
    }
