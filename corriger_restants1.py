#!/usr/bin/env python3
"""
Corrige 2 problemes trouves lors de l'audit qualite (lot restants1,
premier lot cible sur les 164 articles jamais encore vus) :

1. article-230.html (Primes non imposables) : incoherence interne,
   le plafond titre-restaurant part patronale apparait en 7,18e puis
   7,32e dans le meme article. La valeur confirmee ailleurs sur le
   site (article-27) est 7,32e.

2. article-123.html (Graines germees) : artefact d'encodage, drapeau
   francais corrompu "F + caractere invisible" au lieu du vrai emoji.

Idempotent. Sauvegardes .bak_restants1 avant modification.
"""

import os
import shutil

CORRECTIONS = {
    "article-230.html": [
        (
            "7,18 € par titre (part patronale max)",
            "7,32 € par titre (part patronale max)",
        ),
    ],
    "article-123.html": [
        (
            "🇫🡷 Adapté au marché français",
            "🇫🇷 Adapté au marché français",
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

    shutil.copy2(fichier, fichier + ".bak_restants1")
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)
    print(f"  -> {total} correction(s) ecrite(s) dans {fichier} (sauvegarde creee)\n")


def main():
    for fichier, remplacements in CORRECTIONS.items():
        print(f"=== {fichier} ===")
        corriger_fichier(fichier, remplacements)


if __name__ == "__main__":
    main()
