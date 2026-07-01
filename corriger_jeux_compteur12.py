#!/usr/bin/env python3
"""
Corrige le compteur '10 jeux' -> '12 jeux' dans jeux.html.
Idempotent : si les chaînes '12 jeux' sont déjà présentes, ne fait rien.
Fait une sauvegarde .bak_compteur12 avant modification.
"""

import os
import shutil

FICHIER = "jeux.html"

REMPLACEMENTS = [
    (
        '<meta name="description" content="10 jeux gratuits pour apprendre à gérer votre argent en jouant ! Economya.fr">',
        '<meta name="description" content="12 jeux gratuits pour apprendre à gérer votre argent en jouant ! Economya.fr">',
    ),
    (
        '<p>Apprenez à gérer votre argent en jouant ! 10 jeux gratuits et éducatifs pour devenir un expert des économies.</p>',
        '<p>Apprenez à gérer votre argent en jouant ! 12 jeux gratuits et éducatifs pour devenir un expert des économies.</p>',
    ),
]


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier introuvable : {FICHIER}")
        return

    # Lecture
    with open(FICHIER, "r", encoding="utf-8") as f:
        contenu = f.read()

    corrections_appliquees = 0
    contenu_modifie = contenu

    for ancien, nouveau in REMPLACEMENTS:
        if ancien in contenu_modifie:
            contenu_modifie = contenu_modifie.replace(ancien, nouveau)
            corrections_appliquees += 1
        elif nouveau in contenu_modifie:
            print(f"ℹ️  Déjà corrigé (idempotent) : {nouveau[:60]}...")
        else:
            print(f"⚠️  Chaîne attendue non trouvée : {ancien[:60]}...")

    if corrections_appliquees == 0:
        print("✅ Rien à faire — le fichier est déjà à jour (12 jeux).")
        return

    # Sauvegarde avant écriture
    shutil.copy2(FICHIER, FICHIER + ".bak_compteur12")

    # Écriture (opération séparée de la lecture)
    with open(FICHIER, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)

    print(f"✅ {corrections_appliquees} correction(s) appliquée(s) dans {FICHIER}")
    print(f"   Sauvegarde créée : {FICHIER}.bak_compteur12")


if __name__ == "__main__":
    main()
