#!/usr/bin/env python3
"""
Corrige 3 problemes trouves lors de l'audit qualite (lot 20, dernier lot)
avec le HTML exact confirme.

1. article-37.html : "3% garanti" pour le Livret A -> "1,5% garanti"
   (incoherent avec le reste du meme article qui utilise 1,5%).

2. article-3.html : lien "Article precedent" residuel avec l'ancien
   titre 2025 d'article-2 (deja corrige partout ailleurs sauf ici).

3. article-430.html : le "seuil de 77 700 e" attribue a la flat tax est
   en realite le plafond micro-BIC LMNP, sans rapport avec le PFU qui
   n'a pas de seuil de revenu. Remplace par un texte correct.

Idempotent. Sauvegardes .bak_lot20final avant modification.
"""

import os
import shutil

CORRECTIONS = {
    "article-37.html": [
        (
            '<div class="app-name">Livret A (votre banque)</div>\n      <div class="app-tag">3% garanti</div>',
            '<div class="app-name">Livret A (votre banque)</div>\n      <div class="app-tag">1,5% garanti</div>',
        ),
    ],
    "article-3.html": [
        (
            '<span class="nav-title">Quel fournisseur d\'électricité choisir en 2025 ?</span>',
            '<span class="nav-title">Quel fournisseur d\'électricité choisir en 2026 ?</span>',
        ),
    ],
    "article-430.html": [
        (
            '<div class="s-montant">77 700 €</div>\n      <div class="s-body">\n        <h3>Seuil de la flat tax sur les investissements financiers</h3>\n        <p>Le PFU (Prélèvement Forfaitaire Unique) de 31,4 % (depuis 2026) s\'applique sur les revenus financiers (dividendes, plus-values). Option pour le barème progressif si votre taux marginal est inférieur à 30 %.</p>',
            '<div class="s-montant">—</div>\n      <div class="s-body">\n        <h3>Pas de seuil pour la flat tax</h3>\n        <p>Le PFU (Prélèvement Forfaitaire Unique) de 31,4 % (depuis 2026) s\'applique sur tous les revenus financiers (dividendes, plus-values), quel que soit leur montant. Option pour le barème progressif si votre taux marginal est inférieur à 30 %.</p>',
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

    shutil.copy2(fichier, fichier + ".bak_lot20final")
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)
    print(f"  -> {total} correction(s) ecrite(s) dans {fichier} (sauvegarde creee)\n")


def main():
    for fichier, remplacements in CORRECTIONS.items():
        print(f"=== {fichier} ===")
        corriger_fichier(fichier, remplacements)


if __name__ == "__main__":
    main()
