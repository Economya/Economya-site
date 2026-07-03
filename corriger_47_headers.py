#!/usr/bin/env python3
"""
Corrige le rendu casse des 47 articles "modernises" plus tot dans la
session : leurs balises (article-cat, savings-badge, article-meta,
p.intro) n'avaient aucun CSS associe dans leur propre <style>, donc
s'affichaient en texte brut sans aucune mise en forme.

Remplace par du style en ligne garanti, base sur le VRAI CSS trouve
dans article-1.html (qui fonctionne correctement) :
  .article-hero { fond degrade vert, texte blanc centre }
  .article-cat  { pastille orange transparente }
  .savings-badge{ pastille orange pleine }
  .article-meta { ligne d'infos discrete }

Idempotent : reconnait sa marque (data-hero-fixed) et ne retouche pas
un fichier deja corrige. Sauvegardes .bak_herofix avant modification.
"""

import re
import glob
import shutil

# Les 47 articles modernises dans le lot precedent (class="hero" -> class="article-hero")
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

HERO_STYLE = (
    "background:linear-gradient(135deg,#04342C,#0F6E56 60%,#1D9E75);"
    "color:white;padding:4rem 2rem 3rem;text-align:center"
)
CAT_STYLE = (
    "display:inline-block;background:rgba(239,159,39,0.2);color:#EF9F27;"
    "border:1px solid rgba(239,159,39,0.4);padding:.3rem .9rem;border-radius:50px;"
    "font-size:.75rem;font-weight:500;text-transform:uppercase;margin-bottom:1.2rem"
)
H1_STYLE = "color:white;margin:0"
INTRO_STYLE = "color:rgba(255,255,255,0.85);max-width:640px;margin:1rem auto 0;font-size:1rem"
BADGE_STYLE = (
    "display:inline-block;background:#EF9F27;color:white;padding:.5rem 1.2rem;"
    "border-radius:50px;font-weight:500;font-size:.9rem;margin-top:1.2rem"
)
META_STYLE = (
    "display:flex;justify-content:center;gap:1.5rem;flex-wrap:wrap;"
    "margin-top:1.5rem;font-size:.8rem;color:rgba(255,255,255,0.6)"
)


def main():
    traites = 0
    non_trouve = []
    deja_bon = 0

    for f in FICHIERS:
        try:
            with open(f, 'r', encoding='utf-8') as fh:
                contenu = fh.read()
        except FileNotFoundError:
            print(f"  Fichier introuvable : {f} (ignore)")
            continue

        if 'data-hero-fixed="1"' in contenu:
            deja_bon += 1
            continue

        if 'class="article-hero"' not in contenu:
            non_trouve.append(f)
            continue

        c2 = contenu

        c2 = c2.replace(
            '<div class="article-hero">',
            f'<div class="article-hero" data-hero-fixed="1" style="{HERO_STYLE}">',
            1
        )
        c2 = re.sub(
            r'<div class="article-cat">',
            f'<div class="article-cat" style="{CAT_STYLE}">',
            c2, count=1
        )
        c2 = re.sub(
            r'<h1>',
            f'<h1 style="{H1_STYLE}">',
            c2, count=1
        )
        c2 = re.sub(
            r'<p class="intro">',
            f'<p class="intro" style="{INTRO_STYLE}">',
            c2, count=1
        )
        c2 = re.sub(
            r'<div class="savings-badge">',
            f'<div class="savings-badge" style="{BADGE_STYLE}">',
            c2, count=1
        )
        c2 = re.sub(
            r'<div class="article-meta">',
            f'<div class="article-meta" style="{META_STYLE}">',
            c2, count=1
        )

        if c2 == contenu:
            non_trouve.append(f)
            continue

        shutil.copy2(f, f + '.bak_herofix')
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(c2)
        print(f"  OK {f} : style corrige")
        traites += 1

    print(f"\nHeaders corriges : {traites}")
    print(f"Deja bon (ignores) : {deja_bon}")
    print(f"Structure non reconnue : {len(non_trouve)}")
    if non_trouve:
        print(non_trouve)


if __name__ == '__main__':
    main()
