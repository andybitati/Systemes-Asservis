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
    data = np.array(data)
    if data.ndim == 1:
        data = data.reshape(-1, 1)

    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data.tolist())

    print(f"✅ CSV exporté : {filename}")

def export_to_pdf(text, filename="rapport.pdf", title="ControlSysLab - Rapport Global", image_paths=None):
    """
    Génère un rapport PDF avec :
    - Titre principal + date
    - Contenu du rapport (texte multi-lignes)
    - Toutes les images générées automatiquement insérées à la fin

    Args:
        text (str): contenu principal du rapport
        filename (str): nom du fichier PDF à créer
        title (str): titre principal du document
        image_paths (list[str] ou None): chemins vers les images PNG à insérer
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, title, ln=True, align="C")

    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Généré le {datetime.today().strftime('%d/%m/%Y à %Hh%M')}", ln=True, align="C")
    pdf.ln(10)

    # Texte du rapport
    pdf.set_font("Arial", size=12)
    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line)

    # Insertion des images (toutes celles spécifiées)
    if image_paths:
        for img_path in image_paths:
            if os.path.exists(img_path):
                pdf.add_page()
                pdf.set_font("Arial", 'I', 11)
                pdf.cell(0, 10, f"Figure : {os.path.basename(img_path)}", ln=True)
                pdf.image(img_path, x=30, w=150)
            else:
                print(f"⚠️ Image non trouvée : {img_path}")

    pdf.output(filename)
    print(f"✅ PDF généré avec toutes les images : {filename}")

def save_plot_as_image(fig, filename="graphique.png"):
    """
    Sauvegarde une figure matplotlib au format image (PNG).

    Args:
        fig (matplotlib.figure.Figure): figure matplotlib à enregistrer
        filename (str): nom du fichier image à générer
    """
    fig.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✅ Graphique enregistré : {filename}")
