#!/usr/bin/env python3
"""
Génère un fichier `_redirects` qui redirige (301, permanent) chaque page
"nom.html" vers sa version sans extension "nom" — SAUF 404.html (page
d'erreur spéciale de Netlify, à ne jamais rediriger) et index.html (qui
est redirigé vers la racine "/" plutôt que vers "/index").

Pourquoi un fichier par ligne plutôt qu'une règle générique ?
Netlify interdit les jokers (*) au milieu d'un chemin (ex: /*.html),
donc il n'existe pas de règle unique pour "toutes les pages .html".
Il faut lister chaque fichier explicitement — ce script le fait à
votre place en lisant le contenu réel de votre dossier.

Utilisation : lancez ce script depuis le dossier "mon site" (celui qui
contient tous vos fichiers .html). Il crée/écrase le fichier `_redirects`
à la racine de ce même dossier.
"""
import glob
import sys

def main():
    html_files = sorted(glob.glob('*.html'))
    if not html_files:
        print("Aucun fichier .html trouvé dans ce dossier.")
        sys.exit(1)

    lines = [
        "# Redirections .html -> sans extension (générées automatiquement)",
        "# Ne pas modifier à la main : relancez generate_redirects.py si besoin.",
        "",
    ]

    count = 0
    for filename in html_files:
        if filename == '404.html':
            continue  # page d'erreur spéciale Netlify : ne jamais rediriger
        name = filename[:-5]  # retire ".html"
        if filename == 'index.html':
            lines.append(f"/index.html   /   301!")
        else:
            lines.append(f"/{filename}   /{name}   301!")
        count += 1

    with open('_redirects', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')

    print(f"Fichier _redirects créé avec {count} redirection(s) "
          f"(sur {len(html_files)} fichiers .html trouvés, 404.html exclu).")

if __name__ == '__main__':
    main()
