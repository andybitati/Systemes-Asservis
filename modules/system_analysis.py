import numpy as np
from scipy.signal import ss2tf, impulse, step, bode
from numpy.linalg import eigvals
import matplotlib.pyplot as plt
from control import ss
import control

class StateSpaceSystem:
    def __init__(self, A, B, C, D):
        self.A = np.array(A, dtype=float)
        self.B = np.array(B, dtype=float)
        self.C = np.array(C, dtype=float)
        self.D = np.array(D, dtype=float)

        # Valide juste les dimensions ici
        self._check_dimensions()

        # Crée le système après validation
        self.system = ss(self.A, self.B, self.C, self.D)

        # Calcule les propriétés
        self.analysis = self._analyze_system()

    def _check_dimensions(self):
        n, m = self.A.shape[0], self.B.shape[1]
        p = self.C.shape[0]
        
        assert self.A.shape == (n, n), "Matrice A doit être carrée"
        assert self.B.shape == (n, m), "Dimensions B incompatibles avec A"
        assert self.C.shape == (p, n), "Dimensions C incompatibles avec A"
        assert self.D.shape == (p, m), "Dimensions D incompatibles avec B/C"

    def _analyze_system(self):
        poles = control.poles(self.system)
        est_stable = all(np.real(p) < 0 for p in poles)

        t, y = control.impulse_response(self.system)
        omega = np.logspace(-2, 2, 500)  # plage de fréquences
        mag, phase, omega = control.frequency_response(self.system, omega)


        return {
            "poles": poles,
            "stable": est_stable,
            "temps": t,
            "reponse": y,
            "frequence": omega,
            "gain": mag,
            "phase": phase
        }
