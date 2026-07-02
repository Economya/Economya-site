import re, glob
fichiers = sorted(glob.glob('article-*.html'))
for f in fichiers:
    c = open(f, encoding='utf-8').read()
    verifie = re.search(r'V[ée]rifi[ée]\s*juin\s*2026', c)
    lecture = re.search(r'Lecture\s*\d', c)
    if verifie and not lecture:
        idx = verifie.start()
        print(f"=== FICHIER: {f} ===")
        print(c[max(0,idx-900):idx+400])
        break
