#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-218.html — minimum ARE obsolète
À lancer depuis ~/Desktop/mon site

Le minimum ARE était à 31,59€/jour (valeur 2025) — la valeur actuelle
(depuis le 1er juillet 2025, applicable en 2026) est 32,13€/jour, confirmée
par plusieurs sources convergentes.

⚠️ NON corrigés (confiance insuffisante, une seule source chacun, pas de
consensus) : "Plafond 291,06€/jour" et "salaires > 11 600€/mois". À vérifier
séparément sur france-travail.fr ou unedic.org avant correction.

Idempotent. Sauvegarde en .bak_art218.

Usage :
    python3 corriger_article218.py
"""

import os

FICHIER = "article-218.html"

ANCIEN = "Minimum 31,59 €/jour · Maximum 75 % du SJR · Plancher légal selon salaire"
NOUVEAU = "Minimum 32,13 €/jour · Maximum 75 % du SJR · Plancher légal selon salaire"


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
    with open(FICHIER + ".bak_art218", 'w', encoding='utf-8') as f:
        f.write(contenu)
    nouveau_contenu = contenu.replace(ANCIEN, NOUVEAU, 1)
    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)
    print("✅ Minimum ARE corrigé : 31,59€/jour -> 32,13€/jour")
    print("   ⚠️ 'Plafond 291,06€/jour' et seuil '11 600€/mois' NON vérifiés")
    print("      avec assez de confiance — à contrôler sur france-travail.fr")


if __name__ == "__main__":
    main()
