import numpy as np
from scipy.signal import place_poles
from scipy.integrate import solve_ivp

class StateFeedbackController:
    def __init__(self, A, B):
        self.A = np.array(A, dtype=float)
        self.B = np.array(B, dtype=float)
        self.n = self.A.shape[0]

    def compute_gain(self, desired_poles):
        """
        Calcule le gain d’état K tel que (A - BK) a les pôles désirés
        """
        result = place_poles(self.A, self.B, desired_poles)
        self.K = result.gain_matrix
        return self.K

    def simulate_open_loop(self, x0, t_span):
        """
        Simule le système en boucle ouverte (sans feedback)
        dx/dt = Ax + Bu avec u=0
        """
        def open_loop_dynamics(t, x):
            return self.A @ x

        sol = solve_ivp(open_loop_dynamics, t_span, x0, t_eval=np.linspace(t_span[0], t_span[1], 500))
        return sol.t, sol.y

    def simulate_closed_loop(self, x0, t_span):
        """
        Simule le système en boucle fermée avec feedback u = -Kx
        dx/dt = (A - BK)x
        """
        if not hasattr(self, 'K'):
            raise ValueError("Gain K non défini. Appeler compute_gain() d'abord.")

        A_cl = self.A - self.B @ self.K

        def closed_loop_dynamics(t, x):
            return A_cl @ x

        sol = solve_ivp(closed_loop_dynamics, t_span, x0, t_eval=np.linspace(t_span[0], t_span[1], 500))
        return sol.t, sol.y

    def get_closed_loop_matrix(self):
        """
        Retourne la matrice A_cl = A - BK
        """
        if not hasattr(self, 'K'):
            raise ValueError("Gain K non défini. Appeler compute_gain() d'abord.")
        return self.A - self.B @ self.K
