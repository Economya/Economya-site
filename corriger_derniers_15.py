#!/usr/bin/env python3
"""
Ajoute la ligne meta (Lecture / Verifie / tag) manquante sur les 15
derniers articles sans elle : article-501.html a article-515.html.
Ces articles ont deja hero-cat + hero-badge, juste pas de hero-meta.

Temps de lecture calcule depuis le nombre de mots reels de l'article.
Idempotent. Sauvegardes .bak_meta15 avant modification.
"""

import re
import shutil

FICHIERS = [f"article-{i}.html" for i in range(501, 516)]

PATTERN = re.compile(
    r'(<div class="hero-badge">.*?</div>)(\s*</div>)',
    re.DOTALL
)


def calculer_lecture(texte):
    mots = len(re.findall(r'\w+', texte))
    return max(2, round(mots / 200))


def main():
    traites = 0
    for f in FICHIERS:
        try:
            with open(f, 'r', encoding='utf-8') as fh:
                contenu = fh.read()
        except FileNotFoundError:
            print(f"  Fichier introuvable : {f} (ignore)")
            continue

        if 'hero-meta' in contenu:
            print(f"  {f} : deja bon (idempotent), rien fait")
            continue

        m = PATTERN.search(contenu)
        if not m:
            print(f"  ATTENTION {f} : structure non reconnue, non modifie")
            continue

        texte_brut = re.sub(r'<[^>]+>', ' ', contenu)
        minutes = calculer_lecture(texte_brut)

        meta_html = f'''
    <div class="hero-meta">
      <span>📖 {minutes} min de lecture</span>
      <span>✅ Vérifié juin 2026</span>
      <span>🇫🇷 Adapté au marché français</span>
    </div>'''

        contenu_new = contenu[:m.end(1)] + meta_html + contenu[m.end(1):m.start(2)] + contenu[m.start(2):]
        # insertion simple : juste apres le hero-badge, avant la fermeture du hero
        contenu_new = PATTERN.sub(lambda mm: mm.group(1) + meta_html + mm.group(2), contenu, count=1)

        shutil.copy2(f, f + '.bak_meta15')
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(contenu_new)
        print(f"  OK {f} : ligne meta ajoutee ({minutes} min)")
        traites += 1

    print(f"\nTotal traite : {traites}")


if __name__ == '__main__':
    main()
