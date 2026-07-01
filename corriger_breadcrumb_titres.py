#!/usr/bin/env python3
"""
Corrige les fils d'Ariane (breadcrumb) et leur JSON-LD associé qui affichent
encore l'ancien titre/année d'un article (ex: "...en 2025") alors que le
vrai titre de l'article a été mis à jour (ex: "...en 2026").

Principe identique à corriger_simcard_titres.py : on extrait le titre
canonique depuis la balise <title> de CHAQUE article, puis on corrige :
1. Le dernier <span> du fil d'Ariane visible
2. L'entrée JSON-LD BreadcrumbList dont l'"item" pointe vers l'article lui-même

Idempotent. Sauvegarde .bak_breadcrumb avant modification de chaque fichier.
"""

import glob
import re
import shutil

TITLE_RE = re.compile(r'<title>(.*?)\s*—\s*Economya\.fr</title>')
BREADCRUMB_SPAN_RE = re.compile(
    r'(<span style="color:var\(--t,#2C2C2A\)">)([^<]*)(</span></div>)'
)


def titre_canonique(contenu):
    m = TITLE_RE.search(contenu)
    return m.group(1).strip() if m else None


def corriger_fichier(fichier):
    with open(fichier, "r", encoding="utf-8") as f:
        contenu = f.read()

    titre = titre_canonique(contenu)
    if not titre:
        return 0

    nb = [0]

    # 1. Span visible du fil d'Ariane
    def remplacer_span(m):
        if m.group(2) != titre:
            nb[0] += 1
            return m.group(1) + titre + m.group(3)
        return m.group(0)

    contenu_modifie = BREADCRUMB_SPAN_RE.sub(remplacer_span, contenu)

    # 2. JSON-LD : entrée dont "item" pointe vers ce fichier lui-même
    nom_fichier_url = f"https://economya.fr/{fichier}"
    jsonld_re = re.compile(
        r'("name": ")([^"]*)(", "item": "'
        + re.escape(nom_fichier_url)
        + r'"\})'
    )

    def remplacer_jsonld(m):
        if m.group(2) != titre:
            nb[0] += 1
            return m.group(1) + titre + m.group(3)
        return m.group(0)

    contenu_modifie = jsonld_re.sub(remplacer_jsonld, contenu_modifie)

    if nb[0] == 0:
        return 0

    shutil.copy2(fichier, fichier + ".bak_breadcrumb")
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)
    return nb[0]


def main():
    total_fichiers = 0
    total_corrections = 0

    for fichier in sorted(glob.glob("article-*.html")):
        n = corriger_fichier(fichier)
        if n > 0:
            total_fichiers += 1
            total_corrections += n
            print(f"  ✅ {fichier} : {n} correction(s)")

    print(f"\n✅ Total : {total_corrections} correction(s) dans {total_fichiers} fichier(s)")
    if total_corrections == 0:
        print("   (idempotent — rien à faire)")


if __name__ == "__main__":
    main()
