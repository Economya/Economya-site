#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-223.html — dates 2025 restantes (titre, meta, h1)
À lancer depuis ~/Desktop/mon site

Les chiffres (3 000€/6 000€) sont déjà vérifiés corrects et inchangés
pour 2026 (confirmé précédemment dans la session). Seules les dates
"2025" du titre/meta/h1 (oubliées lors d'une correction partielle
précédente) sont mises à jour en "2026".

Idempotent. Sauvegarde en .bak_art223v2.

Usage :
    python3 corriger_article223_v2.py
"""

import os

FICHIER = "article-223.html"

REMPLACEMENTS = [
    (
        'Prime de partage de la valeur 2025 — Jusqu\'à 6 000€ exonérés. Guide complet sur Economya.fr',
        'Prime de partage de la valeur 2026 — Jusqu\'à 6 000€ exonérés. Guide complet sur Economya.fr',
    ),
    (
        '<title>Prime de partage de la valeur 2025 — Economya.fr</title>',
        '<title>Prime de partage de la valeur 2026 — Economya.fr</title>',
    ),
    (
        '"headline": "Prime de partage de la valeur 2025",',
        '"headline": "Prime de partage de la valeur 2026",',
    ),
    (
        '<meta property="og:title" content="Prime de partage de la valeur 2025">',
        '<meta property="og:title" content="Prime de partage de la valeur 2026">',
    ),
    (
        '<meta name="twitter:title" content="Prime de partage de la valeur 2025">',
        '<meta name="twitter:title" content="Prime de partage de la valeur 2026">',
    ),
    (
        '<h1>Prime de partage de la valeur 2025</h1>',
        '<h1>Prime de partage de la valeur 2026</h1>',
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

    with open(FICHIER + ".bak_art223v2", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Titre/meta/h1 corriges en 2026 (chiffres deja verifies corrects)")


if __name__ == "__main__":
    main()
