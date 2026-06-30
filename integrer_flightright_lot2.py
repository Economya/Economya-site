#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Intégration du partenaire d'affiliation Flightright (indemnisation vols
annulés/retardés) sur 4 articles voyage ciblés supplémentaires
À lancer UNE SEULE FOIS depuis ~/Desktop/mon site

Lien Awin vérifié : awinmid=13334, awinaffid=2926395
Article-276 (Flying Blue) déjà traité séparément aujourd'hui.

Règlement (CE) 261/2004 confirmé : indemnisation jusqu'à 600€/passager
pour vol annulé ou retardé de plus de 3h au départ/arrivée de l'UE.

Insertion juste avant <footer>, ancrage fiable présent sur toutes les
pages. Idempotent. Sauvegarde en .bak_flightright avant modification.

Usage :
    python3 integrer_flightright_lot2.py
"""

import os

FICHIERS_CIBLES = [
    "article-280.html",  # Voyager en famille pour moins de 2000€
    "article-282.html",  # Vacances hors saison
    "article-95.html",   # Voyager avec des miles et des points
    "article-281.html",  # Travel hacking France : cartes bancaires
]

LIEN_AWIN = "https://www.awin1.com/cread.php?awinmid=13334&awinaffid=2926395&ued=https%3A%2F%2Fwww.flightright.fr"

BLOC_FLIGHTRIGHT = f'''
  <div class="tip" style="background:#FAEEDA;border-left:4px solid #EF9F27;color:#633806">
    <strong>✈️ Vol annulé ou retardé ? La loi vous protège</strong>
    Un vol annulé ou retardé de plus de 3 heures au départ ou à l'arrivée de l'UE ouvre droit à une indemnisation pouvant atteindre 600€ par passager (règlement CE 261/2004). <a href="{LIEN_AWIN}" target="_blank" rel="noopener sponsored">Flightright</a> vérifie gratuitement votre éligibilité et gère la procédure de réclamation auprès de la compagnie à votre place. Economya peut percevoir une commission sur ce lien, sans coût supplémentaire pour vous.
  </div>
'''


def traiter_fichier(chemin):
    if not os.path.exists(chemin):
        return "introuvable"

    with open(chemin, 'r', encoding='utf-8') as f:
        contenu = f.read()

    if "Flightright" in contenu:
        return "déjà présent"

    if "<footer>" not in contenu:
        return "pas de footer trouvé"

    with open(chemin + ".bak_flightright", 'w', encoding='utf-8') as f:
        f.write(contenu)

    nouveau_contenu = contenu.replace("<footer>", BLOC_FLIGHTRIGHT + "\n<footer>", 1)

    with open(chemin, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)

    return "intégré"


def main():
    print("=== Intégration Flightright (lot 2, 4 articles) ===\n")
    resultats = {}

    for fichier in FICHIERS_CIBLES:
        statut = traiter_fichier(fichier)
        resultats[fichier] = statut
        symbole = "✅" if statut == "intégré" else "⚠️"
        print(f"{symbole} {fichier} : {statut}")

    nb_integres = sum(1 for s in resultats.values() if s == "intégré")
    print(f"\n=== RÉSUMÉ ===")
    print(f"Fichiers intégrés : {nb_integres}/{len(FICHIERS_CIBLES)}")


if __name__ == "__main__":
    main()
