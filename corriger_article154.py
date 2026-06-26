#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-154.html — allocation télétravail : erreur de calcul
+ date
À lancer depuis ~/Desktop/mon site

Le taux journalier (2,70€) est confirmé stable et correct pour 2026.
Mais le calcul mensuel pour "deux jours par semaine" était erroné :
54€ ne correspond à aucun calcul cohérent (2,70€ × 2j × ~4,33 semaines
≈ 23€/mois, confirmé par sources officielles à 22€/mois pour 2j/semaine,
plafond URSSAF). Le 54€ original semble être une confusion avec un
calcul à 4-5 jours/semaine, pas 2.

Idempotent. Sauvegarde en .bak_art154.

Usage :
    python3 corriger_article154.py
"""

import os

FICHIER = "article-154.html"

ANCIEN = "l'allocation forfaitaire journalière (exonérée de charges jusqu'à 2,70 euros par jour de télétravail en 2025, soit environ 54 euros par mois pour deux jours par semaine)"
NOUVEAU = "l'allocation forfaitaire journalière (exonérée de charges jusqu'à 2,70 euros par jour de télétravail en 2026, soit environ 22 euros par mois pour deux jours par semaine, dans la limite de 59,40 €/mois)"


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
    with open(FICHIER + ".bak_art154", 'w', encoding='utf-8') as f:
        f.write(contenu)
    nouveau_contenu = contenu.replace(ANCIEN, NOUVEAU, 1)
    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)
    print("✅ Allocation télétravail corrigée : 54€ -> 22€/mois (erreur de calcul), date 2026")


if __name__ == "__main__":
    main()
