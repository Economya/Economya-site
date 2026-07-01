#!/usr/bin/env python3
"""
Corrige les titres collés dans le widget "Articles similaires" (sim-card-title)
sur l'ensemble des article-*.html.

Principe : plutôt que de deviner via regex quels titres sont "collés", ce script
extrait le VRAI titre de chaque article depuis sa propre balise <title>, puis
corrige tous les sim-card-title qui pointent vers cet article et qui ne
correspondent pas exactement à ce titre canonique (ex: espace manquant après
un mot suivi de "à", "de", etc.).

Exemple : sim-card-title "Manger équilibréà petit budget" pour un lien vers
article-292.html -> corrigé en "Manger équilibré à petit budget" (le vrai titre
de article-292.html lui-même).

Idempotent : si déjà correct, ne touche rien.
Sauvegarde .bak_simcard avant modification de chaque fichier modifié.
"""

import glob
import os
import re
import shutil

TITLE_RE = re.compile(r'<title>(.*?)\s*—\s*Economya\.fr</title>')
SIMCARD_RE = re.compile(
    r'(<a class="sim-card" href="article-(\d+)\.html"><div class="sim-card-cat">[^<]*</div><div class="sim-card-title">)([^<]*)(</div>)'
)


def construire_titres_canoniques():
    titres = {}
    for fichier in glob.glob("article-*.html"):
        m = re.match(r"article-(\d+)\.html", fichier)
        if not m:
            continue
        num = m.group(1)
        try:
            with open(fichier, "r", encoding="utf-8") as f:
                contenu = f.read()
        except Exception:
            continue
        match = TITLE_RE.search(contenu)
        if match:
            titres[num] = match.group(1).strip()
    return titres


def corriger_fichier(fichier, titres):
    with open(fichier, "r", encoding="utf-8") as f:
        contenu = f.read()

    nb_corrections = [0]

    def remplacer(m):
        prefixe, num, titre_actuel, suffixe = m.group(1), m.group(2), m.group(3), m.group(4)
        titre_correct = titres.get(num)
        if titre_correct and titre_actuel != titre_correct:
            nb_corrections[0] += 1
            return prefixe + titre_correct + suffixe
        return m.group(0)

    contenu_modifie = SIMCARD_RE.sub(remplacer, contenu)

    if nb_corrections[0] == 0:
        return 0

    shutil.copy2(fichier, fichier + ".bak_simcard")
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)
    return nb_corrections[0]


def main():
    print("Construction des titres canoniques...")
    titres = construire_titres_canoniques()
    print(f"{len(titres)} titres de référence trouvés.\n")

    total_fichiers = 0
    total_corrections = 0

    for fichier in sorted(glob.glob("article-*.html")):
        n = corriger_fichier(fichier, titres)
        if n > 0:
            total_fichiers += 1
            total_corrections += n
            print(f"  ✅ {fichier} : {n} titre(s) corrigé(s)")

    print(f"\n✅ Total : {total_corrections} correction(s) dans {total_fichiers} fichier(s)")
    if total_corrections == 0:
        print("   (idempotent — rien à faire)")


if __name__ == "__main__":
    main()
