#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-230.html (3e passage) — réintégration des chiffres
CESU et chèques vacances, maintenant vérifiés
À lancer depuis ~/Desktop/mon site

Ce matin, ces chiffres avaient été retirés par prudence (confiance
insuffisante à ce moment-là). Maintenant vérifiés avec une très forte
convergence de sources officielles (Urssaf.fr) pour 2026 :
- CESU préfinancé : 2 591€/an (confirmé, +2% vs 2025)
- Chèques vacances : 560,10€/an pour les petites entreprises (<50 sal.)

Le titre-restaurant n'a PAS de plafond annuel officiel fixe (mécanisme
par titre : 12,20-14,64€ de valeur faciale, 7,32€ max de part patronale
exonérée par titre — dépend du nombre de jours travaillés). Reste donc
sans chiffre annuel inventé, par prudence.

Idempotent. Sauvegarde en .bak_art230v2.

Usage :
    python3 corriger_article230_v2.py
"""

import os

FICHIER = "article-230.html"

ANCIEN = "Une combinaison PPV (3 000 €) + titres-restaurant + chèques vacances + CESU + abondement PEE (jusqu'à 3 845 €) représente plusieurs milliers d'euros par an sans charges ni impôts — l'équivalent d'environ 16 000 € de salaire brut supplémentaire."

NOUVEAU = "Une combinaison PPV (3 000 €) + titres-restaurant (7,32 €/titre de part patronale exonérée, selon le nombre de jours travaillés) + chèques vacances (560 €) + CESU (2 591 €) + abondement PEE (jusqu'à 3 845 €) représente plusieurs milliers d'euros par an sans charges ni impôts."


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
    with open(FICHIER + ".bak_art230v2", 'w', encoding='utf-8') as f:
        f.write(contenu)
    nouveau_contenu = contenu.replace(ANCIEN, NOUVEAU, 1)
    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)
    print("✅ Chiffres CESU (2 591€) et chèques vacances (560€) réintégrés")


if __name__ == "__main__":
    main()
