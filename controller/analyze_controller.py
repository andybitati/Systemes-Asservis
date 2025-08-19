# controller/analyze_controller.py

"""
Contrôleur pour l’analyse des systèmes dynamiques linéaires :
- Calcul des pôles
- Vérification de la stabilité
- Analyse de la contrôlabilité et de l’observabilité
"""

from modules.system_analysis import StateSpaceSystem


def analyze_system(A, B, C, D):
    """
    Analyse un système à partir de ses matrices (A, B, C, D)

    
    """
    system = StateSpaceSystem(A, B, C, D)
    
    return system.analysis
   
   
    
