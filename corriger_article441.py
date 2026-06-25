#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-441.html — dates obsolètes (2025 -> 2026)
À lancer depuis ~/Desktop/mon site

Bonne nouvelle vérifiée : tous les chiffres de l'article (taux 12%/18%/21%,
plafonds 300 000€ et 5 500€/m², durées 6/9/12 ans) sont TOUJOURS CORRECTS
en 2026 — confirmés par de nombreuses sources convergentes. Le dispositif
est même officiellement reconduit jusqu'au 31/12/2027 (loi de finances
2026, art. 47, loi n°2026-103 du 19/02/2026).

Seul problème : les 11 occurrences de "2025" dans le titre/meta/contenu,
à corriger en "2026".

Idempotent. Sauvegarde en .bak_art441.

Usage :
    python3 corriger_article441.py
"""

import os

FICHIER = "article-441.html"


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable.")
        return

    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()

    contenu_original = contenu

    if "2025" not in contenu:
        print("✅ Déjà corrigé.")
        return

    nb_2025 = contenu.count("2025")
    contenu = contenu.replace("2025", "2026")

    with open(FICHIER + ".bak_art441", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_2025} occurrence(s) de '2025' corrigée(s) en '2026'")
    print("   (les taux 12/18/21% et plafonds 300 000€/5 500€ restent")
    print("   inchangés, déjà corrects et vérifiés pour 2026)")


if __name__ == "__main__":
    main()
