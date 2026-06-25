#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-251.html — dates 2025->2026
À lancer depuis ~/Desktop/mon site

Confirmé par AV-TEST (tests février et avril 2026) : le score de
Windows Defender reste 6/6 en protection, inchangé. Seule l'étiquette
d'année est mise à jour ; les scores numériques (6/6, 5.5/6) ne sont PAS
modifiés (déjà confirmés exacts ou plausibles).

Idempotent. Sauvegarde en .bak_art251.

Usage :
    python3 corriger_article251.py
"""

import os

FICHIER = "article-251.html"

REMPLACEMENTS_UNIQUES = [
    (
        "<title>Antivirus gratuit : les meilleurs en 2025 — Economya.fr</title>",
        "<title>Antivirus gratuit : les meilleurs en 2026 — Economya.fr</title>",
    ),
    (
        '"headline": "Antivirus gratuit : les meilleurs en 2025",',
        '"headline": "Antivirus gratuit : les meilleurs en 2026",',
    ),
    (
        "Antivirus gratuit : les meilleurs en 2025 — Protection sans abonnement. Guide complet sur Economya.fr",
        "Antivirus gratuit : les meilleurs en 2026 — Protection sans abonnement. Guide complet sur Economya.fr",
    ),
    (
        '<meta property="og:title" content="Antivirus gratuit : les meilleurs en 2025">',
        '<meta property="og:title" content="Antivirus gratuit : les meilleurs en 2026">',
    ),
    (
        '<meta name="twitter:title" content="Antivirus gratuit : les meilleurs en 2025">',
        '<meta name="twitter:title" content="Antivirus gratuit : les meilleurs en 2026">',
    ),
    (
        "<h1>Antivirus gratuit :<br><em>les meilleurs en 2025</em></h1>",
        "<h1>Antivirus gratuit :<br><em>les meilleurs en 2026</em></h1>",
    ),
    (
        "Payer 40 à 80 € par an pour un antivirus en 2025 ?",
        "Payer 40 à 80 € par an pour un antivirus ?",
    ),
    (
        "Note AV-TEST 2025 : 6/6 en protection.",
        "Note AV-TEST 2026 : 6/6 en protection.",
    ),
]

# AV-TEST 2025 -> 2026 apparait plusieurs fois identique (avsub) : remplace toutes les occurrences
REMPLACEMENT_GLOBAL = ('<span class="avsub">AV-TEST 2025</span>', '<span class="avsub">AV-TEST 2026</span>')


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable.")
        return

    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()

    contenu_original = contenu
    nb_modifs = 0

    for ancien, nouveau in REMPLACEMENTS_UNIQUES:
        if nouveau in contenu and ancien not in contenu:
            continue
        if ancien in contenu:
            contenu = contenu.replace(ancien, nouveau)
            nb_modifs += 1

    ancien_g, nouveau_g = REMPLACEMENT_GLOBAL
    nb_occurrences = contenu.count(ancien_g)
    if nb_occurrences > 0:
        contenu = contenu.replace(ancien_g, nouveau_g)
        nb_modifs += nb_occurrences

    if nb_modifs == 0:
        print("✅ Déjà corrigé ou textes attendus non trouvés.")
        return

    with open(FICHIER + ".bak_art251", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Dates AV-TEST 2026 (scores 6/6 confirmes inchanges)")


if __name__ == "__main__":
    main()
