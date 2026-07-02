#!/usr/bin/env python3
"""
Ajoute la navigation "Article precedent / Article suivant" sur TOUS
les articles du site, dans l'ordre numerique (article-1 -> article-2
-> ... -> article-527), exactement comme sur index.html.

Structure inseree (reprend le format deja existant sur les 36
articles qui l'avaient) :

<div class="article-nav">
  <a class="art-nav-btn" href="article-N.html">
    <span class="nav-label">← Article precedent</span>
    <span class="nav-title">{titre reel}</span>
  </a>
  <a class="art-nav-btn next" href="article-M.html">
    <span class="nav-label">Article suivant →</span>
    <span class="nav-title">{titre reel}</span>
  </a>
</div>

Le premier article n'a pas de "precedent", le dernier n'a pas de
"suivant" (le bloc s'adapte, un seul lien affiche dans ce cas).

Idempotent : ne retouche pas un fichier qui contient deja
'article-nav'. Sauvegardes .bak_nav avant modification.
"""

import glob
import re
import shutil

def get_title(contenu):
    m = re.search(r'<title>(.*?)</title>', contenu, re.DOTALL)
    if not m:
        return "Article Economya.fr"
    titre = m.group(1)
    titre = re.sub(r'\s*—\s*Economya\.fr\s*$', '', titre).strip()
    return titre


def main():
    # on ne prend que les vrais articles numerotes, on exclut les
    # doublons de test (article-XXX-test.html)
    fichiers = glob.glob('article-*.html')
    articles = []
    for f in fichiers:
        m = re.match(r'article-(\d+)\.html$', f)
        if m:
            articles.append((int(m.group(1)), f))
    articles.sort(key=lambda x: x[0])

    print(f"{len(articles)} articles numerotes trouves (de article-{articles[0][0]} a article-{articles[-1][0]})")

    # cache des titres
    titres = {}
    for num, f in articles:
        with open(f, 'r', encoding='utf-8') as fh:
            c = fh.read()
        titres[f] = get_title(c)

    traites = 0
    deja_bon = 0
    erreurs = []

    for i, (num, f) in enumerate(articles):
        with open(f, 'r', encoding='utf-8') as fh:
            contenu = fh.read()

        if 'article-nav' in contenu:
            deja_bon += 1
            continue

        prev_html = ""
        if i > 0:
            prev_f = articles[i-1][1]
            prev_html = f'''<a class="art-nav-btn" href="{prev_f}">
    <span class="nav-label">← Article précédent</span>
    <span class="nav-title">{titres[prev_f]}</span>
  </a>'''

        next_html = ""
        if i < len(articles) - 1:
            next_f = articles[i+1][1]
            next_html = f'''<a class="art-nav-btn next" href="{next_f}">
    <span class="nav-label">Article suivant →</span>
    <span class="nav-title">{titres[next_f]}</span>
  </a>'''

        nav_bloc = f'''
<div class="article-nav">
  {prev_html}
  {next_html}
</div>
'''

        if '<footer>' in contenu:
            contenu_new = contenu.replace('<footer>', nav_bloc + '\n<footer>', 1)
        else:
            erreurs.append(f)
            continue

        shutil.copy2(f, f + '.bak_nav')
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(contenu_new)
        traites += 1

    print(f"\nNav ajoutee : {traites}")
    print(f"Deja bon (ignores) : {deja_bon}")
    print(f"Erreurs (pas de <footer> trouve) : {len(erreurs)}")
    if erreurs:
        print(erreurs[:20])


if __name__ == '__main__':
    main()
