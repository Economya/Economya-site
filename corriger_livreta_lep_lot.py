#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction du lot Livret A/LEP — erreur systémique trouvée sur 7 fichiers
supplémentaires (en plus des 4 déjà corrigés aujourd'hui : 337, 383, 69, 88)
À lancer depuis ~/Desktop/mon site

Taux confirmés 2026 (sources officielles, déjà utilisés ailleurs
aujourd'hui) : Livret A = 1,5%, LEP = 2,5%.

⚠️ article-342 : seuls les pourcentages sont corrigés. Les autres
colonnes du tableau (30 800€/6 800€, 36 800€/12 800€) ne sont PAS
modifiées par prudence — sans connaître les en-têtes exacts du tableau,
impossible de savoir si elles dépendent du taux (à vérifier manuellement
si besoin).

Idempotent. Sauvegardes individuelles .bak_artXXX.

Usage :
    python3 corriger_livreta_lep_lot.py
"""

import os

REMPLACEMENTS = {
    "article-174.html": [
        (
            "Pour un petit épargnant débutant, la priorité absolue est le Livret A (taux de 2,4 % en 2025, défiscalisé, disponible à tout moment).",
            "Pour un petit épargnant débutant, la priorité absolue est le Livret A (taux de 1,5 % en 2026, défiscalisé, disponible à tout moment).",
        ),
    ],
    "article-37.html": [
        (
            "<span>Avec Livret A (3%)</span>",
            "<span>Avec Livret A (1,5%)</span>",
        ),
    ],
    "article-422.html": [
        (
            "Les livrets réglementés (LEP à 4 %) génèrent des intérêts sans aucun effort.",
            "Les livrets réglementés (LEP à 2,5 %) génèrent des intérêts sans aucun effort.",
        ),
    ],
    "article-447.html": [
        (
            "Livret A (3 % en 2025, plafonné à 22 950 €) ou LEP (4 % si revenus modestes, plafonné à 10 000 €) sont les supports idéaux.",
            "Livret A (1,5 % en 2026, plafonné à 22 950 €) ou LEP (2,5 % si revenus modestes, plafonné à 10 000 €) sont les supports idéaux.",
        ),
    ],
    "article-509.html": [
        (
            "Un Livret A à 2,4% ne bat pas une inflation à 3%.",
            "Un Livret A à 1,5% ne bat pas l'inflation actuelle (environ 2,4%).",
        ),
    ],
    "article-514.html": [
        (
            "Le Livret A à 2,4% ne suffit plus.",
            "Le Livret A à 1,5% ne suffit plus.",
        ),
    ],
    "article-342.html": [
        (
            "<tr><td>Livret A</td><td>2,4 %</td>",
            "<tr><td>Livret A</td><td>1,5 %</td>",
        ),
        (
            "<tr><td>LEP</td><td>4 %</td>",
            "<tr><td>LEP</td><td>2,5 %</td>",
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
    print(f"⚠️ article-342 : seuls les % corriges, autres colonnes du tableau")
    print(f"   non modifiees par prudence (en-tetes inconnus)")


if __name__ == "__main__":
    main()
