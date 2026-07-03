#!/usr/bin/env python3
"""
Ajoute "Jusqu'a" devant les 47 badges d'economies qui affichaient un
chiffre absolu sans nuance (risque juridique : promesse de resultat
non garantie). Reformate aussi la ponctuation (espace avant €).

Idempotent : ne modifie pas un badge qui contient deja un mot de
nuance (jusqu'a, des, environ...). Sauvegardes .bak_nuance avant
modification.
"""

import re
import shutil

FICHIERS = [
    "article-100.html", "article-101.html", "article-105.html", "article-110.html",
    "article-117.html", "article-12.html", "article-121.html", "article-122.html",
    "article-129.html", "article-13.html", "article-131.html", "article-136.html",
    "article-141.html", "article-143.html", "article-155.html", "article-16.html",
    "article-161.html", "article-179.html", "article-18.html", "article-20.html",
    "article-236.html", "article-239.html", "article-250.html", "article-259.html",
    "article-294.html", "article-30.html", "article-301.html", "article-31.html",
    "article-35.html", "article-350.html", "article-359.html", "article-36.html",
    "article-397.html", "article-399.html", "article-407.html", "article-42.html",
    "article-476.html", "article-482.html", "article-54.html", "article-61.html",
    "article-70.html", "article-78.html", "article-79.html", "article-84.html",
    "article-9.html", "article-90.html", "article-95.html",
]

MOTS_NUANCE = ['jusqu', 'dès', 'des ', 'à partir', 'environ', 'en moyenne']
PATTERN = re.compile(r'(class="savings-badge"[^>]*>)([^<]*?)(</div>)', re.DOTALL)


def main():
    traites = 0
    deja_bon = 0
    non_trouve = []

    for f in FICHIERS:
        try:
            with open(f, 'r', encoding='utf-8') as fh:
                contenu = fh.read()
        except FileNotFoundError:
            continue

        m = PATTERN.search(contenu)
        if not m:
            non_trouve.append(f)
            continue

        texte = m.group(2)
        if any(mot in texte.lower() for mot in MOTS_NUANCE):
            deja_bon += 1
            continue

        # separer l'emoji du chiffre : "💰 40%" -> emoji="💰 " reste="40%"
        m2 = re.match(r'^(💰\s*)(.*)$', texte.strip())
        if m2:
            emoji, reste = m2.group(1), m2.group(2)
        else:
            emoji, reste = "💰 ", texte.strip()

        nouveau_texte = f"{emoji}Jusqu'à {reste}"

        contenu_new = contenu[:m.start(2)] + nouveau_texte + contenu[m.end(2):]

        shutil.copy2(f, f + '.bak_nuance')
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(contenu_new)
        print(f"  OK {f} : '{texte.strip()}' -> '{nouveau_texte}'")
        traites += 1

    print(f"\nBadges corriges : {traites}")
    print(f"Deja bons (ignores) : {deja_bon}")
    print(f"Non trouves : {len(non_trouve)}")
    if non_trouve:
        print(non_trouve)


if __name__ == '__main__':
    main()
