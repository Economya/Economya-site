#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-51.html — 12e occurrence du taux Livret A obsolète
À lancer depuis ~/Desktop/mon site

Même erreur systémique que les 11 autres occurrences corrigées
aujourd'hui. Taux confirmé 2026 : 1,5%.

Idempotent. Sauvegarde en .bak_art51.

Usage :
    python3 corriger_article51.py
"""

import os

FICHIER = "article-51.html"

ANCIEN = "C'est le rendement historique annualisé du marché actions mondial sur les 30 dernières années — contre 3 % pour le Livret A aujourd'hui."
NOUVEAU = "C'est le rendement historique annualisé du marché actions mondial sur les 30 dernières années — contre 1,5 % pour le Livret A aujourd'hui."


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
    with open(FICHIER + ".bak_art51", 'w', encoding='utf-8') as f:
        f.write(contenu)
    nouveau_contenu = contenu.replace(ANCIEN, NOUVEAU, 1)
    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)
    print("✅ Livret A corrigé : 3% -> 1,5% (12e occurrence de cette erreur)")


if __name__ == "__main__":
    main()
