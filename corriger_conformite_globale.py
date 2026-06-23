#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mise en conformité globale des formulations chiffrées — article-*.html
À lancer UNE SEULE FOIS depuis le dossier ~/Desktop/mon site

Objectif : nuancer systématiquement les affirmations chiffrées non garanties,
sans prétendre vérifier l'exactitude de chaque chiffre individuellement.

Corrections :
1. "Économisez X€" / "économiser X€" -> ajoute "jusqu'à" si absent
2. "-X%" non précédé de "jusqu'à"/"à " -> ajoute "Jusqu'à" devant

Ne touche PAS aux phrases qui contiennent déjà une nuance ("jusqu'à", "environ",
"en moyenne") ni aux plages de valeurs ("10-30%") ni aux mots accolés
("Page-30%").

Idempotent. Sauvegarde chaque fichier modifié en .bak_conformite.

Usage :
    python3 corriger_conformite_globale.py
"""

import os
import re
import glob

# Motif 1 : "Économisez X€" ou "économiser X€" sans "jusqu'à" déjà présent
PATTERN_ECO = re.compile(
    r"(?<!jusqu'à )(?<!Jusqu'à )([ÉéEe]conomisez|[ÉéEe]conomiser) (\d+\s?€)"
)

def fix_eco(match):
    verbe, montant = match.group(1), match.group(2)
    return f"{verbe} jusqu'à {montant}"

# Motif 2 : "-X%" non précédé de "à " (jusqu'à) ni d'une lettre/chiffre (mot accolé ou plage)
PATTERN_PCT = re.compile(
    r"(?<!à )(?<![a-zA-Z0-9])-(\d+)\s?%"
)

def fix_pct(match):
    return f"jusqu'à -{match.group(1)}%"


def traiter_fichier(chemin):
    with open(chemin, 'r', encoding='utf-8') as f:
        contenu = f.read()

    contenu_original = contenu
    nb_eco = len(PATTERN_ECO.findall(contenu))
    nb_pct = len(PATTERN_PCT.findall(contenu))

    if nb_eco == 0 and nb_pct == 0:
        return None

    contenu = PATTERN_ECO.sub(fix_eco, contenu)
    contenu = PATTERN_PCT.sub(fix_pct, contenu)

    if contenu == contenu_original:
        return None

    chemin_bak = chemin + ".bak_conformite"
    if not os.path.exists(chemin_bak):
        with open(chemin_bak, 'w', encoding='utf-8') as f:
            f.write(contenu_original)

    with open(chemin, 'w', encoding='utf-8') as f:
        f.write(contenu)

    return (nb_eco, nb_pct)


def main():
    fichiers = sorted(glob.glob("article-*.html"))

    total_modifies = 0
    total_eco = 0
    total_pct = 0
    erreurs = []

    for fichier in fichiers:
        try:
            resultat = traiter_fichier(fichier)
            if resultat:
                total_modifies += 1
                total_eco += resultat[0]
                total_pct += resultat[1]
        except Exception as e:
            erreurs.append(f"{fichier} : {e}")

    print(f"\n=== RÉSUMÉ ===")
    print(f"Fichiers traités : {len(fichiers)}")
    print(f"Fichiers modifiés : {total_modifies}")
    print(f"  - occurrences 'économisez/économiser X€' nuancées : {total_eco}")
    print(f"  - occurrences '-X%' nuancées avec 'Jusqu'à' : {total_pct}")
    print(f"Erreurs : {len(erreurs)}")
    for e in erreurs:
        print(f"  ⚠️  {e}")
    print(f"\nSauvegardes créées avec l'extension .bak_conformite")


if __name__ == "__main__":
    main()
