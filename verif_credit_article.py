import glob

fichiers = sorted(glob.glob('article-*.html'))
trouve = None

for f in fichiers:
    c = open(f, encoding='utf-8').read()
    if 'Téléphonie mobile' in c and 'Jardinage et potager' in c:
        trouve = f
        break

print("Article trouve:", trouve)

if trouve:
    c = open(trouve, encoding='utf-8').read()
    idx = c.find('<footer')
    print(repr(c[idx:idx+500]))
