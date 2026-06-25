#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-497.html — déficit foncier prolongé + date obsolète
À lancer depuis ~/Desktop/mon site

Le doublement du déficit foncier (21 400€ au lieu de 10 700€) pour les
travaux d'isolation énergétique sortant un logement de "passoire
thermique" a été PROLONGÉ jusqu'au 31 décembre 2027 par la loi de
finances 2026 (loi n°2026-103 du 19 février 2026) — confirmé par de
nombreuses sources convergentes. L'article disait "jusqu'en 2025"
(obsolète, dispositif qui devait s'arrêter mais a été prolongé).

Idempotent. Sauvegarde en .bak_art497.

Usage :
    python3 corriger_article497.py
"""

import os

FICHIER = "article-497.html"

REMPLACEMENTS = [
    (
        "De la déduction PER au déficit foncier en passant par les dons d'associations, voici les principales niches fiscales 2025 classées par accessibilité et impact réel.",
        "De la déduction PER au déficit foncier en passant par les dons d'associations, voici les principales niches fiscales 2026 classées par accessibilité et impact réel.",
    ),
    (
        "Si vous louez un bien immobilier et que vos charges (travaux, intérêts d'emprunt) dépassent vos loyers, le déficit foncier est imputable sur votre revenu global jusqu'à 10 700 €/an (ou 21 400 € pour les travaux d'isolation énergétique jusqu'en 2025). Très puissant pour les gros revenus avec patrimoine immobilier.",
        "Si vous louez un bien immobilier et que vos charges (travaux, intérêts d'emprunt) dépassent vos loyers, le déficit foncier est imputable sur votre revenu global jusqu'à 10 700 €/an (ou 21 400 € pour les travaux d'isolation énergétique sortant un logement de la catégorie \"passoire thermique\", dispositif prolongé jusqu'au 31 décembre 2027). Très puissant pour les gros revenus avec patrimoine immobilier.",
    ),
]


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable.")
        return

    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()

    contenu_original = contenu
    nb_modifs = 0

    for ancien, nouveau in REMPLACEMENTS:
        if nouveau in contenu and ancien not in contenu:
            continue
        if ancien in contenu:
            contenu = contenu.replace(ancien, nouveau)
            nb_modifs += 1

    if nb_modifs == 0:
        print("✅ Déjà corrigé ou textes attendus non trouvés.")
        return

    with open(FICHIER + ".bak_art497", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Deficit foncier majore prolonge jusqu'en 2027, date 2026")


if __name__ == "__main__":
    main()
