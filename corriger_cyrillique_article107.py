#!/usr/bin/env python3
"""
Corrige un artefact d'encodage sur article-107.html : le mot "boudera"
contient des caracteres cyrilliques invisibles a la place de "boudera".

Remplacement direct et exact (pas de table generique, pour eviter tout
risque d'erreur de correspondance).

Idempotent. Sauvegarde .bak_cyrillique avant modification.
"""

import os
import shutil

FICHIER = "article-107.html"

ANCIEN = "personne ne boud\u0435\u0440\u0430 \u00e0 table"
NOUVEAU = "personne ne boudera à table"


def main():
    if not os.path.exists(FICHIER):
        print(f"Fichier introuvable : {FICHIER}")
        return

    with open(FICHIER, "r", encoding="utf-8") as f:
        contenu = f.read()

    if NOUVEAU in contenu and ANCIEN not in contenu:
        print("Rien a faire - deja correct (idempotent).")
        return

    if ANCIEN not in contenu:
        print("Chaine corrompue non trouvee. Verifiez manuellement avec :")
        print("  grep -n 'boud' article-107.html")
        return

    contenu_modifie = contenu.replace(ANCIEN, NOUVEAU, 1)

    shutil.copy2(FICHIER, FICHIER + ".bak_cyrillique")
    with open(FICHIER, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)

    print(f"OK corrige dans {FICHIER}")
    print(f"Sauvegarde creee : {FICHIER}.bak_cyrillique")


if __name__ == "__main__":
    main()
