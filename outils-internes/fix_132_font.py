import shutil

FICHIER = "article-132.html"
ANCIEN = 'sans coût supplémentaire pour vous.</span>\n</font>'
NOUVEAU = 'sans coût supplémentaire pour vous.</span>\n</footer>'

c = open(FICHIER, encoding='utf-8').read()

if '</footer>' in c and ANCIEN not in c:
    print("Deja corrige (idempotent).")
elif ANCIEN in c:
    c_new = c.replace(ANCIEN, NOUVEAU, 1)
    shutil.copy2(FICHIER, FICHIER + '.bak_font132')
    open(FICHIER, 'w', encoding='utf-8').write(c_new)
    print("OK : </font> remplace par </footer>")
else:
    print("Chaine non trouvee, verifier manuellement")
