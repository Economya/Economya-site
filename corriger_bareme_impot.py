#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction du barème de l'impôt sur le revenu dans calculateur-impot.html
À lancer UNE SEULE FOIS depuis le dossier ~/Desktop/mon site

Met à jour les seuils de tranches avec le barème officiel 2026 (revenus 2025),
issu de la loi de finances 2026 (revalorisation +0,9%).

Source vérifiée : service-public.gouv.fr, economie.gouv.fr (juin 2026)

Sans danger à relancer (idempotent). Sauvegarde en .bak_bareme avant modification.

Usage :
    python3 corriger_bareme_impot.py
"""

import os

FICHIER = "calculateur-impot.html"

ANCIEN_BAREME = '''const BAREME = [
  { min: 0,      max: 11497,  taux: 0,    label: "Jusqu'à 11 497 €" },
  { min: 11497,  max: 29315,  taux: 0.11, label: "11 497 € à 29 315 €" },
  { min: 29315,  max: 83823,  taux: 0.30, label: "29 315 € à 83 823 €" },
  { min: 83823,  max: 180294, taux: 0.41, label: "83 823 € à 180 294 €" },
  { min: 180294, max: Infinity,taux: 0.45, label: "Au-delà de 180 294 €" },
];'''

NOUVEAU_BAREME = '''const BAREME = [
  { min: 0,      max: 11600,  taux: 0,    label: "Jusqu'à 11 600 €" },
  { min: 11600,  max: 29579,  taux: 0.11, label: "11 600 € à 29 579 €" },
  { min: 29579,  max: 84577,  taux: 0.30, label: "29 579 € à 84 577 €" },
  { min: 84577,  max: 181917, taux: 0.41, label: "84 577 € à 181 917 €" },
  { min: 181917, max: Infinity,taux: 0.45, label: "Au-delà de 181 917 €" },
];'''


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable dans ce dossier.")
        return

    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()

    if "11600" in contenu and "29579" in contenu:
        print("✅ Déjà corrigé — barème à jour.")
        return

    if ANCIEN_BAREME not in contenu:
        print("⚠️  Le bloc de barème attendu n'a pas été trouvé tel quel.")
        print("   Aucune modification effectuée, pour éviter une erreur.")
        print("   Vérifie manuellement le contenu du fichier.")
        return

    with open(FICHIER + ".bak_bareme", 'w', encoding='utf-8') as f:
        f.write(contenu)

    nouveau_contenu = contenu.replace(ANCIEN_BAREME, NOUVEAU_BAREME, 1)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)

    print("✅ Barème de l'impôt corrigé avec les seuils officiels 2026 (revenus 2025).")
    print(f"   Sauvegarde créée : {FICHIER}.bak_bareme")


if __name__ == "__main__":
    main()
