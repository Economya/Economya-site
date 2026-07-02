#!/usr/bin/env python3
"""
Corrige le centrage de la ligne meta ajoutee sur les 15 articles
501 a 515. Remplace la div hero-meta (sans style garanti) par une
version avec style en ligne qui force le centrage, peu importe le
CSS existant de la page (les styles en ligne priment toujours).

Idempotent : reconnait sa propre marque (data-centered) et ne
retouche pas un fichier deja corrige.
Sauvegardes .bak_centrage avant modification.
"""

import re
import shutil

FICHIERS = [f"article-{i}.html" for i in range(501, 516)]

PATTERN = re.compile(
    r'<div class="hero-meta">\s*'
    r'<span>(.*?)</span>\s*'
    r'<span>(.*?)</span>\s*'
    r'<span>(.*?)</span>\s*'
    r'</div>',
    re.DOTALL
)


def main():
    traites = 0
    for f in FICHIERS:
        try:
            with open(f, 'r', encoding='utf-8') as fh:
                contenu = fh.read()
        except FileNotFoundError:
            print(f"  Fichier introuvable : {f} (ignore)")
            continue

        if 'data-centered="1"' in contenu:
            print(f"  {f} : deja centre (idempotent), rien fait")
            continue

        m = PATTERN.search(contenu)
        if not m:
            print(f"  ATTENTION {f} : bloc hero-meta non trouve tel quel, non modifie")
            continue

        s1, s2, s3 = m.group(1), m.group(2), m.group(3)

        nouveau_bloc = (
            '<div class="hero-meta" data-centered="1" '
            'style="display:flex;justify-content:center;align-items:center;'
            'flex-wrap:wrap;gap:1rem;text-align:center;width:100%;margin-top:.8rem">'
            f'<span>{s1}</span>'
            f'<span>{s2}</span>'
            f'<span>{s3}</span>'
            '</div>'
        )

        contenu_new = contenu[:m.start()] + nouveau_bloc + contenu[m.end():]

        shutil.copy2(f, f + '.bak_centrage')
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(contenu_new)
        print(f"  OK {f} : centrage force")
        traites += 1

    print(f"\nTotal traite : {traites}")


if __name__ == '__main__':
    main()
