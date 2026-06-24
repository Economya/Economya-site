#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-201.html — taux immobilier daté 2025
À lancer depuis ~/Desktop/mon site

Taux actuel (juin 2026, sources convergentes CAFPI/Pretto/Meilleurtaux) :
~3,3 à 3,7% sur 20 ans. La fourchette citée (3,4-3,8%) restait dans le bon
ordre de grandeur mais datée "2025" — mise à jour de l'année et légers
ajustements de la fourchette pour refléter juin 2026.

Idempotent. Sauvegarde en .bak_taux201.

Usage :
    python3 corriger_taux_immo_201.py
"""

import os

FICHIER = "article-201.html"

ANCIEN = "Acheter sa résidence principale est souvent le plus grand achat d'une vie. En 2025, les taux immobiliers se stabilisent autour de 3,4 à 3,8 % sur 20 ans — loin des sommets de 2023, mais encore loin des 1 % de 2021. Faut-il attendre encore, ou sauter le pas ? Et si on achète, comment éviter de payer trop cher à chaque étape ? Ce guide suit l'ordre chronologique d'un achat, du premier calcul de capacité jusqu'à la signature chez le notaire."

NOUVEAU = "Acheter sa résidence principale est souvent le plus grand achat d'une vie. En 2026, les taux immobiliers se stabilisent autour de 3,3 à 3,7 % sur 20 ans — loin des sommets de 2023-2024, mais encore loin des 1 % de 2021. Faut-il attendre encore, ou sauter le pas ? Et si on achète, comment éviter de payer trop cher à chaque étape ? Ce guide suit l'ordre chronologique d'un achat, du premier calcul de capacité jusqu'à la signature chez le notaire."


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
    with open(FICHIER + ".bak_taux201", 'w', encoding='utf-8') as f:
        f.write(contenu)
    nouveau_contenu = contenu.replace(ANCIEN, NOUVEAU, 1)
    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)
    print("✅ Taux immobilier mis à jour : 2025 (3,4-3,8%) -> 2026 (3,3-3,7%)")


if __name__ == "__main__":
    main()
