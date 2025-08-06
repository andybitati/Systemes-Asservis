# controller/export_controller.py

"""
Ce module contient des fonctions pour exporter les résultats
du projet ControlSysLab vers différents formats :
- CSV pour les données tabulaires
- PDF pour les rapports textuels
- PNG pour les graphiques matplotlib
"""

import csv
from fpdf import FPDF
import matplotlib.pyplot as plt

def export_to_csv(data, headers, filename="resultat.csv"):
    """
    Exporte un tableau de données (liste de listes ou numpy array) vers un fichier CSV.

    Args:
        data (list of list or ndarray): données à exporter, ligne par ligne
        headers (list of str): noms des colonnes
        filename (str): nom du fichier de sortie (par défaut "resultat.csv")
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)      # Écrit l’en-tête
        writer.writerows(data)        # Écrit toutes les lignes de données
    print(f"✅ CSV exporté : {filename}")

def export_to_pdf(text, filename="rapport.pdf"):
    """
    Exporte un texte brut dans un fichier PDF A4 (police Arial 12pt).

    Args:
        text (str): texte à exporter (avec sauts de ligne \n)
        filename (str): nom du fichier PDF généré (par défaut "rapport.pdf")
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Découpe le texte ligne par ligne et l’écrit proprement dans le PDF
    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line)

    pdf.output(filename)
    print(f"✅ PDF généré : {filename}")

def save_plot_as_image(fig, filename="graphique.png"):
    """
    Sauvegarde une figure matplotlib au format image (PNG).

    Args:
        fig (matplotlib.figure.Figure): objet figure matplotlib
        filename (str): nom du fichier image de sortie (par défaut "graphique.png")
    """
    fig.savefig(filename, dpi=300, bbox_inches='tight')  # Qualité HD
    print(f"✅ Graphique enregistré : {filename}")
