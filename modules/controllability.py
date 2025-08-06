import numpy as np

class ControlObservabilityAnalyzer:
    def __init__(self, A, B, C):
        self.A = np.array(A, dtype=float)
        self.B = np.array(B, dtype=float)
        self.C = np.array(C, dtype=float)

        self.n = self.A.shape[0]

    def controllability_matrix(self):
        """
        Génère la matrice de contrôlabilité Wc = [B, AB, A²B, ..., A^{n-1}B]
        """
        Wc = self.B
        for i in range(1, self.n):
            Wc = np.hstack((Wc, np.linalg.matrix_power(self.A, i) @ self.B))
        return Wc

    def observability_matrix(self):
        """
        Génère la matrice d'observabilité Wo = [C^T, (CA)^T, (CA^2)^T, ..., (CA^{n-1})^T]^T
        """
        Wo = self.C
        for i in range(1, self.n):
            Wo = np.vstack((Wo, self.C @ np.linalg.matrix_power(self.A, i)))
        return Wo

    def is_controllable(self):
        """
        Renvoie 'True' si le rang de Wc est égal à n
        """
        Wc = self.controllability_matrix()
        return np.linalg.matrix_rank(Wc) == self.n

    def is_observable(self):
        """
        Renvoie True si le rang de Wo est égal à n
        """
        Wo = self.observability_matrix()
        return np.linalg.matrix_rank(Wo) == self.n

    def summary(self):
        """
        Donne un résumé texte des verdicts de contrôlabilité et observabilité
        """
        verdict = ""
        verdict += f"Rang de Wc : {np.linalg.matrix_rank(self.controllability_matrix())} "
        verdict += f"=> {'Contrôlable' if self.is_controllable() else 'Non contrôlable'}\n"
        verdict += f"Rang de Wo : {np.linalg.matrix_rank(self.observability_matrix())} "
        verdict += f"=> {'Observable' if self.is_observable() else 'Non observable'}"
        return verdict
