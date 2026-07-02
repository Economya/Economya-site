#!/usr/bin/env python3
"""
Corrige le style de la nav "Article precedent/suivant" ajoutee sur
491 articles : remplace la structure basee sur des classes CSS qui
n'existaient pas dans leur <style> (donc affichage brut/bleu souligne)
par une version avec style en ligne complet, garantie fonctionnelle
partout.

Idempotent : reconnait sa marque (data-nav-styled) et ne retouche
pas un fichier deja corrige. Sauvegardes .bak_navstyle avant modif.
"""

import re
import glob
import shutil

PATTERN = re.compile(
    r'<div class="article-nav">\s*'
    r'(?:<a class="art-nav-btn" href="([^"]+)">\s*'
    r'<span class="nav-label">(.*?)</span>\s*'
    r'<span class="nav-title">(.*?)</span>\s*'
    r'</a>)?\s*'
    r'(?:<a class="art-nav-btn next" href="([^"]+)">\s*'
    r'<span class="nav-label">(.*?)</span>\s*'
    r'<span class="nav-title">(.*?)</span>\s*'
    r'</a>)?\s*'
    r'</div>',
    re.DOTALL
)

BOX_STYLE = (
    "display:flex;flex-direction:column;gap:.2rem;text-decoration:none;max-width:45%"
)
LABEL_STYLE = (
    "font-size:.7rem;text-transform:uppercase;letter-spacing:.06em;color:var(--m,#8899bb)"
)
TITLE_STYLE = (
    "font-size:.85rem;font-weight:500;color:var(--gd,#085041)"
)


def build_link(href, label, title, align_right=False):
    if not href:
        return '<div></div>'
    align = "text-align:right;align-items:flex-end" if align_right else ""
    return (
        f'<a href="{href}" style="{BOX_STYLE};{align}">'
        f'<span style="{LABEL_STYLE}">{label}</span>'
        f'<span style="{TITLE_STYLE}">{title}</span>'
        f'</a>'
    )


def main():
    fichiers = sorted(glob.glob('article-*.html'))
    traites = 0
    deja_bon = 0
    non_trouve = 0

    for f in fichiers:
        with open(f, 'r', encoding='utf-8') as fh:
            contenu = fh.read()

        if 'data-nav-styled="1"' in contenu:
            deja_bon += 1
            continue

        m = PATTERN.search(contenu)
        if not m:
            non_trouve += 1
            continue

        prev_href, prev_label, prev_title, next_href, next_label, next_title = m.groups()

        prev_html = build_link(prev_href, prev_label, prev_title, align_right=False)
        next_html = build_link(next_href, next_label, next_title, align_right=True)

        nouveau_bloc = (
            '<div class="article-nav" data-nav-styled="1" '
            'style="display:flex;justify-content:space-between;align-items:center;'
            'padding:1.5rem 0;border-top:1px solid var(--b,#e5e5e5);margin-top:3rem;'
            'gap:1rem;flex-wrap:wrap;max-width:900px;margin-left:auto;margin-right:auto;'
            'padding-left:1.5rem;padding-right:1.5rem">'
            f'{prev_html}{next_html}'
            '</div>'
        )

        contenu_new = contenu[:m.start()] + nouveau_bloc + contenu[m.end():]

        shutil.copy2(f, f + '.bak_navstyle')
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(contenu_new)
        traites += 1

    print(f"Nav restylee : {traites}")
    print(f"Deja bon (ignores) : {deja_bon}")
    print(f"Non trouve (structure differente) : {non_trouve}")


if __name__ == '__main__':
    main()
