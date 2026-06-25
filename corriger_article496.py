#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-496.html — PEA prélèvements sociaux obsolètes + dates
À lancer depuis ~/Desktop/mon site

Le PEA n'est pas exempté de la hausse de CSG 2026 (contrairement à
l'assurance-vie/PEL) — son taux de prélèvements sociaux est passé à
18,6% (au lieu de 17,2%), confirmé plus tôt dans la session.

Les rendements précis par action (TotalEnergies, BNP Paribas, etc.) ne
sont PAS modifiés — données de marché fluctuant quotidiennement, hors
périmètre vérifiable individuellement dans cette session.

Idempotent. Sauvegarde en .bak_art496.

Usage :
    python3 corriger_article496.py
"""

import os

FICHIER = "article-496.html"

REMPLACEMENTS = [
    (
        "Actions françaises à dividende : sélection 2025 — 5 à 8% de rendement annuel. Guide complet sur Economya.fr",
        "Actions françaises à dividende : sélection 2026 — 5 à 8% de rendement annuel. Guide complet sur Economya.fr",
    ),
    (
        "<title>Actions françaises à dividende : sélection 2025 — Economya.fr</title>",
        "<title>Actions françaises à dividende : sélection 2026 — Economya.fr</title>",
    ),
    (
        '"headline": "Actions françaises à dividende : sélection 2025",',
        '"headline": "Actions françaises à dividende : sélection 2026",',
    ),
    (
        '<meta property="og:title" content="Actions françaises à dividende : sélection 2025">',
        '<meta property="og:title" content="Actions françaises à dividende : sélection 2026">',
    ),
    (
        '<meta name="twitter:title" content="Actions françaises à dividende : sélection 2025">',
        '<meta name="twitter:title" content="Actions françaises à dividende : sélection 2026">',
    ),
    (
        "<h1>Actions françaises à dividende :<br><em>sélection 2025</em></h1>",
        "<h1>Actions françaises à dividende :<br><em>sélection 2026</em></h1>",
    ),
    (
        "Voici la sélection 2025.",
        "Voici la sélection 2026.",
    ),
    (
        "📊 Sélection d'actions françaises à dividende (2025)",
        "📊 Sélection d'actions françaises à dividende (2026)",
    ),
    (
        "Via un PEA, les dividendes et plus-values sont exonérés d'IR après 5 ans (seuls les prélèvements sociaux de 17,2 % s'appliquent).",
        "Via un PEA, les dividendes et plus-values sont exonérés d'IR après 5 ans (seuls les prélèvements sociaux de 18,6 % s'appliquent depuis 2026).",
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

    with open(FICHIER + ".bak_art496", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   PEA prelevements sociaux 17,2%->18,6%, dates 2026")


if __name__ == "__main__":
    main()
