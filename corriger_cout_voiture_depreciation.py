#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction calculateur-cout-voiture.html — taux de dépréciation
légèrement ajusté
À lancer depuis ~/Desktop/mon site

Le taux de 12%/an était dans la fourchette basse du consensus de
marché (sources convergentes : 10-15% par an après la première année,
15-25% en année 1, ~50-60% de perte totale sur 5 ans). Ajusté à 14%
pour mieux refléter une moyenne lissée incluant l'effet de la première
année plus brutale. Ce taux reste par nature variable selon modèle,
marque et kilométrage — aucune "vraie" valeur unique n'existe.

Idempotent. Sauvegarde en .bak_depreciation2026.

Usage :
    python3 corriger_cout_voiture_depreciation.py
"""

import os

FICHIER = "calculateur-cout-voiture.html"

ANCIEN = "const valeurFinale = achat * Math.pow(0.88, duree);"
NOUVEAU = "const valeurFinale = achat * Math.pow(0.86, duree); // Décote ~14%/an (moyenne marché, varie 10-25% selon modèle/marque/km)"


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable.")
        return
    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()
    if NOUVEAU in contenu:
        print("✅ Déjà corrigé.")
        return
    if ANCIEN not in contenu:
        print("⚠️ Texte attendu non trouvé. Aucune modification.")
        return
    with open(FICHIER + ".bak_depreciation2026", 'w', encoding='utf-8') as f:
        f.write(contenu)
    nouveau_contenu = contenu.replace(ANCIEN, NOUVEAU, 1)
    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)
    print("✅ Taux de dépréciation ajusté : 12%/an -> 14%/an (mieux aligné sur le consensus marché)")


if __name__ == "__main__":
    main()
