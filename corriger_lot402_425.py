#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction du lot article-402/413/415/419/424/425
À lancer depuis ~/Desktop/mon site

article-419 : DEUX problèmes —
1. Erreur d'unité : "€/mois/m²" alors que le plafond légal (art. 35 bis
   CGI) est un montant ANNUEL ("€/an/m²"), confirmé par de nombreuses
   sources officielles (impots.gouv.fr, LégiFiscal)
2. Montants légèrement datés : 206€/152€ -> 213€/157€ (plafonds 2025,
   applicables aux revenus déclarés en 2026)

article-402 : exemple illustratif, dates avancées d'un an pour rester
pertinent (mécanisme inchangé).
article-413/415/424/425 : dates génériques uniquement.

Idempotent. Sauvegardes individuelles .bak_artXXX.

Usage :
    python3 corriger_lot402_425.py
"""

import os

REMPLACEMENTS = {
    "article-402.html": [
        (
            "Des chèques émis en 2024 expirent le 31 décembre 2025.",
            "Des chèques émis en 2025 expirent le 31 décembre 2026.",
        ),
    ],
    "article-413.html": [
        (
            "🚨 Les arnaques les plus répandues en 2025",
            "🚨 Les arnaques les plus répandues en 2026",
        ),
    ],
    "article-415.html": [
        (
            "⭐ Marché très actif en 2025",
            "⭐ Marché très actif en 2026",
        ),
    ],
    "article-419.html": [
        (
            "si vous louez une pièce de votre résidence principale à des étudiants ou salariés à titre de résidence principale, les loyers peuvent être exonérés d'impôt si le loyer n'excède pas 206 €/mois/m² (zones tendues) ou 152 €/mois/m² (autres zones) en 2025.",
            "si vous louez une pièce de votre résidence principale à des étudiants ou salariés à titre de résidence principale, les loyers peuvent être exonérés d'impôt si le loyer annuel n'excède pas 213 €/an/m² (Île-de-France) ou 157 €/an/m² (autres régions) en 2025-2026.",
        ),
        (
            "Si vous louez une ou plusieurs pièces de votre résidence principale à titre de résidence principale du locataire, les revenus sont exonérés d'impôt sous conditions de plafond de loyer. En 2025, le plafond est de 206 €/m² de surface habitable dans les zones tendues et 152 €/m² ailleurs. Une chambre de 12 m² peut générer jusqu'à 2 472 €/an exonérés en zone tendue.",
            "Si vous louez une ou plusieurs pièces de votre résidence principale à titre de résidence principale du locataire, les revenus sont exonérés d'impôt sous conditions de plafond de loyer ANNUEL (et non mensuel). En 2025-2026, le plafond est de 213 €/m²/an de surface habitable en Île-de-France et 157 €/m²/an dans les autres régions. Une chambre de 12 m² peut générer jusqu'à 2 556 €/an exonérés en Île-de-France.",
        ),
    ],
    "article-424.html": [
        (
            "Très populaire en 2025.",
            "Très populaire depuis 2025.",
        ),
    ],
    "article-425.html": [
        (
            "Marché très actif en 2025.",
            "Marché très actif en 2026.",
        ),
    ],
}


def main():
    total_fichiers = 0
    total_remplacements = 0

    for fichier, paires in REMPLACEMENTS.items():
        if not os.path.exists(fichier):
            print(f"❌ {fichier} introuvable, ignoré.")
            continue

        with open(fichier, 'r', encoding='utf-8') as f:
            contenu = f.read()

        contenu_original = contenu
        nb_modifs_fichier = 0

        for ancien, nouveau in paires:
            if nouveau in contenu and ancien not in contenu:
                continue
            if ancien in contenu:
                contenu = contenu.replace(ancien, nouveau)
                nb_modifs_fichier += 1

        if nb_modifs_fichier == 0:
            print(f"✅ {fichier} : déjà corrigé ou texte non trouvé")
            continue

        ext = fichier.replace("article-", "").replace(".html", "")
        with open(fichier + f".bak_art{ext}", 'w', encoding='utf-8') as f:
            f.write(contenu_original)

        with open(fichier, 'w', encoding='utf-8') as f:
            f.write(contenu)

        print(f"✅ {fichier} : {nb_modifs_fichier} remplacement(s)")
        total_fichiers += 1
        total_remplacements += nb_modifs_fichier

    print(f"\n=== RÉSUMÉ ===")
    print(f"Fichiers modifiés : {total_fichiers}")
    print(f"Remplacements totaux : {total_remplacements}")
    print(f"⚠️ article-419: erreur d'unite corrigee (mois -> an)")


if __name__ == "__main__":
    main()
