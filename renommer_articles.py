import os
import re
import shutil

dossier = os.path.dirname(os.path.abspath(__file__))
print("🔍 Analyse du dossier...")

# Lister tous les fichiers HTML
fichiers = [f for f in os.listdir(dossier) if f.lower().endswith('.html') and f.lower() != 'index.html']

# Construire le mapping ancien nom → nouveau nom
mapping = {}
conflits = {}

for nom in fichiers:
    m = re.search(r"(\d+)", nom)
    if not m:
        continue
    num = int(m.group(1))
    nouveau = f"article-{num}.html"
    
    if nouveau in conflits:
        conflits[nouveau].append(nom)
    else:
        conflits[nouveau] = [nom]

print(f"📁 {len(fichiers)} fichiers HTML trouvés")
print(f"📝 {len(conflits)} articles uniques")

# Vérifier les conflits
vrais_conflits = {k: v for k, v in conflits.items() if len(v) > 1}
if vrais_conflits:
    print(f"⚠️  {len(vrais_conflits)} conflits (2 fichiers pour le même numéro) :")
    for cible, sources in list(vrais_conflits.items())[:5]:
        print(f"   {cible} ← {sources}")
    print("   → Le premier fichier sera gardé, les doublons ignorés.")

# Renommer
renommes = 0
ignores = 0
deja_bons = 0

for nouveau, sources in sorted(conflits.items(), key=lambda x: int(re.search(r"\d+", x[0]).group())):
    source = sources[0]  # Prendre le premier en cas de conflit
    ancien_chemin = os.path.join(dossier, source)
    nouveau_chemin = os.path.join(dossier, nouveau)
    
    if source == nouveau:
        deja_bons += 1
        continue
    
    if os.path.exists(nouveau_chemin):
        ignores += 1
        continue
    
    os.rename(ancien_chemin, nouveau_chemin)
    renommes += 1

print(f"\n✅ {renommes} fichiers renommés")
print(f"ℹ️  {deja_bons} fichiers avaient déjà le bon nom")
print(f"ℹ️  {ignores} fichiers ignorés (conflit)")
print(f"\n🎉 Vos articles s'appellent maintenant article-1.html, article-2.html, etc.")
input("\nAppuyez sur Entrée pour fermer...")
