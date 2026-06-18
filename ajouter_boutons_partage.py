import os
import re

dossier = "/Users/alexandregoffinet/Desktop/mon site"
fichiers_modifies = 0
fichiers_erreur = 0

boutons_html = '''
<!-- Boutons partage -->
<div style="background:#fff;border-radius:16px;border:1px solid rgba(0,0,0,0.08);padding:1.2rem 1.5rem;margin:2rem auto;max-width:680px;text-align:center">
  <p style="font-size:.82rem;font-weight:600;color:#5F5E5A;margin-bottom:.8rem;text-transform:uppercase;letter-spacing:.05em">Partager cet article</p>
  <div style="display:flex;gap:.6rem;justify-content:center;flex-wrap:wrap">
    <a href="https://www.facebook.com/sharer/sharer.php?u=URL_PAGE" target="_blank" rel="noopener" style="background:#1877F2;color:white;text-decoration:none;padding:.5rem 1.1rem;border-radius:50px;font-size:.82rem;font-weight:600;display:inline-flex;align-items:center;gap:.4rem">📘 Facebook</a>
    <a href="https://twitter.com/intent/tweet?url=URL_PAGE&text=TITRE_PAGE" target="_blank" rel="noopener" style="background:#000;color:white;text-decoration:none;padding:.5rem 1.1rem;border-radius:50px;font-size:.82rem;font-weight:600;display:inline-flex;align-items:center;gap:.4rem">𝕏 Twitter</a>
    <a href="https://www.linkedin.com/sharing/share-offsite/?url=URL_PAGE" target="_blank" rel="noopener" style="background:#0A66C2;color:white;text-decoration:none;padding:.5rem 1.1rem;border-radius:50px;font-size:.82rem;font-weight:600;display:inline-flex;align-items:center;gap:.4rem">💼 LinkedIn</a>
    <a href="whatsapp://send?text=TITRE_PAGE - URL_PAGE" target="_blank" rel="noopener" style="background:#25D366;color:white;text-decoration:none;padding:.5rem 1.1rem;border-radius:50px;font-size:.82rem;font-weight:600;display:inline-flex;align-items:center;gap:.4rem">💬 WhatsApp</a>
    <a href="https://pinterest.com/pin/create/button/?url=URL_PAGE&description=TITRE_PAGE" target="_blank" rel="noopener" style="background:#E60023;color:white;text-decoration:none;padding:.5rem 1.1rem;border-radius:50px;font-size:.82rem;font-weight:600;display:inline-flex;align-items:center;gap:.4rem">📌 Pinterest</a>
  </div>
</div>
<script>
(function(){
  var url = encodeURIComponent(window.location.href);
  var titre = encodeURIComponent(document.title);
  document.querySelectorAll('a[href*="URL_PAGE"]').forEach(function(a){
    a.href = a.href.replace(/URL_PAGE/g, url).replace(/TITRE_PAGE/g, titre);
  });
})();
</script>
'''

for fichier in os.listdir(dossier):
    if not fichier.endswith('.html'):
        continue

    chemin = os.path.join(dossier, fichier)

    try:
        with open(chemin, 'r', encoding='utf-8') as f:
            contenu = f.read()

        # Vérifier si déjà présent
        if 'Partager cet article' in contenu:
            continue

        # Insérer avant </footer>
        if '<footer' in contenu:
            contenu = contenu.replace('<footer', boutons_html + '\n<footer', 1)
            with open(chemin, 'w', encoding='utf-8') as f:
                f.write(contenu)
            fichiers_modifies += 1

    except Exception as e:
        fichiers_erreur += 1
        print(f"Erreur sur {fichier}: {e}")

print(f"✅ {fichiers_modifies} fichiers modifiés")
print(f"❌ {fichiers_erreur} erreurs")
