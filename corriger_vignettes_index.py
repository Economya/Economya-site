#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nuance des badges vignettes sur la page d'accueil — index.html
À lancer UNE SEULE FOIS depuis le dossier ~/Desktop/mon site

Même logique que la passe de nuance déjà appliquée sur les 527 articles,
mais ici sur les badges "abadge" de la page d'accueil (qui sont du texte
codé en dur, séparé des articles, et n'avaient pas été touchés).

Corrections :
1. "Économisez X€" -> "Économisez jusqu'à X€"
2. "-X%" (non protégé) -> "Jusqu'à -X%"

Cohérent avec le style déjà utilisé sur la majorité des autres badges
de la page ("Jusqu'à 80€/mois" etc.) — uniformise sans dénaturer
l'aspect accrocheur.

Idempotent. Sauvegarde en .bak_conformite_index avant modification.

Usage :
    python3 corriger_vignettes_index.py
"""

import os
import re

FICHIER = "index.html"

PATTERN_ECO = re.compile(
    r"(?<!jusqu'à )(?<!Jusqu'à )([ÉéEe]conomisez|[ÉéEe]conomiser) (\d+\s?€)"
)

def fix_eco(match):
    verbe, montant = match.group(1), match.group(2)
    return f"{verbe} jusqu'à {montant}"

PATTERN_PCT = re.compile(
    r"(?<!à )(?<![a-zA-Z0-9])-(\d+)\s?%"
)

def fix_pct(match):
    return f"jusqu'à -{match.group(1)}%"


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable dans ce dossier.")
        return

    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()

    contenu_original = contenu
    nb_eco = len(PATTERN_ECO.findall(contenu))
    nb_pct = len(PATTERN_PCT.findall(contenu))

    if nb_eco == 0 and nb_pct == 0:
        print("✅ Déjà à jour — aucune formulation non nuancée trouvée.")
        return

    contenu = PATTERN_ECO.sub(fix_eco, contenu)
    contenu = PATTERN_PCT.sub(fix_pct, contenu)

    with open(FICHIER + ".bak_conformite_index", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ Vignettes corrigées :")
    print(f"   - 'Économisez/économiser X€' nuancées : {nb_eco}")
    print(f"   - '-X%' nuancés avec 'jusqu'à' : {nb_pct}")
    print(f"   Sauvegarde créée : {FICHIER}.bak_conformite_index")


if __name__ == "__main__":
    main()
