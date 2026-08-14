# add_epilogue.py — épilogue : faux article de journal du lendemain
import os, sys

BASE = "docs"

def lire(f):
    with open(f, encoding="utf-8") as fh:
        return fh.read()

def ecrire(f, c):
    with open(f, "w", encoding="utf-8") as fh:
        fh.write(c)

MODALE_HTML = '''
  <!-- ÉPILOGUE : ARTICLE DU LENDEMAIN -->
  <div class="modale" id="modale-article" hidden>
    <div class="journal">
      <button class="btn petit fermer" id="btn-fermer-article">✖ Fermer</button>
      <p class="j-nom">LE COURRIER DE MIRABEAU</p>
      <p class="j-date">Édition locale — samedi 16 août 2026 — 6 h 12</p>
      <h2 class="j-titre">Confession à 3 h 33 sur Fréquence Zéro</h2>
      <div class="j-corps">
        <p>Après vingt ans de silence, l'incendie de la cabine radio de 2006 a enfin une voix. Dans la nuit de vendredi à samedi, l'animateur de l'émission nocturne <i>Fréquence Zéro</i> a diffusé en direct la confession de M. D., ancien technicien de la station.</p>
        <p>L'homme a reconnu avoir fermé la porte de la cabine de diffusion lors de l'incendie du 15 août 2006, sans savoir qu'un technicien de nuit, R. Callot, s'y trouvait encore. Le rapport de l'époque concluait à un accident et à des locaux vides.</p>
        <p>« La bande tourne encore », nous a confié l'animateur, joint par téléphone. La police a confirmé la saisie d'un enregistrement « d'intérêt majeur ».</p>
        <p>M. D. s'est constitué prisonnier à l'aube. Il a demandé à être jugé « en direct, si c'est possible ».</p>
        <p>La ligne téléphonique intérieure dite « ligne 0 », installée au sous-sol avant l'incendie, a été débranchée hier matin. Selon la station, « plus aucun appel n'est attendu ».</p>
      </div>
      <p class="j-sign">— La rédaction locale</p>
    </div>
  </div>
'''

EPILOGUE_CSS = '''
/* ============ ÉPILOGUE — ARTICLE DE JOURNAL ============ */
.modale { position: fixed; inset: 0; z-index: 20; display: flex; align-items: center; justify-content: center; padding: 16px; background: rgba(0,0,0,.78); }
.modale[hidden] { display: none; }
.journal {
  max-width: 640px; width: 100%; max-height: 88%; overflow-y: auto;
  background: #e8e2d0; color: #1c1a15;
  font-family: Georgia, "Times New Roman", serif;
  border-radius: 4px; padding: 26px 30px;
  box-shadow: 0 10px 60px rgba(0,0,0,.8);
  text-align: left; position: relative;
  transform: rotate(-.6deg);
}
.journal .fermer { position: absolute; top: 10px; right: 10px; border-color: #1c1a15; color: #1c1a15; }
.journal .fermer:hover:not(:disabled) { background: #1c1a15; color: #e8e2d0; }
.j-nom { text-align: center; letter-spacing: .3em; font-weight: bold; border-bottom: 3px double #1c1a15; padding-bottom: 8px; }
.j-date { text-align: center; font-size: .8rem; color: #6b6353; margin: 6px 0 14px; }
.j-titre { text-align: center; font-size: 1.5rem; letter-spacing: .04em; margin: 10px 0 14px; text-transform: uppercase; }
.j-corps p { margin: 0 0 10px; line-height: 1.65; text-align: justify; }
.j-corps p:first-child::first-letter { font-size: 2.6em; float: left; line-height: .9; padding-right: 6px; font-weight: bold; }
.j-sign { text-align: right; font-style: italic; }
'''

EPILOGUE_JS = '''
/* ---------- ÉPILOGUE : ARTICLE ---------- */
function ouvrirArticle() { const m = $("#modale-article"); if (m) { m.hidden = false; gresillement(1.2, 0.03); } }
function fermerArticle() { const m = $("#modale-article"); if (m) m.hidden = true; }
document.querySelectorAll(".btn-article, #btn-article-fin").forEach((b) => b.onclick = ouvrirArticle);
const btnFermerArticle = $("#btn-fermer-article");
if (btnFermerArticle) btnFermerArticle.onclick = fermerArticle;
const modaleArticle = $("#modale-article");
if (modaleArticle) modaleArticle.addEventListener("click", (e) => { if (e.target === modaleArticle) fermerArticle(); });
'''

LIGNE_ARTICLE_FIN = '''  const artBtn = $("#btn-article-fin");
  if (artBtn) artBtn.style.display = (indexNuit + 1 === NUITS.length) ? "inline-block" : "none";
'''

BTN_GENERIQUE = "      <button class=\"btn petit btn-article\">📰 Lire l'article du lendemain</button>\n"
BTN_FIN = "        <button class=\"btn btn-article\" id=\"btn-article-fin\" style=\"display:none\">📰 Lire l'article du lendemain</button>"

# --- 1. index.html : modale + bouton 📰 ---
f = os.path.join(BASE, "index.html")
html = lire(f)
if "modale-article" in html:
    print("⏭️  index.html déjà modifié")
else:
    if "</main>" not in html:
        sys.exit("❌ Balise </main> introuvable dans index.html")
    html = html.replace("</main>", "</main>" + MODALE_HTML, 1)
    if "ecran-generique" in html and "mikefri-studio.github.io</a>" in html:
        html = html.replace("mikefri-studio.github.io</a>", "mikefri-studio.github.io</a>\n" + BTN_GENERIQUE, 1)
        print("✅ bouton 📰 ajouté sur le générique")
    else:
        cible = '<button class="btn" id="btn-suite" style="display:none"></button>'
        if cible not in html:
            sys.exit("❌ Bouton btn-suite introuvable dans index.html")
        html = html.replace(cible, cible + "\n" + BTN_FIN, 1)
        print("✅ bouton 📰 ajouté sur l'écran de fin")
    ecrire(f, html)
    print("✅ index.html")

# --- 2. style.css ---
f = os.path.join(BASE, "css", "style.css")
c = lire(f)
if "ÉPILOGUE — ARTICLE" in c:
    print("⏭️  css/style.css déjà modifié")
else:
    ecrire(f, c + EPILOGUE_CSS)
    print("✅ css/style.css")

# --- 3. game.js ---
f = os.path.join(BASE, "js", "game.js")
c = lire(f)
modif = False
if "artBtn" not in c:
    cible = 'montrer("#ecran-fin");'
    if cible not in c:
        sys.exit("❌ Ligne montrer(#ecran-fin) introuvable dans game.js")
    c = c.replace(cible, LIGNE_ARTICLE_FIN + cible, 1)
    modif = True
if "ÉPILOGUE : ARTICLE" not in c:
    c += EPILOGUE_JS
    modif = True
if modif:
    ecrire(f, c)
    print("✅ js/game.js")
else:
    print("⏭️  js/game.js déjà modifié")

print("\n🗞️ Épilogue intégré !")
print('git add . && git commit -m "🗞️ Épilogue : article du lendemain" && git push')