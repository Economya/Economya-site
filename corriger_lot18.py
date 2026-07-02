#!/usr/bin/env python3
"""
Corrige 3 problemes trouves lors de l'audit qualite (lot 18) :

1. article-2.html : fil d'Ariane residuel "en 2025" (le title et le h1
   disent deja 2026, seul le breadcrumb n'avait pas ete corrige).

2. article-43.html : typo "Tioir par tiroir" -> "Tiroir par tiroir".

3. article-96.html : "statut d'auto-entrepreneur simplifie depuis 2015"
   -> le regime auto-entrepreneur existe depuis 2009 (loi de
   modernisation de l'economie), pas 2015. Deja repere au lot 2, corrige
   ici.

Idempotent. Sauvegardes .bak_lot18 avant modification.
"""

import os
import shutil

CORRECTIONS = {
    "article-2.html": [
        (
            "Accueil › Énergie › Quel fournisseur d'électricité choisir en 2025 ?",
            "Accueil › Énergie › Quel fournisseur d'électricité choisir en 2026 ?",
        ),
    ],
    "article-43.html": [
        (
            "Tioir par tiroir",
            "Tiroir par tiroir",
        ),
    ],
    "article-96.html": [
        (
            "Le statut d'auto-entrepreneur simplifié depuis 2015",
            "Le statut d'auto-entrepreneur, créé en 2009,",
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

    shutil.copy2(fichier, fichier + ".bak_lot18")
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)
    print(f"  -> {total} correction(s) ecrite(s) dans {fichier} (sauvegarde creee)\n")


def main():
    for fichier, remplacements in CORRECTIONS.items():
        print(f"=== {fichier} ===")
        corriger_fichier(fichier, remplacements)


if __name__ == "__main__":
    main()
