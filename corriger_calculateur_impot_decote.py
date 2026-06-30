#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction calculateur-impot.html — montants de la décote obsolètes
À lancer depuis ~/Desktop/mon site

CONFIRMÉ par source officielle (economie.gouv.fr, article daté du
17/04/2026, citant l'article 197 du CGI) :
- Décote célibataire : 897€ (l'outil utilisait 873€, montant 2025)
- Décote couple : 1 483€ (l'outil utilisait 1444€, montant 2025)
- Formule de calcul (45,25%) confirmée correcte, inchangée

Idempotent. Sauvegarde en .bak_decote2026.

Usage :
    python3 corriger_calculateur_impot_decote.py
"""

import os

FICHIER = "calculateur-impot.html"

ANCIEN = "const decote = parts === 1 ? 873 - impotBrut * 0.4525 : 1444 - impotBrut * 0.4525;"
NOUVEAU = "const decote = parts === 1 ? 897 - impotBrut * 0.4525 : 1483 - impotBrut * 0.4525;"


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
    with open(FICHIER + ".bak_decote2026", 'w', encoding='utf-8') as f:
        f.write(contenu)
    nouveau_contenu = contenu.replace(ANCIEN, NOUVEAU, 1)
    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)
    print("✅ Décote corrigée : 873e->897e (célibataire), 1444e->1483e (couple)")
    print("   Confirmé par economie.gouv.fr, article du 17/04/2026")


if __name__ == "__main__":
    main()
