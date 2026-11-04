import glob

fichiers = sorted(glob.glob('article-*.html'))
trouve = None

for f in fichiers:
    c = open(f, encoding='utf-8').read()
    if 'Vacances en France pas chères' in c and "voiture d'occasion" in c:
        trouve = f
        break

print("Article trouve:", trouve)

if trouve:
    c = open(trouve, encoding='utf-8').read()
    print("Longueur totale du fichier:", len(c))
    print("Contient </html>:", '</html>' in c)
    print("Contient <footer:", '<footer' in c)
    print("Contient </footer>:", '</footer>' in c)
    print()
    idx = c.find('article-nav')
    print("=== Fin du fichier a partir de article-nav ===")
    print(repr(c[idx:idx+1500]))
