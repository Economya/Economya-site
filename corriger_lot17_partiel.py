#!/usr/bin/env python3
"""
Corrige article-266.html (Leasing social VE) : le seuil de distance
domicile-travail pour l'eligibilite est passe de 15 km a 10 km pour la
3e edition 2026 (confirme service-public.gouv.fr, economie.gouv.fr).

Idempotent. Sauvegarde .bak_lot17 avant modification.
"""

import os
import shutil

FICHIER = "article-266.html"
ANCIEN = "Trajets domicile-travail > 15 km OU pas de TC adaptés"
NOUVEAU = "Trajets domicile-travail > 10 km OU plus de 8 000 km/an pro"


def main():
    if not os.path.exists(FICHIER):
        print(f"Fichier introuvable : {FICHIER}")
        return

    with open(FICHIER, "r", encoding="utf-8") as f:
        contenu = f.read()

    if NOUVEAU in contenu:
        print("Rien a faire - deja corrige (idempotent).")
        return

    if ANCIEN not in contenu:
        print(f"Chaine non trouvee. Verifiez manuellement :")
        print("  grep -n '15 km' article-266.html")
        return

    contenu_modifie = contenu.replace(ANCIEN, NOUVEAU, 1)

    shutil.copy2(FICHIER, FICHIER + ".bak_lot17")
    with open(FICHIER, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)

    print(f"OK 1 correction appliquee dans {FICHIER}")
    print("   15 km (obsolete) -> 10 km (seuil 3e edition 2026)")


if __name__ == "__main__":
    main()
