#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-433.html — plafond PER obsolète (répétition) + dates
À lancer depuis ~/Desktop/mon site

Même erreur que déjà corrigée une fois aujourd'hui (article-431) : le
plafond PER cité ("32 909€", donnée ~2021) est obsolète. Plafond 2026
confirmé : 37 680€ pour un salarié.

Idempotent. Sauvegarde en .bak_art433.

Usage :
    python3 corriger_article433.py
"""

import os

FICHIER = "article-433.html"

REMPLACEMENTS = [
    (
        "Déclaration de revenus 2025 : cases méconnues — Cases que personne ne coche. Guide complet sur Economya.fr",
        "Déclaration de revenus 2026 : cases méconnues — Cases que personne ne coche. Guide complet sur Economya.fr",
    ),
    (
        "<title>Déclaration de revenus 2025 : cases méconnues — Economya.fr</title>",
        "<title>Déclaration de revenus 2026 : cases méconnues — Economya.fr</title>",
    ),
    (
        '"headline": "Déclaration de revenus 2025 : cases méconnues",',
        '"headline": "Déclaration de revenus 2026 : cases méconnues",',
    ),
    (
        '<meta property="og:title" content="Déclaration de revenus 2025 : cases méconnues">',
        '<meta property="og:title" content="Déclaration de revenus 2026 : cases méconnues">',
    ),
    (
        '<meta name="twitter:title" content="Déclaration de revenus 2025 : cases méconnues">',
        '<meta name="twitter:title" content="Déclaration de revenus 2026 : cases méconnues">',
    ),
    (
        "<h1>Déclaration de revenus 2025 :<br><em>cases méconnues</em></h1>",
        "<h1>Déclaration de revenus 2026 :<br><em>cases méconnues</em></h1>",
    ),
    (
        "📋 Les cases méconnues à ne pas oublier en 2025",
        "📋 Les cases méconnues à ne pas oublier en 2026",
    ),
    (
        "Les versements volontaires sur un PER individuel sont déductibles du revenu imposable. Plafond 2025 : 10 % du revenu professionnel net de l'année précédente (max environ 32 909 €). La déduction est au taux marginal d'imposition — particulièrement avantageuse pour les TMI 30 % et 41 %.",
        "Les versements volontaires sur un PER individuel sont déductibles du revenu imposable. Plafond 2026 : 10 % du revenu professionnel net de l'année précédente (max 37 680 € pour un salarié). La déduction est au taux marginal d'imposition — particulièrement avantageuse pour les TMI 30 % et 41 %.",
    ),
    (
        '<span class="ctag g">Déduction au TMI</span><span class="ctag">Plafond ~32 000 €</span>',
        '<span class="ctag g">Déduction au TMI</span><span class="ctag">Plafond ~37 680 €</span>',
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

    with open(FICHIER + ".bak_art433", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Plafond PER 32909e->37680e (repetition corrigee), dates 2026")


if __name__ == "__main__":
    main()
