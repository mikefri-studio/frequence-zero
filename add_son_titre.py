# add_son_titre.py — son d'ambiance dès l'écran titre
import os, sys

BASE = "docs"

def lire(f):
    with open(f, encoding="utf-8") as fh:
        return fh.read()

def ecrire(f, c):
    with open(f, "w", encoding="utf-8") as fh:
        fh.write(c)

BTN_TITRE_HTML = '      <button class="btn petit" id="btn-casque">🎧 Activer le son</button>\n'

TITRE_JS = '''
/* ---------- SON DÈS L'ÉCRAN TITRE ---------- */
const btnCasque = $("#btn-casque");
if (btnCasque) btnCasque.onclick = () => {
  ambianceOn = true;
  const bAmb = $("#btn-ambiance"); if (bAmb) bAmb.textContent = "🔊";
  gresillement(1.4, 0.04); bip(640, .2, .08); bip(880, .45, .1);
  reglerAmbiance(0);
  btnCasque.textContent = "🎧 Son activé — bonne écoute";
  btnCasque.disabled = true;
};
'''

TITRE_CSS = '''
/* ----- bouton casque sur le titre ----- */
#btn-casque { border-color: var(--ambre); color: var(--ambre); animation: souffle 2.5s infinite; }
@keyframes souffle { 50% { box-shadow: 0 0 14px rgba(255,179,64,.35); } }
'''

# --- 0. prérequis : le moteur d'ambiance ---
f = os.path.join(BASE, "js", "game.js")
c = lire(f)
if "AMBIANCE SONORE" not in c:
    sys.exit("❌ Moteur d'ambiance absent. Lance d'abord : python3 add_ambiance_sonore.py")

modif = False

# --- 1. game.js : handler du bouton casque ---
if "SON DÈS L'ÉCRAN TITRE" not in c:
    c += TITRE_JS
    modif = True
if modif:
    ecrire(f, c)
    print("✅ js/game.js")
else:
    print("⏭️  js/game.js déjà modifié")

# --- 2. index.html : bouton 🎧 sur l'écran titre ---
f = os.path.join(BASE, "index.html")
html = lire(f)
if "btn-casque" in html:
    print("⏭️  index.html déjà modifié")
else:
    cible = '<div id="liste-nuits"></div>'
    if cible not in html:
        sys.exit("❌ Div #liste-nuits introuvable dans index.html")
    ecrire(f, html.replace(cible, BTN_TITRE_HTML + cible, 1))
    print("✅ index.html")

# --- 3. style.css : halo respirant du bouton ---
f = os.path.join(BASE, "css", "style.css")
c = lire(f)
if "bouton casque" in c:
    print("⏭️  css/style.css déjà modifié")
else:
    ecrire(f, c + TITRE_CSS)
    print("✅ css/style.css")

print("\n🎧 Son sur l'écran titre intégré !")
print('git add . && git commit -m "🎧 Bouton casque sur l\'écran titre" && git push')