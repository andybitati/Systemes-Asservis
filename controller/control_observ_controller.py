from modules.controllability import ControlObservabilityAnalyzer
import numpy as np
from numpy.linalg import matrix_rank

    
   
def control_observ(A, B, C, D):
    
    """
    vérifie la commandabilité et l'observabilité du système et génère les matrice d'observabilité et de commandabilité

    
    """
    obj = ControlObservabilityAnalyzer(A,B,C,D)
    
    Wc = obj.controllability_matrix()
    rang_Wc = matrix_rank(Wc)
    
    Wo = obj.observability_matrix()
    rang_Wo = matrix_rank(Wo)
    
    conclusion = obj.summary()
    
    return {
        'rang_Wc': rang_Wc,
        'rang_Wo': rang_Wo,
        'conclusion': conclusion
    }
