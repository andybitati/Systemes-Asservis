import numpy as np
import control as ctrl
from scipy import signal
import matplotlib.pyplot as plt  # facultatif pour affichage des courbes

class PIDModel:
    def __init__(self, num, den):
        """
        Initialise le système à partir de la fonction de transfert (numérateur, dénominateur)
        """
        self.sys = ctrl.TransferFunction(num, den)

    def set_pid_gains(self, Kp, Ki, Kd):
        """
        Crée le régulateur PID : Kp + Ki/s + Kd*s
        """
        s = ctrl.TransferFunction.s
        self.pid = Kp + Ki / s + Kd * s
        return self.pid

    def closed_loop_response(self):
        """
        Calcule la réponse en boucle fermée avec le PID actuel
        """
        if not hasattr(self, 'pid'):
            raise ValueError("PID non défini. Utiliser set_pid_gains().")
        closed_loop = ctrl.feedback(self.pid * self.sys, 1)
        t, y = ctrl.step_response(closed_loop)
        return t, y

    def compute_tracking_error(self):
        """
        Calcule l’erreur de suivi : différence entre consigne (1) et sortie
        """
        t, y = self.closed_loop_response()
        e = 1 - y
        return t, e

    def bode_plot_data(self):
        """Retourne les données pour tracer le diagramme de Bode sans erreur.

        On utilise `control.freqresp()` au lieu de `control.bode()` pour éviter tout conflit
        avec Matplotlib (pas d'erreur liée à Plot).
        """
        if not hasattr(self, 'pid'):
            raise ValueError("PID non défini.")

        system_open_loop = self.pid * self.sys

        # Fréquence personnalisée de 0.01 à 100 rad/s (échelle log)
        omega = np.logspace(-2, 2, 1000)

        # Calcul de la réponse fréquentielle complexe H(jω)
        H = ctrl.freqresp(system_open_loop, omega)

        # Calcul magnitude et phase à partir de H(jω)
        mag = np.abs(H)
        phase = np.angle(H)

        return omega, mag, phase


    def nyquist_plot_data(self):
        """
        Retourne les données pour tracer le diagramme de Nyquist
        """
        if not hasattr(self, 'pid'):
            raise ValueError("PID non défini.")
        real, imag, freq = ctrl.nyquist(self.pid * self.sys, Plot=False)
        return real, imag

    def ziegler_nichols_gains(self, Ku, Tu):
        """
        Méthode classique de Ziegler-Nichols pour un système de type 1
        Paramètres :
            Ku : gain critique
            Tu : période d'oscillation critique
        Retourne :
            Kp, Ki, Kd selon Ziegler-Nichols (régulation)
        """
        Kp = 0.6 * Ku
        Ki = 2 * Kp / Tu
        Kd = Kp * Tu / 8
        return Kp, Ki, Kd
