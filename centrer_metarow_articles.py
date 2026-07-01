#!/usr/bin/env python3
"""
Ajoute justify-content:center à la règle CSS .meta-row{display:flex;...}
dans tous les articles utilisant le template .ah, pour centrer la rangée
de badges (durée de lecture, date de vérification, thème) sous le titre.

text-align:center ne suffit pas sur un conteneur flex : il faut
justify-content:center pour centrer les éléments flex horizontalement.

Idempotent. Sauvegarde .bak_centrage_metarow avant modification.
"""

import glob
import re
import shutil

PATTERN_META = re.compile(r'\.meta-row\{([^}]*)\}')


def corriger_fichier(fichier):
    with open(fichier, "r", encoding="utf-8") as f:
        contenu = f.read()

    if ".ah{" not in contenu:
        return None

    match = PATTERN_META.search(contenu)
    if not match:
        return "sans_regle"

    regle_interieure = match.group(1)
    if "justify-content" in regle_interieure:
        return "deja_ok"

    nouvelle_regle = ".meta-row{" + regle_interieure.rstrip(";") + ";justify-content:center}"
    contenu_modifie = PATTERN_META.sub(lambda m, nr=nouvelle_regle: nr, contenu, count=1)

    shutil.copy2(fichier, fichier + ".bak_centrage_metarow")
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)
    return "corrige"


def main():
    fichiers = sorted(glob.glob("article-*.html"))
    stats = {"corrige": 0, "deja_ok": 0, "sans_regle": 0}

    for fichier in fichiers:
        resultat = corriger_fichier(fichier)
        if resultat is None:
            continue
        stats[resultat] = stats.get(resultat, 0) + 1

    print(f"✅ {stats['corrige']} fichier(s) corrigé(s) (justify-content:center ajouté)")
    print(f"ℹ️  {stats['deja_ok']} fichier(s) déjà corrects (idempotent)")
    if stats["sans_regle"]:
        print(f"⚠️  {stats['sans_regle']} fichier(s) sans règle .meta-row{{}} trouvée")


if __name__ == "__main__":
    main()
