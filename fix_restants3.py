#!/usr/bin/env python3
"""
Corrige 2 problemes trouves lors du dernier lot d'audit qualite
(restants3, dernier lot de la couverture complete des 527 articles) :

1. article-380.html (Ados et argent de poche) : exemple utilisant
   "2,4% d'interets" pour le Livret A - taux obsolete, doit etre 1,5%.

2. article-414.html (Identite numerique volee) : meme URL cassee que
   celle deja corrigee sur article-413 - "plainte-en-ligne.masse.fr"
   au lieu de "plainte-en-ligne.masecurite.interieur.gouv.fr".

Idempotent. Sauvegardes .bak_restants3 avant modification.
"""

import os
import shutil

CORRECTIONS = {
    "article-380.html": [
        (
            "Si tu épargnes 50 € par mois pendant 10 ans avec 2,4 % d'intérêts",
            "Si tu épargnes 50 € par mois pendant 10 ans avec 1,5 % d'intérêts",
        ),
    ],
    "article-414.html": [
        (
            "plainte-en-ligne.masse.fr",
            "plainte-en-ligne.masecurite.interieur.gouv.fr",
        ),
    ],
}


def corriger_fichier(fichier, remplacements):
    if not os.path.exists(fichier):
        print(f"  Fichier introuvable : {fichier} (ignore)")
        return

    with open(fichier, "r", encoding="utf-8") as f:
        contenu = f.read()

    contenu_modifie = contenu
    total = 0

    for ancien, nouveau in remplacements:
        if ancien in contenu_modifie:
            contenu_modifie = contenu_modifie.replace(ancien, nouveau, 1)
            print(f"  OK Corrige : {ancien[:55]}...")
            total += 1
        elif nouveau in contenu_modifie:
            print(f"  INFO Deja corrige (idempotent) : {nouveau[:55]}...")
        else:
            print(f"  ATTENTION chaine non trouvee : {ancien[:55]}...")

    if total == 0:
        print(f"  -> Rien a faire pour {fichier}.")
        return

    shutil.copy2(fichier, fichier + ".bak_restants3")
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)
    print(f"  -> {total} correction(s) ecrite(s) dans {fichier} (sauvegarde creee)\n")


def main():
    for fichier, remplacements in CORRECTIONS.items():
        print(f"=== {fichier} ===")
        corriger_fichier(fichier, remplacements)


if __name__ == "__main__":
    main()
