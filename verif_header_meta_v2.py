import glob
import re

fichiers = sorted(glob.glob('article-*.html'))

# Regex plus permissif : "Lecture" suivi (avec ou sans ":") d'un chiffre
lecture_re = re.compile(r'Lecture\s*:?\s*\d')
verifie_re = re.compile(r'V[ée]rifi[ée]\s*juin\s*2026')
hero_re = re.compile(r'class="article-hero"')
old_hero_re = re.compile(r'class="hero"')

has_lecture = 0
has_verifie = 0
has_both = 0
vraiment_vide = []
vieux_gabarit = []

for f in fichiers:
    c = open(f, encoding='utf-8').read()
    lecture = bool(lecture_re.search(c))
    verifie = bool(verifie_re.search(c))
    has_article_hero = bool(hero_re.search(c))
    has_old_hero = bool(old_hero_re.search(c)) and not has_article_hero

    if lecture:
        has_lecture += 1
    if verifie:
        has_verifie += 1
    if lecture and verifie:
        has_both += 1

    if not lecture and not verifie:
        if has_old_hero:
            vieux_gabarit.append(f)
        else:
            vraiment_vide.append(f)

print(f"Total articles : {len(fichiers)}")
print(f"Avec 'Lecture' (regex corrige) : {has_lecture}")
print(f"Avec 'Verifie juin 2026' : {has_verifie}")
print(f"Avec les deux : {has_both}")
print()
print(f"Vieux gabarit (class='hero', pages speciales type recap) : {len(vieux_gabarit)}")
print(vieux_gabarit[:15])
print()
print(f"Vraiment vides (article-hero mais sans meta du tout) : {len(vraiment_vide)}")
print(vraiment_vide[:15])
