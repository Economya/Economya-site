import glob

fichiers = sorted(glob.glob('article-*.html'))
sans_footer_tag = []
sans_footer_texte = []

for f in fichiers:
    c = open(f, encoding='utf-8').read()
    if '<footer>' not in c and '<footer ' not in c:
        sans_footer_tag.append(f)
    if 'Economya.fr' not in c.split('<footer', 1)[-1] if '<footer' in c else True:
        # verification alternative : le mot Economya.fr apparait-il apres la derniere balise footer
        pass

print(f"Total articles : {len(fichiers)}")
print(f"SANS balise <footer> du tout : {len(sans_footer_tag)}")
print(sans_footer_tag[:30])
