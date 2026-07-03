import glob

fichiers = sorted(glob.glob('article-*.html'))
print(f"Total articles : {len(fichiers)}\n")

variantes = {}

for f in fichiers:
    c = open(f, encoding='utf-8').read()
    idx = c.find('<footer')
    if idx == -1:
        cle = "AUCUN_FOOTER"
    else:
        bloc = c[idx:idx+400]
        a_mentions = 'Mentions légales' in bloc
        a_contact = '>Contact<' in bloc
        if a_mentions and a_contact:
            cle = "COMPLET (Mentions+Contact)"
        else:
            cle = "INCOMPLET"
    variantes.setdefault(cle, []).append(f)

for cle, files in variantes.items():
    print(f"{cle} : {len(files)} articles")

print()
print("=== Liste des INCOMPLETS ===")
print(variantes.get("INCOMPLET", []))
