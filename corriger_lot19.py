#!/usr/bin/env python3
"""
Corrige 2 problemes trouves lors de l'audit qualite (lot 19) :

1. article-382.html (TDAH et budget) : une balise HTML mal fermee fuite
   dans le texte visible ("class="defi-icon">" apparait litteralement
   sur la page au lieu d'etre une balise fonctionnelle).

2. article-464.html (Desencombrement KonMari) : typo "Tioir par tiroir"
   -> "Tiroir par tiroir" (mal attribue a article-43 au lot precedent,
   corrige ici au bon endroit).

Idempotent. Sauvegardes .bak_lot19 avant modification.
"""

import os
import shutil

CORRECTIONS = {
    "article-382.html": [
        (
            '      class="defi-icon">😤</div>',
            '      <div class="defi-icon">😤</div>',
        ),
    ],
    "article-464.html": [
        (
            "Tioir par tiroir",
            "Tiroir par tiroir",
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

    shutil.copy2(fichier, fichier + ".bak_lot19")
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)
    print(f"  -> {total} correction(s) ecrite(s) dans {fichier} (sauvegarde creee)\n")


def main():
    for fichier, remplacements in CORRECTIONS.items():
        print(f"=== {fichier} ===")
        corriger_fichier(fichier, remplacements)


if __name__ == "__main__":
    main()
