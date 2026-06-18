import os

count = 0
script = '<script>function toggleMenu(){var m=document.getElementById("mobileMenu");m.classList.toggle("open");document.body.style.overflow=m.classList.contains("open")?"hidden":"";}</script>'

for f in os.listdir('.'):
    if not f.endswith('.html') or f == 'index.html':
        continue
    content = open(f, 'r', encoding='utf-8', errors='ignore').read()
    if 'function toggleMenu' not in content:
        content = content.replace('</body>', script + '</body>', 1)
        open(f, 'w', encoding='utf-8').write(content)
        count += 1

print(str(count) + ' fichiers corriges')