#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-279.html — dates 2025->2026
À lancer depuis ~/Desktop/mon site

Contenu générique (sac cabine), pas de chiffre substantiel a verifier.

Idempotent. Sauvegarde en .bak_art279.

Usage :
    python3 corriger_article279.py
"""

import os

FICHIER = "article-279.html"

ANCIEN = "💡 Le meilleur sac cabine en 2025"
NOUVEAU = "💡 Le meilleur sac cabine en 2026"


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable.")
        return
    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()
    if NOUVEAU in contenu:
        print("✅ Déjà corrigé.")
        return
    if ANCIEN not in contenu:
        print("⚠️ Texte attendu non trouvé. Aucune modification.")
        return
    with open(FICHIER + ".bak_art279", 'w', encoding='utf-8') as f:
        f.write(contenu)
    nouveau_contenu = contenu.replace(ANCIEN, NOUVEAU, 1)
    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)
    print("✅ Date corrigee 2026")


if __name__ == "__main__":
    main()
