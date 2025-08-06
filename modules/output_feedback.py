import numpy as np
from scipy.signal import place_poles
from scipy.integrate import solve_ivp

class OutputFeedbackSystem:
    def __init__(self, A, B, C):
        self.A = np.array(A, dtype=float)
        self.B = np.array(B, dtype=float)
        self.C = np.array(C, dtype=float)
        self.n = self.A.shape[0]

    def set_state_feedback_gain(self, K):
        self.K = np.array(K, dtype=float)

    def compute_observer_gain(self, desired_observer_poles):
        """
        Calcule le gain L de l’observateur tel que (A - LC) a les pôles désirés
        """
        result = place_poles(self.A.T, self.C.T, desired_observer_poles)
        self.L = result.gain_matrix.T
        return self.L

    def simulate_output_feedback(self, x0, xhat0, t_span):
        """
        Simule le système avec retour de sortie :
        dx/dt = Ax + Bu
        dẋ̂/dt = A x̂ + B u + L(y - C x̂)
        u = -K x̂
        """
        if not hasattr(self, 'K') or not hasattr(self, 'L'):
            raise ValueError("Gains K et L doivent être définis.")

        A = self.A
        B = self.B
        C = self.C
        K = self.K
        L = self.L

        def dynamics(t, z):
            x = z[:self.n]
            x_hat = z[self.n:]
            y = C @ x
            
            y_hat = C @ x_hat
            u = -K @ x_hat
            dx = A @ x + B @ u
            dx_hat = A @ x_hat + B @ u + L @ (y - y_hat)
            return np.concatenate((dx, dx_hat))

        z0 = np.concatenate((x0, xhat0))
        sol = solve_ivp(dynamics, t_span, z0, t_eval=np.linspace(t_span[0], t_span[1], 500))
        return sol.t, sol.y[:self.n], sol.y[self.n:]
