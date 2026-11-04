import glob

fichiers = sorted(glob.glob('article-*.html'))
print(f"Total articles : {len(fichiers)}\n")

sans_bon_footer = []

for f in fichiers:
    c = open(f, encoding='utf-8').read()
    a_texte1 = 'Votre meilleur allié finance' in c and 'Fait avec' in c
    a_texte2 = 'Mentions légales' in c and 'Contact' in c
    if not (a_texte1 and a_texte2):
        sans_bon_footer.append(f)

print(f"Articles SANS le bon footer complet : {len(sans_bon_footer)}")
print(sans_bon_footer)
