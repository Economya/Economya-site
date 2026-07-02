#!/usr/bin/env python3
"""
Centre completement le bloc hero (categorie, titre, bandeau, meta)
sur les 15 articles 501-515, pour matcher le style du reste du site
(comme article-1.html, "Jouer aux jeux video sans se ruiner").

Force le centrage par styles en ligne sur le conteneur ET chaque
enfant (badges en inline-block, texte centre), sans dependre du CSS
existant de la page.

Idempotent : reconnait sa marque (data-hero-centered) et ne retouche
pas un fichier deja corrige. Sauvegardes .bak_herocenter avant modif.
"""

import re
import shutil

FICHIERS = [f"article-{i}.html" for i in range(501, 516)]

# Capture tout le bloc <div class="hero"> ... </div> (non-greedy jusqu'a la 1ere fermeture correspondante)
PATTERN = re.compile(
    r'<div class="hero">(.*?)</div>\s*(?=<div class="container"|<article|<div class="ab")',
    re.DOTALL
)


def centrer_enfants(inner_html):
    # hero-cat : badge pilule centree
    inner_html = re.sub(
        r'<div class="hero-cat">',
        '<div class="hero-cat" style="display:inline-block;margin:0 auto 1rem">',
        inner_html
    )
    # h1 : texte centre
    inner_html = re.sub(
        r'<h1>',
        '<h1 style="text-align:center">',
        inner_html
    )
    # hero-badge : badge pilule centree
    inner_html = re.sub(
        r'<div class="hero-badge">',
        '<div class="hero-badge" style="display:inline-block;margin:1rem auto">',
        inner_html
    )
    # hero-meta : deja centre par notre precedent script, mais on s'assure
    inner_html = re.sub(
        r'<div class="hero-meta"[^>]*>',
        '<div class="hero-meta" style="display:flex;justify-content:center;'
        'align-items:center;flex-wrap:wrap;gap:1rem;text-align:center;'
        'width:100%;margin-top:.8rem">',
        inner_html
    )
    return inner_html


def main():
    traites = 0
    for f in FICHIERS:
        try:
            with open(f, 'r', encoding='utf-8') as fh:
                contenu = fh.read()
        except FileNotFoundError:
            print(f"  Fichier introuvable : {f} (ignore)")
            continue

        if 'data-hero-centered="1"' in contenu:
            print(f"  {f} : deja centre completement (idempotent), rien fait")
            continue

        m = PATTERN.search(contenu)
        if not m:
            print(f"  ATTENTION {f} : bloc hero non trouve tel quel, non modifie")
            continue

        inner = centrer_enfants(m.group(1))

        nouveau_bloc = (
            '<div class="hero" data-hero-centered="1" '
            'style="text-align:center;display:flex;flex-direction:column;'
            'align-items:center">'
            f'{inner}</div>'
        )

        contenu_new = contenu[:m.start()] + nouveau_bloc + contenu[m.end():]

        shutil.copy2(f, f + '.bak_herocenter')
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(contenu_new)
        print(f"  OK {f} : bloc hero entierement centre")
        traites += 1

    print(f"\nTotal traite : {traites}")


if __name__ == '__main__':
    main()
