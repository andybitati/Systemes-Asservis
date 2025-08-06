"""
Ce module contient des fonctions pour exporter les résultats
du projet ControlSysLab vers différents formats :
- CSV pour les données tabulaires
- PDF pour les rapports textuels avec en-tête
- PNG pour les graphiques matplotlib
"""

import csv
import os
import numpy as np
from fpdf import FPDF
from datetime import datetime
import matplotlib.pyplot as plt

def export_to_csv(data, headers, filename="resultat.csv"):
    """
    Exporte proprement une matrice ou un vecteur vers un fichier CSV,
    avec chaque élément dans une colonne différente.

    Args:
        data (list or ndarray): données à exporter (matrice ou vecteur)
        headers (list of str): noms des colonnes
        filename (str): nom du fichier exporté
    """
    # Conversion en tableau numpy si nécessaire
    data = np.array(data)

    # Si vecteur 1D → transformer en matrice colonne (Nx1)
    if data.ndim == 1:
        data = data.reshape(-1, 1)

    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)           # En-tête
        writer.writerows(data.tolist())    # Données ligne par ligne
    print(f"✅ CSV exporté : {filename}")

def export_to_pdf(text, filename="rapport.pdf", title="ControlSysLab - Rapport Global", image_path=None):
    """
    Exporte un rapport avec :
    - Un en-tête (titre, date)
    - Un texte formaté (multi-ligne)
    - Une image insérée à la fin (ex. : graphique PNG)

    Args:
        text (str): contenu du rapport (avec \n pour les sauts de ligne)
        filename (str): nom du fichier PDF à générer
        title (str): titre principal en haut du rapport
        image_path (str): chemin vers une image PNG à insérer (optionnel)
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)

    # Titre centré
    pdf.cell(0, 10, title, ln=True, align="C")

    # Date
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Généré le {datetime.today().strftime('%d/%m/%Y à %Hh%M')}", ln=True, align="C")
    pdf.ln(10)

    # Texte principal
    pdf.set_font("Arial", size=12)
    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line)

    # Image (facultative)
    if image_path:
        if os.path.exists(image_path):
            pdf.ln(10)
            pdf.set_font("Arial", 'I', 11)
            pdf.cell(0, 10, "Figure : Réponse du système PID", ln=True)
            pdf.image(image_path, x=30, w=150)
        else:
            print(f"⚠️ Image non trouvée : {image_path}")

    pdf.output(filename)
    print(f"✅ PDF généré avec image : {filename}")

def save_plot_as_image(fig, filename="graphique.png"):
    """
    Sauvegarde une figure matplotlib au format image (PNG).

    Args:
        fig (matplotlib.figure.Figure): objet figure matplotlib
        filename (str): nom du fichier image de sortie (par défaut "graphique.png")
    """
    fig.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✅ Graphique enregistré : {filename}")
