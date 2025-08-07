import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controller.analyze_controller import analyze_system
from controller.state_feedback_controller import compute_state_feedback
from controller.output_feedback_controller import simulate_output_feedback
from controller.nonlinear_controller import analyze_nonlinear_system
from controller.pid_controller import simulate_pid
from export.export_controller import export_to_csv, export_to_pdf, save_plot_as_image
from simulation.poles_controller import plot_poles
from simulation.impulse_controller import plot_impulse_response
from simulation.bode_controller import plot_bode

import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
from control import TransferFunction

def run_all(
    A=None, B=None, C=None, D=None,
    x0=None, xhat0=None, t_span=(0, 10),
    desired_poles=None, observer_poles=None,
    num=None, den=None, Kp=None, Ki=None, Kd=None,
    nonlinear_f=None, nonlinear_x0=None, nonlinear_eq_point=None, V_expr=None
):
    # === Valeurs par défaut pour test local
    if A is None: A = [[0, 1], [-2, -3]]
    if B is None: B = [[0], [1]]
    if C is None: C = [[1, 0]]
    if D is None: D = [[0]]
    if x0 is None: x0 = [1, 0]
    if xhat0 is None: xhat0 = [0, 0]
    if desired_poles is None: desired_poles = [-2, -5]
    if observer_poles is None: observer_poles = [-8, -9]
    if num is None: num = [1]
    if den is None: den = [1, 3, 2]
    if Kp is None: Kp = 2
    if Ki is None: Ki = 1
    if Kd is None: Kd = 0.5
    if nonlinear_f is None:
        x1, x2 = sp.symbols('x1 x2')
        nonlinear_f = [x2, -x1 + (1 - x1**2) * x2]
    if nonlinear_x0 is None: nonlinear_x0 = [1.5, 0]
    if nonlinear_eq_point is None: nonlinear_eq_point = [0, 0]
    if V_expr is None: V_expr = "x1**2 + x2**2"

    # === ANALYSE DU SYSTÈME
    result_analysis = analyze_system(A, B, C, D)
    print("\n=== Analyse du Système ===")
    print("Pôles :", result_analysis["poles"])
    print("Système stable :", "Oui" if result_analysis["is_stable"] else "Non")
    print(result_analysis["summary"])

    # === EXPORTS DES MATRICES
    Wo = result_analysis["Wo"]
    Wc = result_analysis["Wc"]
    headers_wo = [f"Col {i+1}" for i in range(Wo.shape[1])]
    headers_wc = [f"Col {i+1}" for i in range(Wc.shape[1])]
    export_to_csv(Wo.tolist(), headers_wo, filename="observabilite.csv")
    export_to_csv(Wc.tolist(), headers_wc, filename="controlabilite.csv")
    export_to_pdf(result_analysis["summary"], filename="analyse.pdf")

    # === COMMANDE PAR ÉTAT
    feedback_result = compute_state_feedback(A, B, desired_poles, x0, t_span)
    print("\n=== Commande État ===")
    print("Gain K :", feedback_result["K"])
    print("Temps (boucle fermée) :", feedback_result["t_closed"][:5], "...")
    print("Sortie (boucle fermée) :", feedback_result["y_closed"][:, :5], "...")

    # === OBSERVATEUR
    K = [[5, 6]]  # valeur fixe pour l’instant
    observer_result = simulate_output_feedback(A, B, C, K, observer_poles, x0, xhat0, t_span)
    print("\n=== Commande Observateur ===")
    print("Gain observateur L :", observer_result["L"])
    print("Temps :", observer_result["t"][:5], "...")
    print("État estimé (x̂) :", observer_result["x_hat"][:, :5], "...")

    # === NON LINÉAIRE
    nonlinear_result = analyze_nonlinear_system(
        [sp.symbols('x1'), sp.symbols('x2')],
        nonlinear_f, nonlinear_x0, t_span, nonlinear_eq_point, V_expr
    )
    print("\n=== Système Non Linéaire ===")
    print("Jacobienne :", nonlinear_result["jacobian"])
    print("dV/dt =", nonlinear_result["dVdt"])

    # === PID
    pid_result = simulate_pid(num, den, Kp, Ki, Kd)
    print("\n=== Régulateur PID ===")
    print("Tracking Error (t<5) :", pid_result["err"][:5])
    print("Bode Phase (t<5) :", pid_result["phase"][:5])

    # === SAUVEGARDE DES COURBES
    fig_pid, ax_pid = plt.subplots()
    ax_pid.plot(pid_result["t"], pid_result["y"])
    ax_pid.set_title("Réponse du système PID")
    ax_pid.set_xlabel("Temps (s)")
    ax_pid.set_ylabel("Sortie")
    ax_pid.grid(True)
    save_plot_as_image(fig_pid, filename="pid_response.png")
    plt.close(fig_pid)

    # Autres images (avec save_path)
    plot_poles(pid_result["poles"], save_path="poles_plot.png")
    plot_impulse_response(pid_result["system_open_loop"], save_path="impulse_plot.png")
    plot_bode(pid_result["system_open_loop"], save_path="bode_plot.png")

    # === RAPPORT FINAL
    rapport = "RAPPORT COMPLET - ControlSysLab\n\n"
    rapport += "=== MATRICES D'ENTRÉE ===\n"
    rapport += f"A = \n{np.array(A)}\n"
    rapport += f"B = \n{np.array(B)}\n"
    rapport += f"C = \n{np.array(C)}\n"
    rapport += f"D = \n{np.array(D)}\n\n"
    rapport += "=== CONTRÔLABILITÉ ===\nWc = \n" + str(Wc) + "\n\n"
    rapport += "=== OBSERVABILITÉ ===\nWo = \n" + str(Wo) + "\n\n"
    rapport += "=== PID ===\n"
    rapport += f"Kp = {Kp}, Ki = {Ki}, Kd = {Kd}\n"
    rapport += f"Erreur (5 premiers) : {pid_result['err'][:5]}\n\n"
    rapport += "Fonction de transfert (boucle ouverte) :\n"
    rapport += str(pid_result["system_open_loop"]) + "\n\n"

    # Génération du PDF complet avec toutes les figures
    export_to_pdf(
        text=rapport,
        filename="rapport_complet.pdf",
        title="ControlSysLab - Rapport Complet avec Figures",
        image_paths=[
            "pid_response.png",
            "poles_plot.png",
            "impulse_plot.png",
            "bode_plot.png"
        ]
    )

    print("\n✅ Rapport complet généré avec images incluses.")

if __name__ == "__main__":
    run_all()
