#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-429.html — dates 2025->2026
À lancer depuis ~/Desktop/mon site

Contenu majoritairement conceptuel (pas de chiffre réglementé à vérifier).
Seules les dates sont corrigées.

Idempotent. Sauvegarde en .bak_art429.

Usage :
    python3 corriger_article429.py
"""

import os

FICHIER = "article-429.html"

REMPLACEMENTS = [
    (
        "Dropshipping en 2025 : est-ce encore rentable ? — La vérité sans bullshit. Guide complet sur Economya.fr",
        "Dropshipping en 2026 : est-ce encore rentable ? — La vérité sans bullshit. Guide complet sur Economya.fr",
    ),
    (
        "<title>Dropshipping en 2025 : est-ce encore rentable ? — Economya.fr</title>",
        "<title>Dropshipping en 2026 : est-ce encore rentable ? — Economya.fr</title>",
    ),
    (
        '"headline": "Dropshipping en 2025 : est-ce encore rentable ?",',
        '"headline": "Dropshipping en 2026 : est-ce encore rentable ?",',
    ),
    (
        '<meta property="og:title" content="Dropshipping en 2025 : est-ce encore rentable ?">',
        '<meta property="og:title" content="Dropshipping en 2026 : est-ce encore rentable ?">',
    ),
    (
        '<meta name="twitter:title" content="Dropshipping en 2025 : est-ce encore rentable ?">',
        '<meta name="twitter:title" content="Dropshipping en 2026 : est-ce encore rentable ?">',
    ),
    (
        "<h1>Dropshipping en 2025 :<br><em>est-ce encore rentable ?</em></h1>",
        "<h1>Dropshipping en 2026 :<br><em>est-ce encore rentable ?</em></h1>",
    ),
    (
        'le dropshipping générique depuis la Chine est devenu très difficile en 2025, mais certaines niches et approches restent rentables.',
        'le dropshipping générique depuis la Chine est devenu très difficile, mais certaines niches et approches restent rentables.',
    ),
    (
        "⚖️ Verdict 2025 : dropshipping oui ou non ?",
        "⚖️ Verdict 2026 : dropshipping oui ou non ?",
    ),
    (
        "C'est la grande évolution du dropshipping 2025.",
        "C'est la grande évolution du dropshipping ces dernières années.",
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

    with open(FICHIER + ".bak_art429", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Dates 2026")


if __name__ == "__main__":
    main()
