#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-249.html — dates 2025->2026
À lancer depuis ~/Desktop/mon site

Les prix précis des forfaits 5G par opérateur (Free, Prixtel, Auchan
Telecom...) changent par promotions hebdomadaires/mensuelles — sources
consultées datées de janvier, mai, juin 2026 citant déjà des montants
différents. Tenter de fixer un prix exact serait à nouveau obsolète en
quelques semaines. Seules les dates et le cadrage temporel sont corrigés ;
les prix (9,99€/7,99€/6,99€/14,99€) ne sont PAS modifiés (plausibles,
non vérifiables avec confiance dans ce marché très volatil).

Idempotent. Sauvegarde en .bak_art249.

Usage :
    python3 corriger_article249.py
"""

import os

FICHIER = "article-249.html"

REMPLACEMENTS = [
    (
        '"name": "Forfait 5G pas cher : comparatif opérateurs 2025", "item": "https://economya.fr/article-249.html"',
        '"name": "Forfait 5G pas cher : comparatif opérateurs 2026", "item": "https://economya.fr/article-249.html"',
    ),
    (
        "<h1>Forfait 5G pas cher :<br><em>comparatif opérateurs 2025</em></h1>",
        "<h1>Forfait 5G pas cher :<br><em>comparatif opérateurs 2026</em></h1>",
    ),
    (
        "La 5G était réservée aux forfaits premium à 30 € il y a trois ans. En 2025, les opérateurs low-cost cassent les prix : Free, Prixtel, Auchan Telecom… La 5G est accessible dès 6 € par mois. Voici comment choisir sans se tromper.",
        "La 5G était réservée aux forfaits premium à 30 € il y a quelques années. Les opérateurs low-cost cassent désormais les prix : Free, Prixtel, Auchan Telecom… La 5G est accessible dès quelques euros par mois selon les promotions en cours. Voici comment choisir sans se tromper — vérifiez les tarifs actuels sur le site de chaque opérateur, ces offres évoluant très fréquemment.",
    ),
]


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable.")
        return

    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()

    contenu_original = contenu
    nb_modifs = 0

    for ancien, nouveau in REMPLACEMENTS:
        if nouveau in contenu and ancien not in contenu:
            continue
        if ancien in contenu:
            contenu = contenu.replace(ancien, nouveau)
            nb_modifs += 1

    if nb_modifs == 0:
        print("✅ Déjà corrigé ou textes attendus non trouvés.")
        return

    with open(FICHIER + ".bak_art249", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Dates 2026, cadrage temporel ajuste (prix non modifies)")


if __name__ == "__main__":
    main()
