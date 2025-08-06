import numpy as np
import control as ctrl
from scipy import signal

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
        """
        Retourne les données pour tracer le diagramme de Bode
        """
        if not hasattr(self, 'pid'):
            raise ValueError("PID non défini.")
        system_open_loop = self.pid * self.sys
        mag, phase, omega = ctrl.bode(system_open_loop, Plot=False)
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
