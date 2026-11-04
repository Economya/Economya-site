import re, glob, shutil

fichiers = sorted(glob.glob('article-*.html'))

ANCIEN = '· <a href="index.html">Accueil</a> · Cet site contient des liens partenaires.'
NOUVEAU = ('· <a href="mentions-legales.html">Mentions légales</a> · '
           '<a href="politique-confidentialite.html">Politique de confidentialité</a> · '
           '<a href="contact.html">Contact</a> · Economya peut percevoir une commission '
           'sur certains liens présents sur ce site, sans coût supplémentaire pour vous.')

traites = 0
deja_bon = 0
non_trouve = []

for f in fichiers:
    c = open(f, encoding='utf-8').read()
    if NOUVEAU in c:
        deja_bon += 1
        continue
    if ANCIEN in c:
        c_new = c.replace(ANCIEN, NOUVEAU, 1)
        shutil.copy2(f, f + '.bak_footer110')
        open(f, 'w', encoding='utf-8').write(c_new)
        traites += 1
    else:
        non_trouve.append(f)

print(f"Footers corriges : {traites}")
print(f"Deja bons : {deja_bon}")
print(f"Non trouves (a verifier manuellement) : {len(non_trouve)}")
if non_trouve:
    print(non_trouve[:20])
