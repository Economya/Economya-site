#!/usr/bin/env python3
"""
Centre le texte du bandeau d'en-tête (.hi) dans tous les articles utilisant
le template .ah, pour matcher le style déjà centré du template .article-hero
(ex: article-14.html "Carburant").

Ajoute `text-align:center` à la règle CSS `.hi{...}` uniquement si elle
n'a pas déjà cette propriété.

Traite tous les fichiers article-*.html contenant `.ah{` en CSS.

Idempotent : relancer sur des fichiers déjà corrigés ne change rien.
Sauvegarde .bak_centrage_hi avant modification de chaque fichier.
"""

import glob
import os
import re
import shutil

PATTERN_HI = re.compile(r'\.hi\{([^}]*)\}')


def corriger_fichier(fichier):
    with open(fichier, "r", encoding="utf-8") as f:
        contenu = f.read()

    if ".ah{" not in contenu:
        return None  # fichier hors périmètre

    match = PATTERN_HI.search(contenu)
    if not match:
        return "sans_regle_hi"

    regle_interieure = match.group(1)
    if "text-align" in regle_interieure:
        return "deja_ok"

    nouvelle_regle = ".hi{" + regle_interieure.rstrip(";") + ";text-align:center}"
    contenu_modifie = PATTERN_HI.sub(lambda m, nr=nouvelle_regle: nr, contenu, count=1)

    shutil.copy2(fichier, fichier + ".bak_centrage_hi")
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)
    return "corrige"


def main():
    fichiers = sorted(glob.glob("article-*.html"))
    stats = {"corrige": 0, "deja_ok": 0, "sans_regle_hi": 0}

    for fichier in fichiers:
        resultat = corriger_fichier(fichier)
        if resultat is None:
            continue
        stats[resultat] = stats.get(resultat, 0) + 1

    print(f"✅ {stats['corrige']} fichier(s) corrigé(s) (text-align:center ajouté)")
    print(f"ℹ️  {stats['deja_ok']} fichier(s) déjà corrects (idempotent)")
    if stats["sans_regle_hi"]:
        print(f"⚠️  {stats['sans_regle_hi']} fichier(s) avec .ah{{}} mais sans règle .hi{{}} trouvée — à vérifier manuellement")


if __name__ == "__main__":
    main()
