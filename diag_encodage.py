c = open('article-1.html', encoding='utf-8').read()
idx = c.find('meilleur')
print("Position trouvee:", idx)
if idx != -1:
    extrait = c[max(0,idx-20):idx+60]
    print("Extrait:", repr(extrait))
else:
    print("Le mot 'meilleur' n'existe pas du tout dans le fichier !")
    idx2 = c.find('<footer')
    print(repr(c[idx2:idx2+300]))
