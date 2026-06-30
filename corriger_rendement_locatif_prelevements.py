#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction calculateur-rendement-locatif.html — prélèvements sociaux
obsolètes (17,2% au lieu de 18,6%)
À lancer depuis ~/Desktop/mon site

MÊME ERREUR que celle trouvée et corrigée aujourd'hui dans plusieurs
articles (ex: article-496, PEA) : les prélèvements sociaux sont passés
à 18,6% en 2026 (hausse confirmée, non exemptée pour les revenus
fonciers). L'outil utilisait encore 17,2% (taux historique), répété
4 fois dans le calcul (régime micro-foncier 30%, régime réel x2,
LMNP).

Le taux marginal d'imposition (TMI 30%) est conservé tel quel — c'est
une hypothèse de calcul par défaut (TMI médiane), pas une erreur.

Idempotent. Sauvegarde en .bak_prelevsociaux2026.

Usage :
    python3 corriger_rendement_locatif_prelevements.py
"""

import os

FICHIER = "calculateur-rendement-locatif.html"

REMPLACEMENTS = [
    (
        "baseImposable = loyersAnnuels * 0.70; // abattement 30%\n    impots = baseImposable * (0.30 + 0.172);",
        "baseImposable = loyersAnnuels * 0.70; // abattement 30%\n    impots = baseImposable * (0.30 + 0.186); // TMI 30% + prelevements sociaux 18,6% (2026)",
    ),
    (
        "baseImposable = loyersAnnuels * 0.50; // abattement 50%\n    impots = baseImposable * (0.30 + 0.172);",
        "baseImposable = loyersAnnuels * 0.50; // abattement 50%\n    impots = baseImposable * (0.30 + 0.186); // TMI 30% + prelevements sociaux 18,6% (2026)",
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

    # Traiter aussi les 2 occurrences isolées restantes (régime réel et LMNP)
    ancien_isole = "impots = baseImposable * (0.30 + 0.172);"
    nouveau_isole = "impots = baseImposable * (0.30 + 0.186); // prelevements sociaux 18,6% (2026)"
    while ancien_isole in contenu:
        contenu = contenu.replace(ancien_isole, nouveau_isole, 1)
        nb_modifs += 1

    if nb_modifs == 0:
        print("✅ Déjà corrigé ou texte non trouvé.")
        return

    with open(FICHIER + ".bak_prelevsociaux2026", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} occurrence(s) corrigée(s) : prélèvements sociaux 17,2% -> 18,6%")


if __name__ == "__main__":
    main()
