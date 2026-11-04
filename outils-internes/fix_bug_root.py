import glob, shutil

fichiers = sorted(glob.glob('article-*.html'))
traites = 0
deja_bon = 0

for f in fichiers:
    c = open(f, encoding='utf-8').read()
    modifie = False
    c_new = c

    if ': root{' in c_new:
        c_new = c_new.replace(': root{', ':root{')
        modifie = True
    if ': root {' in c_new:
        c_new = c_new.replace(': root {', ':root {')
        modifie = True

    if modifie:
        shutil.copy2(f, f + '.bak_rootfix')
        open(f, 'w', encoding='utf-8').write(c_new)
        traites += 1
    else:
        deja_bon += 1

print(f"Corriges : {traites}")
print(f"Deja bons : {deja_bon}")
