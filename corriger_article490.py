#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-490.html — taux MaPrimeRénov' obsolète
À lancer depuis ~/Desktop/mon site

"Jusqu'à 70%" -> "jusqu'à 80%" (taux maximum 2026 confirmé, cohérent avec
les autres corrections déjà appliquées sur le site).

Idempotent. Sauvegarde en .bak_art490.

Usage :
    python3 corriger_article490.py
"""

import os

FICHIER = "article-490.html"

ANCIEN = '<div class="p-right"><span class="p-gratuit">Jusqu\'à 70 %</span><span class="p-sub">Des travaux pris en charge</span></div>'
NOUVEAU = '<div class="p-right"><span class="p-gratuit">Jusqu\'à 80 %</span><span class="p-sub">Des travaux pris en charge</span></div>'


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
    with open(FICHIER + ".bak_art490", 'w', encoding='utf-8') as f:
        f.write(contenu)
    nouveau_contenu = contenu.replace(ANCIEN, NOUVEAU, 1)
    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)
    print("✅ Taux corrigé : 70% -> 80%")


if __name__ == "__main__":
    main()
