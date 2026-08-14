# add_portraits.py — intègre les portraits des auditeurs dans le jeu
import os, re, sys

BASE = "docs"

def lire(f):
    with open(f, encoding="utf-8") as fh:
        return fh.read()

def ecrire(f, c):
    with open(f, "w", encoding="utf-8") as fh:
        fh.write(c)

# --- 0. Vérifie la présence des images ---
for img in ("marco.jpg", "sonia.jpg", "ancien.jpg"):
    p = os.path.join(BASE, "assets", "images", img)
    print(("✅ " if os.path.exists(p) else "⚠️  MANQUANT : ") + p)

# --- 1. index.html : cadre portrait dans l'écran d'appel ---
f = os.path.join(BASE, "index.html")
html = lire(f)
if "appel-haut" in html:
    print("⏭️  index.html déjà modifié")
else:
    motif = re.compile(
        r'<div class="entete-appel">\s*<span class="pastille"></span>.*?id="minuteur">00:00</span>\s*</div>',
        re.S)
    if not motif.search(html):
        sys.exit("❌ Bloc entete-appel introuvable dans index.html")
    html = motif.sub('''<div class="appel-haut">
        <img id="portrait" class="portrait" src="" alt="Auditeur">
        <div class="entete-appel">
          <span class="pastille"></span> APPEL ENTRANT — « <span id="nom-auditeur"></span> »
          <span class="minuteur" id="minuteur">00:00</span>
        </div>
      </div>''', html, count=1)
    ecrire(f, html)
    print("✅ index.html")

# --- 2. Les 3 nuits : champ portrait ---
NUITS = [
    ("js/nuit1.js", 'auditeur: "Marco",', "marco.jpg"),
    ("js/nuit2.js", 'auditeur: "Sonia",', "sonia.jpg"),
    ("js/nuit3.js", 'auditeur: "L\'Ancien",', "ancien.jpg"),
]
for fichier, cible, img in NUITS:
    f = os.path.join(BASE, fichier)
    c = lire(f)
    if "portrait:" in c:
        print("⏭️  " + fichier + " déjà modifié")
        continue
    if cible not in c:
        sys.exit("❌ Ligne auditeur introuvable dans " + fichier)
    ecrire(f, c.replace(cible, cible + '\n  portrait: "assets/images/' + img + '",', 1))
    print("✅ " + fichier)

# --- 3. game.js : affiche le portrait au début de chaque nuit ---
f = os.path.join(BASE, "js", "game.js")
c = lire(f)
if "nuit.portrait" in c:
    print("⏭️  js/game.js déjà modifié")
else:
    cible = '$("#nom-auditeur").textContent = nuit.auditeur;'
    if cible not in c:
        sys.exit("❌ Cible introuvable dans game.js")
    ecrire(f, c.replace(cible, cible + '\n  $("#portrait").src = nuit.portrait;', 1))
    print("✅ js/game.js")

# --- 4. style.css : pastille ronde + néon + scintillement ---
f = os.path.join(BASE, "css", "style.css")
c = lire(f)
if ".portrait" in c:
    print("⏭️  css/style.css déjà modifié")
else:
    c += """
/* ----- portrait de l'auditeur ----- */
.appel-haut { display: flex; align-items: center; gap: 14px; margin-bottom: 12px; }
.appel-haut .entete-appel { margin-bottom: 0; flex: 1; }
.portrait {
  width: 86px; height: 86px; border-radius: 50%;
  object-fit: cover;
  border: 2px solid var(--rouge);
  box-shadow: 0 0 18px rgba(255,59,48,.45);
  filter: saturate(.9) contrast(1.1);
  animation: cligner-portrait 4s infinite;
}
@keyframes cligner-portrait {
  0%, 90%, 100% { opacity: 1; }
  92% { opacity: .55; }
  95% { opacity: .9; }
}
"""
    ecrire(f, c)
    print("✅ css/style.css")

print("\n🎉 Terminé ! Teste l'aperçu, puis commit :")
print('git add . && git commit -m "🎭 Portraits des auditeurs" && git push')