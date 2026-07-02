#!/usr/bin/env python3
"""
Corrige article-308.html (Conge parental) : le tableau recapitulatif
PreParE 2026 contredisait les cartes plus haut dans le meme article
(432e/278e/596e/195e dans le tableau vs 459,70e/297,17e/751,40e dans
les cartes). Confirme par sources officielles multiples (avis-parents.com,
lespetitsculottes.com, droit-finances.commentcamarche.com) : les valeurs
correctes 2026 sont celles des cartes.

Idempotent. Sauvegarde .bak_restants2 avant modification.
"""

import os
import shutil

FICHIER = "article-308.html"

CORRECTIONS = [
    ("432 €/mois", "459,70 €/mois"),
    ("278 €/mois", "297,17 €/mois"),
    ("596 €/mois", "751,40 €/mois"),
    ("195 €/mois", "171,42 €/mois"),
]


def main():
    if not os.path.exists(FICHIER):
        print(f"Fichier introuvable : {FICHIER}")
        return

    with open(FICHIER, "r", encoding="utf-8") as f:
        contenu = f.read()

    contenu_modifie = contenu
    total = 0

    for ancien, nouveau in CORRECTIONS:
        if ancien in contenu_modifie:
            n = contenu_modifie.count(ancien)
            contenu_modifie = contenu_modifie.replace(ancien, nouveau)
            print(f"  OK Corrige ({n}x) : {ancien} -> {nouveau}")
            total += n
        elif nouveau in contenu_modifie:
            print(f"  INFO Deja corrige (idempotent) : {nouveau}")
        else:
            print(f"  ATTENTION chaine non trouvee : {ancien}")

    if total == 0:
        print("Rien a faire.")
        return

    shutil.copy2(FICHIER, FICHIER + ".bak_restants2")
    with open(FICHIER, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)
    print(f"-> {total} correction(s) ecrite(s), sauvegarde creee.")


if __name__ == "__main__":
    main()
