#!/usr/bin/env python3
"""
Harmonise la 1ere ligne du footer sur les 98 articles qui disaient
"Retour a l'accueil" au lieu de "Votre meilleur allie finance ·
Fait avec coeur en France" (le format cible souhaite).

Ne touche PAS a la 2e ligne (mentions legales/disclaimer), qui varie
legitimement selon le type d'article (informatif vs commission
affiliee) - ce n'est pas un bug, juste du contenu different.

Idempotent. Sauvegardes .bak_footer avant modification.
"""

import glob
import shutil

ANCIEN = '<strong>Economya.fr</strong> · <a href="index.html">Retour à l\'accueil</a><br>'
NOUVEAU = '<strong>Economya.fr</strong> · Votre meilleur allié finance · Fait avec ❤️ en France<br>'


def main():
    fichiers = sorted(glob.glob('article-*.html'))
    traites = 0
    deja_bon = 0

    for f in fichiers:
        with open(f, 'r', encoding='utf-8') as fh:
            contenu = fh.read()

        if ANCIEN not in contenu:
            deja_bon += 1
            continue

        contenu_new = contenu.replace(ANCIEN, NOUVEAU, 1)

        shutil.copy2(f, f + '.bak_footer')
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(contenu_new)
        print(f"  OK {f} : footer harmonise")
        traites += 1

    print(f"\nFooters harmonises : {traites}")
    print(f"Deja bons (ignores) : {deja_bon}")


if __name__ == '__main__':
    main()
