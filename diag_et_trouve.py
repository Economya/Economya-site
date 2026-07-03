import glob

# 1. Diagnostiquer article-132
c = open('article-132.html', encoding='utf-8').read()
idx = c.find('<footer')
print("=== article-132 : contexte du footer ===")
print(repr(c[max(0,idx-50):idx+800]))
print()

# 2. Trouver l'article marathon
fichiers = sorted(glob.glob('article-*.html'))
trouve = None
for f in fichiers:
    c2 = open(f, encoding='utf-8').read()
    if 'Participer à un marathon' in c2 and 'CV et lettres de motivation' in c2:
        trouve = f
        break

print(f"=== Article marathon trouve : {trouve} ===")
if trouve:
    c2 = open(trouve, encoding='utf-8').read()
    idx2 = c2.find('<footer')
    if idx2 == -1:
        print("PAS DE BALISE FOOTER DU TOUT")
    else:
        print(repr(c2[idx2:idx2+600]))
