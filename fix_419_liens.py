import glob, shutil

fichiers = sorted(glob.glob('article-*.html'))

ANCIEN = 'Mentions légales · Contact ·'
NOUVEAU = (
    '<a href="mentions-legales.html" style="color:inherit;text-decoration:underline">Mentions légales</a> · '
    '<a href="politique-confidentialite.html" style="color:inherit;text-decoration:underline">Politique de confidentialité</a> · '
    '<a href="contact.html" style="color:inherit;text-decoration:underline">Contact</a> ·'
)

traites = 0
deja_bon = 0
non_trouve = []

for f in fichiers:
    c = open(f, encoding='utf-8').read()
    if '<a href="mentions-legales.html"' in c and '<a href="politique-confidentialite.html"' in c and '<a href="contact.html"' in c:
        deja_bon += 1
        continue
    if ANCIEN in c:
        c_new = c.replace(ANCIEN, NOUVEAU, 1)
        shutil.copy2(f, f + '.bak_liens419')
        open(f, 'w', encoding='utf-8').write(c_new)
        traites += 1
    else:
        non_trouve.append(f)

print(f"Corriges : {traites}")
print(f"Deja bons : {deja_bon}")
print(f"Non trouves (a verifier) : {len(non_trouve)}")
if non_trouve:
    print(non_trouve[:20])
