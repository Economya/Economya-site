#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ajout du disclaimer simulateurs sur les outils de calcul/estimation
À lancer UNE SEULE FOIS depuis le dossier ~/Desktop/mon site

Insère le disclaimer juste avant le bandeau cookies (donc avant </body>)
sur la liste de fichiers ci-dessous.

Sans danger à relancer (idempotent). Sauvegarde en .bak_disclaimer avant modification.

Usage :
    python3 ajouter_disclaimer_simulateurs.py
"""

import os

FICHIERS = [
    "calculateur-budget.html",
    "calculateur-capacite-emprunt.html",
    "calculateur-cout-voiture.html",
    "calculateur-frais-notaire.html",
    "calculateur-impot.html",
    "calculateur-prime-activite.html",
    "calculateur-rendement-locatif.html",
    "calculateur-salaire.html",
    "comparateur-livrets.html",
    "generateur-budget.html",
    "generateur-defi-epargne.html",
    "simulateur-apl.html",
    "simulateur-credit-immo.html",
    "simulateur-economies-energie.html",
    "simulateur-epargne.html",
    "simulateur-loyer-achat.html",
    "simulateur-retraite.html",
    "investisseur-virtuel.html",
    "finance-wrapped.html",
    "inflation-run.html",
    "aura-financiere.html",
    "jackpot-finance.html",
    "boite-economies.html",
    "le-bon-deal.html",
    "le-negociateur.html",
    "checklist-abonnements.html",
    "roue-economies.html",
]

DISCLAIMER = '''<div class="economya-disclaimer-simulateur" style="font-size:0.8rem;color:#5F5E5A;background:#f7f7f5;border-left:3px solid #1D9E75;padding:10px 14px;margin:1.5rem auto;max-width:680px;line-height:1.5;">
Les résultats fournis par cet outil sont donnés à titre indicatif et n'ont pas de valeur contractuelle. Ils sont basés sur les informations renseignées et des hypothèses générales qui peuvent ne pas correspondre à votre situation exacte. Nous recommandons de vérifier ces estimations auprès d'un professionnel avant toute décision financière.
</div>'''


def traiter_fichier(chemin):
    if not os.path.exists(chemin):
        return "introuvable"

    with open(chemin, 'r', encoding='utf-8') as f:
        contenu = f.read()

    if "economya-disclaimer-simulateur" in contenu:
        return "déjà présent"

    if "</body>" not in contenu:
        return "pas de </body> trouvé"

    contenu_modifie = contenu.replace("</body>", DISCLAIMER + "\n</body>", 1)

    with open(chemin + ".bak_disclaimer", 'w', encoding='utf-8') as f:
        f.write(contenu)

    with open(chemin, 'w', encoding='utf-8') as f:
        f.write(contenu_modifie)

    return "ajouté"


def main():
    resultats = {"ajouté": 0, "déjà présent": 0, "introuvable": 0, "pas de </body> trouvé": 0}
    details_introuvables = []

    for fichier in FICHIERS:
        statut = traiter_fichier(fichier)
        resultats[statut] = resultats.get(statut, 0) + 1
        if statut == "introuvable":
            details_introuvables.append(fichier)

    print(f"\n=== RÉSUMÉ ===")
    print(f"Fichiers ajoutés : {resultats['ajouté']}")
    print(f"Déjà présents (ignorés) : {resultats['déjà présent']}")
    print(f"Introuvables : {resultats['introuvable']}")
    if details_introuvables:
        for f in details_introuvables:
            print(f"  ⚠️  {f}")
    print(f"\nSauvegardes créées avec l'extension .bak_disclaimer")


if __name__ == "__main__":
    main()
