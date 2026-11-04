import glob

fichiers = sorted(glob.glob('article-*.html'))
sans_vrais_liens = []

for f in fichiers:
    c = open(f, encoding='utf-8').read()
    idx = c.find('<footer')
    if idx == -1:
        continue
    bloc = c[idx:idx+500]
    # un vrai lien Mentions legales doit avoir une balise <a autour
    a_lien_mentions = '<a href="mentions-legales.html"' in bloc
    a_lien_politique = '<a href="politique-confidentialite.html"' in bloc
    a_lien_contact = '<a href="contact.html"' in bloc
    if not (a_lien_mentions and a_lien_politique and a_lien_contact):
        sans_vrais_liens.append(f)

print(f"Total articles : {len(fichiers)}")
print(f"SANS les 3 vrais liens cliquables : {len(sans_vrais_liens)}")
print(sans_vrais_liens)
