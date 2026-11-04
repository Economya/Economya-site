import glob, shutil

fichiers = sorted(glob.glob('article-*.html'))

# on cherche les liens footer sans style de couleur (bleu par defaut du navigateur)
ANCIENS = [
    '<a href="mentions-legales.html">Mentions légales</a>',
    '<a href="politique-confidentialite.html">Politique de confidentialité</a>',
    '<a href="contact.html">Contact</a>',
]
NOUVEAUX = [
    '<a href="mentions-legales.html" style="color:inherit;text-decoration:underline">Mentions légales</a>',
    '<a href="politique-confidentialite.html" style="color:inherit;text-decoration:underline">Politique de confidentialité</a>',
    '<a href="contact.html" style="color:inherit;text-decoration:underline">Contact</a>',
]

traites = 0
deja_bon = 0

for f in fichiers:
    c = open(f, encoding='utf-8').read()
    if 'color:inherit;text-decoration:underline">Mentions' in c:
        deja_bon += 1
        continue
    c_new = c
    modifie = False
    for ancien, nouveau in zip(ANCIENS, NOUVEAUX):
        if ancien in c_new:
            c_new = c_new.replace(ancien, nouveau)
            modifie = True
    if modifie:
        shutil.copy2(f, f + '.bak_liencolor')
        open(f, 'w', encoding='utf-8').write(c_new)
        traites += 1

print(f"Corriges : {traites}")
print(f"Deja bons : {deja_bon}")
