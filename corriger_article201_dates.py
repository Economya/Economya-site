#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-201.html — dates 2025->2026 (oubliées lors de la
correction du taux immobilier ce matin)
À lancer depuis ~/Desktop/mon site

DÉCOUVERTE : c'est la SOURCE du problème de liens croisés répétés sur
article-204/205/206/209/210 — le script de synchronisation fonctionnait
bien, c'est le titre source (article-201) qui n'avait jamais été
corrigé. Après ce script, RELANCER synchroniser_liens_croises.py pour
propager la correction partout.

Idempotent. Sauvegarde en .bak_art201dates.

Usage :
    python3 corriger_article201_dates.py
"""

import os

FICHIER = "article-201.html"

REMPLACEMENTS = [
    (
        "Acheter sa résidence principale : le guide 2025 — Le bon moment pour acheter. Guide complet sur Economya.fr",
        "Acheter sa résidence principale : le guide 2026 — Le bon moment pour acheter. Guide complet sur Economya.fr",
    ),
    (
        "<title>Acheter sa résidence principale : le guide 2025 — Economya.fr</title>",
        "<title>Acheter sa résidence principale : le guide 2026 — Economya.fr</title>",
    ),
    (
        '"headline": "Acheter sa résidence principale : le guide 2025",',
        '"headline": "Acheter sa résidence principale : le guide 2026",',
    ),
    (
        '<meta property="og:title" content="Acheter sa résidence principale : le guide 2025">',
        '<meta property="og:title" content="Acheter sa résidence principale : le guide 2026">',
    ),
    (
        '<meta name="twitter:title" content="Acheter sa résidence principale : le guide 2025">',
        '<meta name="twitter:title" content="Acheter sa résidence principale : le guide 2026">',
    ),
    (
        '"name": "Acheter sa résidence principale : le guide complet 2025", "item": "https://economya.fr/article-201.html"',
        '"name": "Acheter sa résidence principale : le guide complet 2026", "item": "https://economya.fr/article-201.html"',
    ),
    (
        "<h1>Acheter sa résidence principale : le guide complet 2025</h1>",
        "<h1>Acheter sa résidence principale : le guide complet 2026</h1>",
    ),
    (
        "le PTZ 2025 peut financer jusqu'à 50 % du bien dans les zones tendues",
        "le PTZ 2026 peut financer jusqu'à 50 % du bien dans les zones tendues",
    ),
    (
        '<span class="step-tip">PTZ 2025 : élargi aux maisons individuelles dans toutes les zones</span>',
        '<span class="step-tip">PTZ 2026 : élargi aux maisons individuelles dans toutes les zones</span>',
    ),
    (
        "En 2025, les marges de négociation sont réelles : 3 à 8 % selon les marchés.",
        "En 2026, les marges de négociation sont réelles : 3 à 8 % selon les marchés.",
    ),
    (
        "📌 2025 : acheter ou attendre ?",
        "📌 2026 : acheter ou attendre ?",
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

    with open(FICHIER + ".bak_art201dates", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   IMPORTANT: relancer synchroniser_liens_croises.py ensuite")


if __name__ == "__main__":
    main()
