#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-34.html — prix Game Pass Ultimate obsolète + dates
À lancer depuis ~/Desktop/mon site

Saga de prix confirmée par très nombreuses sources convergentes :
Game Pass Ultimate 17,99€ -> 26,99€ (octobre 2025, +50%) -> 20,99€/mois
(avril 2026, après une fronde massive des abonnés). Le "9,99€/mois" de
l'article est largement obsolète, bien en dessous même de l'ancien prix.

⚠️ Les figures du tableau comparatif (lignes 286/292/298/310/316) ne sont
PAS modifiées par prudence — sans visibilité sur les en-têtes exacts du
tableau, impossible d'identifier avec certitude quel service correspond
à quel prix. À vérifier manuellement si besoin.

Idempotent. Sauvegarde en .bak_art34.

Usage :
    python3 corriger_article34.py
"""

import os

FICHIER = "article-34.html"

REMPLACEMENTS = [
    (
        "<title>Jouer aux jeux vidéo sans se ruiner en 2025 — Economya.fr</title>",
        "<title>Jouer aux jeux vidéo sans se ruiner en 2026 — Economya.fr</title>",
    ),
    (
        '"headline": "Jouer aux jeux vidéo sans se ruiner en 2025",',
        '"headline": "Jouer aux jeux vidéo sans se ruiner en 2026",',
    ),
    (
        '<meta property="og:title" content="Jouer aux jeux vidéo sans se ruiner en 2025">',
        '<meta property="og:title" content="Jouer aux jeux vidéo sans se ruiner en 2026">',
    ),
    (
        '<meta name="twitter:title" content="Jouer aux jeux vidéo sans se ruiner en 2025">',
        '<meta name="twitter:title" content="Jouer aux jeux vidéo sans se ruiner en 2026">',
    ),
    (
        '<meta name="description" content="Jouer aux jeux vidéo sans se ruiner en 2025 — Economya.fr" />',
        '<meta name="description" content="Jouer aux jeux vidéo sans se ruiner en 2026 — Economya.fr" />',
    ),
    (
        "<h1>Jouer aux jeux vidéo <em>sans se ruiner</em> en 2025</h1>",
        "<h1>Jouer aux jeux vidéo <em>sans se ruiner</em> en 2026</h1>",
    ),
    (
        "Game Pass (Xbox/PC), PlayStation Plus et Apple Arcade proposent des centaines de jeux pour un abonnement mensuel de 10 à 15€. Le Game Pass Ultimate inclut des jeux day one dès leur sortie, du cloud gaming et EA Play — c'est objectivement la meilleure offre du marché. Pour quelqu'un qui joue régulièrement, un abonnement remplace avantageusement l'achat de 2 à 3 jeux par an.",
        "Game Pass (Xbox/PC), PlayStation Plus et Apple Arcade proposent des centaines de jeux pour un abonnement mensuel. Le Game Pass Ultimate (20,99€/mois, après une forte hausse suivie d'un retour en arrière partiel en 2025-2026) inclut des jeux day one dès leur sortie, du cloud gaming et EA Play — c'est objectivement la meilleure offre du marché malgré son coût en hausse. Pour quelqu'un qui joue régulièrement, un abonnement remplace avantageusement l'achat de 2 à 3 jeux par an.",
    ),
    (
        '<div class="strategie-gain">Dès 9,99€/mois</div>',
        '<div class="strategie-gain">Dès 12,99€/mois (PC Game Pass)</div>',
    ),
    (
        "Comparatif des abonnements gaming en 2025",
        "Comparatif des abonnements gaming en 2026",
    ),
    (
        "Les meilleurs jeux gratuits en 2025",
        "Les meilleurs jeux gratuits en 2026",
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

    with open(FICHIER + ".bak_art34", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Game Pass Ultimate 20,99e mentionne, dates 2026")
    print("   Tableau comparatif NON modifie (structure exacte incertaine)")


if __name__ == "__main__":
    main()
