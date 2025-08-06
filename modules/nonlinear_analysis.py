import numpy as np
import sympy as sp
from sympy.utilities.lambdify import lambdify
from scipy.integrate import solve_ivp

class NonlinearSystem:
    def __init__(self, state_vars, dynamics_exprs):
        """
        state_vars: liste de symboles (ex: [x1, x2])
        dynamics_exprs: liste d'expressions symboliques (ex: [x2, -x1 + (1 - x1**2)*x2])
        """
        self.x = state_vars
        self.f = dynamics_exprs
        self.f_func = lambdify(self.x, self.f, modules='numpy')

    def evaluate_dynamics(self, x_vals):
        return np.array(self.f_func(*x_vals), dtype=float)

    def linearize_at(self, eq_point):
        """
        Linéarise autour d'un point d'équilibre : retourne la matrice Jacobienne évaluée
        """
        J = sp.Matrix(self.f).jacobian(self.x)
        J_at_point = J.subs(zip(self.x, eq_point))
        return np.array(J_at_point.evalf(), dtype=float)

    def simulate(self, x0, t_span):
        """
        Simule numériquement le système non linéaire dx/dt = f(x)
        """
        def dyn(t, x):
            return self.evaluate_dynamics(x)

        sol = solve_ivp(dyn, t_span, x0, t_eval=np.linspace(t_span[0], t_span[1], 1000))
        return sol.t, sol.y

    def check_lyapunov_function(self, V_expr):
        """
        Vérifie si V(x) est une fonction de Lyapunov candidate.
        Retourne :
            V(x), dV(x)/dt symboliquement
        """
        V = sp.sympify(V_expr)
        dVdx = [sp.diff(V, xi) for xi in self.x]
        dVdt = sum(dVdx[i] * self.f[i] for i in range(len(self.x)))
        return V, dVdt
