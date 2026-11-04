import glob

fichiers = sorted(glob.glob('article-*.html'))
problemes = []

for f in fichiers:
    c = open(f, encoding='utf-8').read()
    a_footer_ouvrant = '<footer' in c
    a_footer_fermant = '</footer>' in c
    a_fin_propre = '</html>' in c[-200:] or '</html>' in c

    if not a_footer_ouvrant or not a_footer_fermant or not a_fin_propre:
        raisons = []
        if not a_footer_ouvrant:
            raisons.append("pas de <footer")
        if not a_footer_fermant:
            raisons.append("pas de </footer>")
        if not a_fin_propre:
            raisons.append("fichier tronque (pas de </html>)")
        problemes.append((f, " + ".join(raisons)))

print(f"Total articles : {len(fichiers)}")
print(f"Fichiers avec probleme structurel : {len(problemes)}")
for f, raison in problemes:
    print(f"  {f} : {raison}")
