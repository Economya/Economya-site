#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-89.html — montant ASPA obsolète
À lancer depuis ~/Desktop/mon site

ASPA (minimum vieillesse) : 1 012€/mois (2025, déjà imprécis) -> 1 043,59€/mois
(2026, revalorisé +0,9% au 1er janvier 2026, confirmé par service-public.gouv.fr
et de nombreuses sources convergentes).

Idempotent. Sauvegarde en .bak_art89.

Usage :
    python3 corriger_article89.py
"""

import os

FICHIER = "article-89.html"

ANCIEN = "L'ASPA (Allocation de Solidarité aux Personnes Âgées)</strong> — le minimum vieillesse rénové, accessible dès 65 ans sous conditions de revenus. Jusqu'à 1 012 € par mois pour une personne seule en 2025."
NOUVEAU = "L'ASPA (Allocation de Solidarité aux Personnes Âgées)</strong> — le minimum vieillesse rénové, accessible dès 65 ans sous conditions de revenus. Jusqu'à 1 043,59 € par mois pour une personne seule en 2026."


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
    with open(FICHIER + ".bak_art89", 'w', encoding='utf-8') as f:
        f.write(contenu)
    nouveau_contenu = contenu.replace(ANCIEN, NOUVEAU, 1)
    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)
    print("✅ ASPA corrigée : 1 012€ (2025) -> 1 043,59€ (2026)")


if __name__ == "__main__":
    main()
