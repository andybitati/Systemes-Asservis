import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# === IMPORTATION DES MODULES DE CONTRÔLE ===
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

def run_all():
    # === MATRICES DE BASE ===
    A = [[0, 1], [-2, -3]]
    B = [[0], [1]]
    C = [[1, 0]]
    D = [[0]]

    # === ANALYSE DU SYSTÈME ===
    result_analysis = analyze_system(A, B, C, D)
    print("\n=== Analyse du Système ===")
    print("Pôles :", result_analysis["poles"])
    print("Système stable :", "Oui" if result_analysis["is_stable"] else "Non")
    print(result_analysis["summary"])

    # === EXPORT CSV : Observabilité / Contrôlabilité ===
    Wo = result_analysis["Wo"]
    Wc = result_analysis["Wc"]
    headers_wo = [f"Col {i+1}" for i in range(Wo.shape[1])]
    headers_wc = [f"Col {i+1}" for i in range(Wc.shape[1])]
    export_to_csv(Wo.tolist(), headers_wo, filename="observabilite.csv")
    export_to_csv(Wc.tolist(), headers_wc, filename="controlabilite.csv")

    # === EXPORT PDF : Résumé simple
    export_to_pdf(result_analysis["summary"], filename="analyse.pdf")

    # === COMMANDE ÉTAT ===
    x0 = [1, 0]
    t_span = (0, 10)
    desired_poles = [-2, -5]
    feedback_result = compute_state_feedback(A, B, desired_poles, x0, t_span)
    print("\n=== Commande État ===")
    print("Gain K :", feedback_result["K"])
    print("Temps (boucle fermée) :", feedback_result["t_closed"][:5], "...")
    print("Sortie (boucle fermée) :", feedback_result["y_closed"][:, :5], "...")

    # === OBSERVATEUR ===
    K = [[5, 6]]
    observer_poles = [-8, -9]
    xhat0 = [0, 0]
    observer_result = simulate_output_feedback(A, B, C, K, observer_poles, x0, xhat0, t_span)
    print("\n=== Commande Observateur ===")
    print("Gain observateur L :", observer_result["L"])
    print("Temps :", observer_result["t"][:5], "...")
    print("État estimé (x̂) :", observer_result["x_hat"][:, :5], "...")

    # === SYSTÈME NON LINÉAIRE ===
    x1, x2 = sp.symbols('x1 x2')
    f = [x2, -x1 + (1 - x1**2) * x2]
    x0_nl = [1.5, 0]
    eq_point = [0, 0]
    V_expr = "x1**2 + x2**2"
    nonlinear_result = analyze_nonlinear_system([x1, x2], f, x0_nl, (0, 20), eq_point, V_expr)
    print("\n=== Système Non Linéaire ===")
    print("Jacobienne :", nonlinear_result["jacobian"])
    print("dV/dt =", nonlinear_result["dVdt"])

    # === PID CONTROL ===
    num = [1]
    den = [1, 3, 2]
    Kp, Ki, Kd = 2, 1, 0.5
    pid_result = simulate_pid(num, den, Kp, Ki, Kd)
    print("\n=== Régulateur PID ===")
    print("Tracking Error (t<5) :", pid_result["err"][:5])
    print("Bode Phase (t<5) :", pid_result["phase"][:5])

    # === EXPORT IMAGE : Courbe PID
    fig, ax = plt.subplots()
    t_pid = pid_result["t"]
    y_pid = pid_result["y"]
    ax.plot(t_pid, y_pid)
    ax.set_title("Réponse du système PID")
    ax.set_xlabel("Temps (s)")
    ax.set_ylabel("Sortie")
    ax.grid(True)
    save_plot_as_image(fig, filename="pid_response.png")
    plt.close(fig)

    # === RAPPORT GLOBAL PDF
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

    export_to_pdf(rapport, filename="rapport_complet.pdf", image_path="pid_response.png")

    # === AFFICHAGES FINAUX ===
    print("\n=== AFFICHAGES ===")
    print("→ Pôles")
    plot_poles(pid_result["poles"])

    print("→ Réponse impulsionnelle")
    plot_impulse_response(pid_result["system_open_loop"])

    print("→ Diagramme de Bode")
    plot_bode(pid_result["system_open_loop"])


