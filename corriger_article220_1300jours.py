#!/usr/bin/env python3
"""
Corrige le résidu trouvé sur article-220.html (Démission reconversion) :
le champ "Durée : 1826 jours minimum" est incohérent avec le seuil légal
réel de 1300 jours travaillés (déjà correctement mentionné ailleurs dans
le même article : "5 ans (1 300 jours) d'activité salariée continue").

1826 jours = 5 années calendaires pleines, mais la loi compte les jours
réellement TRAVAILLÉS (1300 jours sur 60 mois), pas les jours calendaires.

Idempotent. Sauvegarde .bak_1300jours avant modification.
"""

import os
import shutil

FICHIER = "article-220.html"

ANCIEN = "Durée : 1 826 jours minimum"
NOUVEAU = "Durée : 1 300 jours travaillés minimum (sur 60 mois)"


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier introuvable : {FICHIER}")
        return

    with open(FICHIER, "r", encoding="utf-8") as f:
        contenu = f.read()

    if NOUVEAU in contenu:
        print("✅ Rien à faire — déjà corrigé (idempotent).")
        return

    if ANCIEN not in contenu:
        print(f"⚠️  Chaîne '{ANCIEN}' non trouvée. Vérifiez manuellement :")
        print("   grep -n 'jours minimum' article-220.html")
        return

    contenu_modifie = contenu.replace(ANCIEN, NOUVEAU, 1)

    shutil.copy2(FICHIER, FICHIER + ".bak_1300jours")
    with open(FICHIER, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)

    print(f"✅ 1 correction appliquée dans {FICHIER}")
    print(f"   1 826 jours (calendaires) -> 1 300 jours travaillés")
    print(f"   Sauvegarde créée : {FICHIER}.bak_1300jours")


if __name__ == "__main__":
    main()
