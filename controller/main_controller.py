# main.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


"""
Ce fichier est le point d’entrée du projet ControlSysLab.
Il montre comment utiliser les contrôleurs en appelant chaque module
avec des paramètres fournis par l'utilisateur (ou codés ici pour test).
"""

# === IMPORTATION DES MODULES DE CONTRÔLE ===
from controller.analyze_controller import analyze_system
from controller.state_feedback_controller import compute_state_feedback
from controller.output_feedback_controller import simulate_output_feedback
from controller.nonlinear_controller import analyze_nonlinear_system
from controller.pid_controller import simulate_pid
from controller.export_controller import export_to_csv, export_to_pdf
from controller.export_controller import save_plot_as_image


import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

def run_all():
    # === EXEMPLE DE DONNÉES (à remplacer par les inputs utilisateurs plus tard) ===
    A = [[0, 1], [-2, -3]]
    B = [[0], [1]]
    C = [[1, 0]]
    D = [[0]]

    # === MODULE 1 & 2 : Analyse système, stabilité, contrôlabilité, observabilité ===
    result_analysis = analyze_system(A, B, C, D)

    print("\n=== Analyse du Système ===")
    print("Pôles :", result_analysis["poles"])
    print("Système stable :", "Oui" if result_analysis["is_stable"] else "Non")
    print(result_analysis["summary"])


    # === EXPORT CSV : Matrice d'observabilité ===
    Wo = result_analysis["Wo"]
    headers = [f"Col {i+1}" for i in range(Wo.shape[1])]  # noms des colonnes
    export_to_csv(Wo.tolist(), headers, filename="observabilite.csv")

    # === EXPORT CSV : Matrice de contrôlabilité ===
    Wc = result_analysis["Wc"]
    headers_wc = [f"Col {i+1}" for i in range(Wc.shape[1])]
    export_to_csv(Wc.tolist(), headers_wc, filename="controlabilite.csv")

    # === EXPORT PDF : Résumé de l'analyse ===
    summary_text = result_analysis["summary"]
    export_to_pdf(summary_text, filename="analyse.pdf")



    # === MODULE 3 : Commande par retour d'état (feedback d’état) ===
    x0 = [1, 0]               # Condition initiale
    t_span = (0, 10)          # Intervalle de simulation
    desired_poles = [-2, -5]  # Pôles en boucle fermée

    feedback_result = compute_state_feedback(A, B, desired_poles, x0, t_span)

    print("\n=== Commande État ===")
    print("Gain K :", feedback_result["K"])
    print("Temps (boucle fermée) :", feedback_result["t_closed"][:5], "...")
    print("Sortie (boucle fermée) :", feedback_result["y_closed"][:, :5], "...")

    # === MODULE 4 : Commande par observateur (output feedback) ===
    K = [[5, 6]]
    observer_poles = [-8, -9]
    xhat0 = [0, 0]

    observer_result = simulate_output_feedback(A, B, C, K, observer_poles, x0, xhat0, t_span)

    print("\n=== Commande Observateur ===")
    print("Gain observateur L :", observer_result["L"])
    print("Temps :", observer_result["t"][:5], "...")
    print("État estimé (x̂) :", observer_result["x_hat"][:, :5], "...")

    # === MODULE 5 : Analyse d’un système non linéaire ===
    x1, x2 = sp.symbols('x1 x2')
    f = [x2, -x1 + (1 - x1**2) * x2]          # Équation de Van der Pol
    x0_nl = [1.5, 0]                          # État initial
    eq_point = [0, 0]                         # Point d'équilibre
    V_expr = "x1**2 + x2**2"                  # Candidate fonction de Lyapunov

    nonlinear_result = analyze_nonlinear_system([x1, x2], f, x0_nl, (0, 20), eq_point, V_expr)

    print("\n=== Système Non Linéaire ===")
    print("Jacobienne :", nonlinear_result["jacobian"])
    print("dV/dt =", nonlinear_result["dVdt"])

    # === MODULE 6 : PID avec système à fonction de transfert ===
    num = [1]
    den = [1, 3, 2]
    Kp, Ki, Kd = 2, 1, 0.5

    pid_result = simulate_pid(num, den, Kp, Ki, Kd)

    print("\n=== Régulateur PID ===")
    print("Tracking Error (t<5) :", pid_result["err"][:5])
    print("Bode Phase (t<5) :", pid_result["phase"][:5])

    # === EXPORT IMAGE : Courbe de réponse du système PID

    fig, ax = plt.subplots()
    t_pid = pid_result["t"]
    y_pid = pid_result["y"]
    ax.plot(t_pid, y_pid)
    ax.set_title("Réponse du système PID")
    ax.set_xlabel("Temps (s)")
    ax.set_ylabel("Sortie")
    ax.grid(True)

    save_plot_as_image(fig, filename="pid_response.png")
    plt.close(fig)  # Important pour libérer la mémoire

    rapport = "RAPPORT COMPLET - ControlSysLab\n\n"

    # Matrices d'entrée
    rapport += "=== MATRICES D'ENTRÉE ===\n"
    rapport += f"A = \n{np.array(A)}\n"
    rapport += f"B = \n{np.array(B)}\n"
    rapport += f"C = \n{np.array(C)}\n"
    rapport += f"D = \n{np.array(D)}\n\n"

    # Matrices de contrôlabilité / observabilité
    rapport += "=== CONTRÔLABILITÉ ===\n"
    rapport += f"Wc = \n{Wc}\n\n"

    rapport += "=== OBSERVABILITÉ ===\n"
    rapport += f"Wo = \n{Wo}\n\n"

    # PID
    rapport += "=== PID ===\n"
    rapport += f"Kp = {Kp}, Ki = {Ki}, Kd = {Kd}\n"
    rapport += f"Erreur (5 premiers) : {pid_result['err'][:5]}\n"

    # Génération du PDF complet avec image incluse
    export_to_pdf(
        text=rapport,
        filename="rapport_complet.pdf",
        image_path="pid_response.png",  # générée juste avant
        title="ControlSysLab - Rapport complet avec graphe"
    )


