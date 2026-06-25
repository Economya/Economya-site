#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-223.html (date) et article-230.html (abondement PEE)
À lancer depuis ~/Desktop/mon site

1. article-223 : "reconduite et pérennisée en 2025" -> 2026 (la PPV est
   confirmée pérenne, plafonds 3000€/6000€ inchangés et vérifiés pour 2026)
2. article-230 : abondement PEE "3 519€" -> "3 845€" (plafond 2026,
   indexé sur le PASS qui augmente chaque année — confirmé par plusieurs
   sources convergentes)

⚠️ NON corrigés dans article-230 (confiance insuffisante) : titres-
restaurant (1 292€), chèques vacances (520€), CESU (2 421€) — leurs modes
de calcul exacts n'ont pas pu être vérifiés avec assez de certitude pour
cette session. À vérifier séparément si la précision de cet exemple
chiffré est importante.

Idempotent. Sauvegarde en .bak_ppv.

Usage :
    python3 corriger_ppv.py
"""

import os

REMPLACEMENTS = {
    "article-223.html": [
        (
            "La Prime de Partage de la Valeur (PPV) — anciennement prime Macron ou prime de pouvoir d'achat — est reconduite et pérennisée en 2025.",
            "La Prime de Partage de la Valeur (PPV) — anciennement prime Macron ou prime de pouvoir d'achat — est reconduite et pérennisée en 2026.",
        ),
    ],
    "article-230.html": [
        (
            "Une combinaison PPV (3 000 €) + titres-restaurant (1 292 €) + chèques vacances (520 €) + CESU (2 421 €) + abondement PEE (3 519 €) représente plus de 10 000 € par an sans charges ni impôts",
            "Une combinaison PPV (3 000 €) + titres-restaurant + chèques vacances + CESU + abondement PEE (jusqu'à 3 845 €) représente plusieurs milliers d'euros par an sans charges ni impôts",
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

        with open(fichier + ".bak_ppv", 'w', encoding='utf-8') as f:
            f.write(contenu_original)

        with open(fichier, 'w', encoding='utf-8') as f:
            f.write(contenu)

        print(f"✅ {fichier} : {nb_modifs_fichier} remplacement(s)")
        total_fichiers += 1
        total_remplacements += nb_modifs_fichier

    print(f"\n=== RÉSUMÉ ===")
    print(f"Fichiers modifiés : {total_fichiers}")
    print(f"Remplacements totaux : {total_remplacements}")
    print(f"⚠️ Titres-restaurant/cheques vacances/CESU NON corriges (confiance")
    print(f"   insuffisante) - chiffres retires de l'exemple plutot que devines")


if __name__ == "__main__":
    main()
