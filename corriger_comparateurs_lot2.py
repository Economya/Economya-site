#!/usr/bin/env python3
"""
Corrige 2 problèmes dans comparateurs.html :
1. Lien cassé : carte "Banque en ligne vs traditionnelle" pointait vers
   article-182.html (jardinage) au lieu de article-187.html (banques).
2. Texte obsolète : "Néobanques 2025" -> "Néobanques 2026"
   (l'article cible article-410.html s'appelle bien "Néobanques 2026").

Idempotent : si déjà corrigé, ne fait rien.
Sauvegarde .bak_fixcomparateurs avant modification.
"""

import os
import shutil

FICHIER = "comparateurs.html"

REMPLACEMENTS = [
    (
        '<a href="article-182.html" class="comp-card">',
        '<a href="article-187.html" class="comp-card">',
    ),
    (
        'comp-name">Néobanques 2025',
        'comp-name">Néobanques 2026',
    ),
]


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier introuvable : {FICHIER}")
        print("   Assurez-vous d'être dans le dossier ~/Desktop/mon site")
        return

    with open(FICHIER, "r", encoding="utf-8") as f:
        contenu = f.read()

    contenu_modifie = contenu
    corrections_appliquees = 0

    for ancien, nouveau in REMPLACEMENTS:
        if ancien in contenu_modifie:
            contenu_modifie = contenu_modifie.replace(ancien, nouveau, 1)
            corrections_appliquees += 1
            print(f"✅ Corrigé : {ancien[:50]}... -> {nouveau[:50]}...")
        elif nouveau in contenu_modifie:
            print(f"ℹ️  Déjà corrigé (idempotent) : {nouveau[:50]}...")
        else:
            print(f"⚠️  Chaîne attendue non trouvée : {ancien[:50]}...")

    if corrections_appliquees == 0:
        print("✅ Rien à faire — le fichier est déjà à jour.")
        return

    shutil.copy2(FICHIER, FICHIER + ".bak_fixcomparateurs")

    with open(FICHIER, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)

    print(f"\n✅ {corrections_appliquees} correction(s) appliquée(s) dans {FICHIER}")
    print(f"   Sauvegarde créée : {FICHIER}.bak_fixcomparateurs")


if __name__ == "__main__":
    main()
