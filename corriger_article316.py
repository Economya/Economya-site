#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-316.html — montant ARS obsolète (même correction que
article-309/article-53)
À lancer depuis ~/Desktop/mon site

ARS 2026 : 466€ maximum (au lieu de 406€).

Idempotent. Sauvegarde en .bak_art316.

Usage :
    python3 corriger_article316.py
"""

import os

FICHIER = "article-316.html"

ANCIEN = '<div class="aide-amount">jusqu\'à 406 €</div>\n      <div class="aide-cond">Par enfant scolarisé de 6 à 18 ans. Sous conditions de revenus. Versée en août par la CAF.</div>'
NOUVEAU = '<div class="aide-amount">jusqu\'à 466 €</div>\n      <div class="aide-cond">Par enfant scolarisé de 6 à 18 ans, selon son âge (426,87€ à 466,02€ en 2026). Sous conditions de revenus. Versée en août par la CAF.</div>'


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
    with open(FICHIER + ".bak_art316", 'w', encoding='utf-8') as f:
        f.write(contenu)
    nouveau_contenu = contenu.replace(ANCIEN, NOUVEAU, 1)
    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)
    print("✅ ARS corrigée : 406€ -> 466€ (avec détail des tranches d'âge)")


if __name__ == "__main__":
    main()
