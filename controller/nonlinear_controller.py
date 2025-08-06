# controller/nonlinear_controller.py

"""
Contrôleur pour les systèmes non linéaires :
- Simulation
- Linéarisation autour d’un point
- Vérification de fonction de Lyapunov
"""

from modules.nonlinear_analysis import NonlinearSystem

def analyze_nonlinear_system(state_vars, dynamics_exprs, x0, t_span, eq_point, V_expr):
    """
    Analyse un système non linéaire

    Args:
        state_vars : liste de symboles sympy (ex: [x1, x2])
        dynamics_exprs : équations dynamiques symboliques
        x0 : état initial
        t_span : intervalle de temps
        eq_point : point d’équilibre
        V_expr : fonction de Lyapunov symbolique (ex: "x1**2 + x2**2")

    Returns:
        dict contenant :
            - solution temporelle
            - Jacobienne
            - V(x) et dV/dt
    """
    sys = NonlinearSystem(state_vars, dynamics_exprs)
    t, y = sys.simulate(x0, t_span)
    J = sys.linearize_at(eq_point)
    V, dVdt = sys.check_lyapunov_function(V_expr)

    return {
        "t": t,
        "states": y,
        "jacobian": J,
        "lyapunov_V": V,
        "dVdt": dVdt
    }
