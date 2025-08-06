"""
Ce module contient des fonctions pour exporter les résultats
du projet ControlSysLab vers différents formats :
- CSV pour les données tabulaires
- PDF pour les rapports textuels avec en-tête
- PNG pour les graphiques matplotlib
"""

import csv
import os  # ✅ Pour vérifier l'existence de l’image
from fpdf import FPDF
from datetime import datetime
import matplotlib.pyplot as plt

def export_to_csv(data, headers, filename="resultat.csv"):
    """
    Exporte une liste de listes (ou tableau numpy) vers un fichier CSV.

    Args:
        data (list of list or ndarray): données à exporter, ligne par ligne
        headers (list of str): noms des colonnes
        filename (str): nom du fichier de sortie (par défaut "resultat.csv")
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)      # Écrit l’en-tête
        writer.writerows(data)        # Écrit les lignes de données
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

    # Titre
    pdf.cell(0, 10, title, ln=True, align="C")

    # Date
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Généré le {datetime.today().strftime('%d/%m/%Y à %Hh%M')}", ln=True, align="C")
    pdf.ln(10)

    # Texte principal
    pdf.set_font("Arial", size=12)
    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line)

    # Image (si fournie et existante)
    if image_path:
        if os.path.exists(image_path):
            pdf.ln(10)
            pdf.set_font("Arial", 'I', 11)
            pdf.cell(0, 10, "Figure : Réponse du système PID", ln=True)
            pdf.image(image_path, x=30, w=150)  # largeur en mm
        else:
            print(f"⚠️ Image non trouvée : {image_path}")

    # Sauvegarde finale
    pdf.output(filename)
    print(f"✅ PDF généré avec image : {filename}")

def save_plot_as_image(fig, filename="graphique.png"):
    """
    Sauvegarde une figure matplotlib au format image (PNG).

    Args:
        fig (matplotlib.figure.Figure): objet figure matplotlib
        filename (str): nom du fichier image de sortie (par défaut "graphique.png")
    """
    fig.savefig(filename, dpi=300, bbox_inches='tight')  # Qualité HD
    print(f"✅ Graphique enregistré : {filename}")
