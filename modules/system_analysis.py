import numpy as np
from scipy.signal import ss2tf, impulse, step, bode
from numpy.linalg import eigvals
import matplotlib.pyplot as plt
from control import ss

class StateSpaceSystem:
    def __init__(self, A, B, C, D):
        """
        Système d'espace d'état linéaire
        Args:
            A: Matrice d'état (n x n)
            B: Matrice d'entrée (n x m)
            C: Matrice de sortie (p x n)
            D: Matrice de transmission directe (p x m)
        """
        self.A = np.array(A, dtype=float)
        self.B = np.array(B, dtype=float)
        self.C = np.array(C, dtype=float)
        self.D = np.array(D, dtype=float)
        self._validate_matrices()
        self.system = ss(self.A, self.B, self.C, self.D)

    def _validate_matrices(self):
        """Valide les dimensions des matrices"""
        n, m = self.A.shape[0], self.B.shape[1]
        p = self.C.shape[0]
        
        assert self.A.shape == (n, n), "Matrice A doit être carrée"
        assert self.B.shape == (n, m), "Dimensions B incompatibles avec A"
        assert self.C.shape == (p, n), "Dimensions C incompatibles avec A"
        assert self.D.shape == (p, m), "Dimensions D incompatibles avec B/C"

    def get_poles(self):
        """Retourne les pôles du système (valeurs propres de A)."""
        return eigvals(self.A)

    def is_stable(self, tol=1e-6):
        """
        Teste la stabilité asymptotique
        Args:
            tol: Tolérance pour les parties réelles nulles
        Returns:
            bool: True si tous les pôles ont partie réelle < -tol
        """
        poles = self.get_poles()
        return np.all(np.real(poles) < -tol)

    def impulse_response(self, T=None):
        """Calcule la réponse impulsionnelle."""
        T, y = impulse(self.system, T=T)
        return T, y

    def step_response(self, T=None):
        """Calcule la réponse à l'échelon."""
        T, y = step(self.system, T=T)
        return T, y

    def bode_plot(self, omega=None):
        """Génère les données pour un diagramme de Bode."""
        mag, phase, omega = bode(self.system, omega=omega, Plot=True)
        return omega, mag, phase

    def plot_response(self, T, y, title="Réponse temporelle", ylabel="Sortie"):
        """Affiche une courbe de réponse temporelle."""
        plt.figure(figsize=(8, 4))
        plt.plot(T, y)
        plt.title(title)
        plt.xlabel("Temps (s)")
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_bode(self):
        """Affiche le diagramme de Bode."""
        omega, mag, phase = self.bode_plot()
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
        
        ax1.semilogx(omega, 20 * np.log10(mag))
        ax1.set_title("Diagramme de Bode - Gain")
        ax1.set_ylabel("Magnitude (dB)")
        ax1.grid(True)

        ax2.semilogx(omega, phase * 180 / np.pi)
        ax2.set_title("Diagramme de Bode - Phase")
        ax2.set_ylabel("Phase (deg)")
        ax2.set_xlabel("Fréquence (rad/s)")
        ax2.grid(True)

        plt.tight_layout()
        plt.show()