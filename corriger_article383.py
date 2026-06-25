#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-383.html — inflation et LEP obsolètes, recalcul complet
À lancer depuis ~/Desktop/mon site

Découvertes (sources INSEE/Banque de France, mai 2026) :
1. Inflation en nette remontée en 2026 (2,4% en mai, après 0,3% en
   janvier) — bien au-dessus du "1,5-2%" cité par l'article
2. LEP corrigé à 2,5% (déjà identifié comme obsolète ailleurs sur le site,
   l'article disait 4%)
3. Cascade : l'avantage "taux réel positif" du LEP passe de +2,5 points
   (calcul erroné avec d'anciens taux) à seulement +0,1 point (calcul
   exact avec les taux à jour) — un changement de message, pas qu'un
   chiffre : le LEP bat l'inflation de très peu désormais, pas largement.

Idempotent. Sauvegarde en .bak_art383.

Usage :
    python3 corriger_article383.py
"""

import os

FICHIER = "article-383.html"

REMPLACEMENTS = [
    (
        "Inflation 2025 : s'adapter et protéger son pouvoir d'achat — Vos stratégies anti-inflation. Guide complet sur Economya.fr",
        "Inflation 2026 : s'adapter et protéger son pouvoir d'achat — Vos stratégies anti-inflation. Guide complet sur Economya.fr",
    ),
    (
        "<title>Inflation 2025 : s'adapter et protéger son pouvoir d'achat — Economya.fr</title>",
        "<title>Inflation 2026 : s'adapter et protéger son pouvoir d'achat — Economya.fr</title>",
    ),
    (
        '"headline": "Inflation 2025 : s\'adapter et protéger son pouvoir d\'achat",',
        '"headline": "Inflation 2026 : s\'adapter et protéger son pouvoir d\'achat",',
    ),
    (
        '<meta property="og:title" content="Inflation 2025 : s\'adapter et protéger son pouvoir d\'achat">',
        '<meta property="og:title" content="Inflation 2026 : s\'adapter et protéger son pouvoir d\'achat">',
    ),
    (
        '<meta name="twitter:title" content="Inflation 2025 : s\'adapter et protéger son pouvoir d\'achat">',
        '<meta name="twitter:title" content="Inflation 2026 : s\'adapter et protéger son pouvoir d\'achat">',
    ),
    (
        "<h1>Inflation 2025 :<br><em>s'adapter et protéger son pouvoir d'achat</em></h1>",
        "<h1>Inflation 2026 :<br><em>s'adapter et protéger son pouvoir d'achat</em></h1>",
    ),
    (
        "Après une période d'inflation élevée (2022–2023), l'inflation française se stabilise autour de 1,5–2 % en 2025. Mais l'effet cumulatif des hausses précédentes pèse encore lourdement sur les budgets. Voici les stratégies concrètes pour protéger son pouvoir d'achat dans ce contexte.",
        "Après une période d'inflation élevée (2022–2023) puis un ralentissement en 2024-2025, l'inflation française est repartie à la hausse depuis le printemps 2026, atteignant environ 2,4 % en mai. L'effet cumulatif des hausses précédentes pèse encore lourdement sur les budgets. Voici les stratégies concrètes pour protéger son pouvoir d'achat dans ce contexte.",
    ),
    (
        "Hausse cumulée 2021–2025. Le poste le plus impacté.",
        "Hausse cumulée 2021–2026. Le poste le plus impacté.",
    ),
    (
        '<div class="imp-val">LEP 4 %</div>',
        '<div class="imp-val">LEP 2,5 %</div>',
    ),
    (
        "À 4 % alors que l'inflation est à ~1,5 %, le LEP offre un taux réel positif de ~2,5 %. C'est le seul livret réglementé qui bat vraiment l'inflation en 2025. Vérifiez votre éligibilité sur impots.gouv.fr — 18 millions de Français sont éligibles.",
        "À 2,5 % alors que l'inflation est remontée à ~2,4 % en 2026, le LEP ne bat l'inflation que de très peu désormais (≈0,1 point) — un avantage net réduit par rapport aux années précédentes, mais qui reste le meilleur taux garanti sans risque accessible aux ménages modestes. Vérifiez votre éligibilité sur impots.gouv.fr — 18 millions de Français sont éligibles.",
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

    with open(FICHIER + ".bak_art383", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Inflation 2026 (2,4%), LEP 2,5%, avantage reel recalcule (0,1 pt)")


if __name__ == "__main__":
    main()
