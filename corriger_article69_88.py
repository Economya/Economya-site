#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-69.html (PTZ) et article-88.html (Livret A/LEP)
À lancer depuis ~/Desktop/mon site

1. article-69 : "jusqu'à 40%" du PTZ généralise mal — le vrai max est
   50% en zone A (confirmé dans article-203 corrigé plus tôt aujourd'hui).

2. article-88 : Livret A "3% en 2025" était déjà faux à l'époque (le
   vrai taux 2025 tournait autour de 1,7-2,4%), et le LEP "4% en 2025"
   est la même erreur déjà trouvée et corrigée plusieurs fois aujourd'hui.
   Taux 2026 confirmés : Livret A 1,5%, LEP 2,5%.

Idempotent. Sauvegardes en .bak_art69 et .bak_art88.

Usage :
    python3 corriger_article69_88.py
"""

import os

REMPLACEMENTS = {
    "article-69.html": [
        (
            "Le PTZ finance jusqu'à 40 % du prix du logement sans intérêts ni frais de dossier. Soumis à conditions de revenus et de zone géographique. Réformé en 2024 pour couvrir aussi bien le neuf que l'ancien avec travaux.",
            "Le PTZ finance jusqu'à 50 % du prix du logement sans intérêts ni frais de dossier, selon la zone géographique. Soumis à conditions de revenus. Réformé en 2025 pour couvrir aussi bien le neuf que l'ancien avec travaux, prorogé jusqu'au 31 décembre 2027.",
        ),
    ],
    "article-88.html": [
        (
            "Le Livret A est le point de départ idéal pour une épargne de précaution : taux garanti par l'État (3 % en 2025), liquidité immédiate, aucun risque de perte.",
            "Le Livret A est le point de départ idéal pour une épargne de précaution : taux garanti par l'État (1,5 % en 2026), liquidité immédiate, aucun risque de perte.",
        ),
        (
            "Et pour les ménages modestes, le <strong>Livret d'Épargne Populaire (LEP)</strong> propose un taux supérieur au Livret A (4 % en 2025) avec un plafond de 10 000 €.",
            "Et pour les ménages modestes, le <strong>Livret d'Épargne Populaire (LEP)</strong> propose un taux supérieur au Livret A (2,5 % en 2026) avec un plafond de 10 000 €.",
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


if __name__ == "__main__":
    main()
