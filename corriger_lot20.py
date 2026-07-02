#!/usr/bin/env python3
"""
Corrige 3 problemes trouves lors de l'audit qualite (lot 20, dernier lot) :

1. article-37.html (Epargner 100e/mois) : incoherence interne, "Livret A
   3% garanti" alors que le meme article utilise correctement 1,5% dans
   son propre tableau de simulation juste au-dessus.

2. article-3.html : lien de navigation "Article precedent" residuel avec
   l'ancien titre "2025" d'article-2 (4e type de widget jamais couvert
   par les scripts precedents : nav precedent/suivant, distinct du
   breadcrumb et du sim-card widget).

3. article-430.html (Seuils de revenus) : "77 700 e - Seuil de la flat
   tax" est une confusion avec le plafond micro-BIC LMNP (chiffre
   different, sans rapport avec le PFU qui n'a pas de seuil de revenu).

Idempotent. Sauvegardes .bak_lot20 avant modification.
"""

import os
import shutil

CORRECTIONS = {
    "article-37.html": [
        (
            "Livret A (votre banque) 3% garanti",
            "Livret A (votre banque) 1,5% garanti",
        ),
    ],
    "article-3.html": [
        (
            "Article précédent Quel fournisseur d'électricité choisir en 2025 ?",
            "Article précédent Quel fournisseur d'électricité choisir en 2026 ?",
        ),
    ],
    "article-430.html": [
        (
            "77 700 € Seuil de la flat tax sur les investissements financiers Le PFU (Prélèvement Forfaitaire Unique) de 31,4 % (depuis 2026) s'applique sur les revenus financiers (dividendes, plus-values). Option pour le barème progressif si votre taux marginal est inférieur à 30 %.",
            "— Pas de seuil pour la flat tax Le PFU (Prélèvement Forfaitaire Unique) de 31,4 % (depuis 2026) s'applique sur tous les revenus financiers (dividendes, plus-values), quel que soit leur montant. Option pour le barème progressif si votre taux marginal est inférieur à 30 %.",
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

    shutil.copy2(fichier, fichier + ".bak_lot20")
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)
    print(f"  -> {total} correction(s) ecrite(s) dans {fichier} (sauvegarde creee)\n")


def main():
    for fichier, remplacements in CORRECTIONS.items():
        print(f"=== {fichier} ===")
        corriger_fichier(fichier, remplacements)


if __name__ == "__main__":
    main()
