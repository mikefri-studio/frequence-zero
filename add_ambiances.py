# add_generique.py — écran de fin définitif : générique, crédits, recommencer
import os, sys

BASE = "docs"

def lire(f):
    with open(f, encoding="utf-8") as fh:
        return fh.read()

def ecrire(f, c):
    with open(f, "w", encoding="utf-8") as fh:
        fh.write(c)

GEN_HTML = '''
  <!-- GÉNÉRIQUE -->
  <section class="ecran" id="ecran-generique">
    <div class="contenu carte generique">
      <h2 class="gen-titre">FRÉQUENCE ZÉRO</h2>
      <p class="gen-sous">Une histoire de nuits, d'ondes et de confessions.</p>
      <div class="gen-credits">
        <p><span>Écriture et conception</span><b>mikefri-studio</b></p>
        <p><span>Moteur de jeu et audio</span><b>Vanilla JS — Web Audio API</b></p>
        <p><span>Décors et fioritures</span><b>SVG et CSS maison</b></p>
        <p><span>Voix de la ligne 0</span><b>Marco, Sonia, L'Ancien… et toi</b></p>
      </div>
      <p class="gen-merci">Merci d'avoir écouté.<br>La ligne 0 est maintenant muette.</p>
      <a class="btn petit" href="https://mikefri-studio.github.io/frequence-zero/docs/index.html" target="_blank" rel="noopener">📻 mikefri-studio.github.io</a>
      <div class="rangée">
        <button class="btn" id="btn-recommencer">↺ Recommencer depuis le début</button>
        <button class="btn petit" id="btn-titre2">🏠 Titre</button>
      </div>
    </div>
  </section>
'''

GEN_CSS = '''
/* ============ GÉNÉRIQUE DE FIN ============ */
.generique { text-align: center; }
.gen-titre { color: #fff; letter-spacing: .3em; text-shadow: 0 0 10px var(--rouge), 0 0 30px var(--rouge); margin-bottom: 6px; }
.gen-sous { color: var(--gris-texte); font-style: italic; margin-bottom: 18px; }
.gen-credits p { display: flex; justify-content: space-between; gap: 14px; margin: 10px 0; padding: 8px 12px; border-bottom: 1px dashed #22303d; }
.gen-credits span { color: #55708a; }
.gen-credits b { color: var(--ambre); font-weight: normal; letter-spacing: .06em; }
.gen-merci { margin: 18px 0; color: var(--vert); text-shadow: 0 0 10px rgba(57,255,136,.4); }
'''

GEN_JS = '''
/* ---------- GÉNÉRIQUE ---------- */
const btnGen = $("#btn-generique");
if (btnGen) btnGen.onclick = () => { montrer("#ecran-generique"); gresillement(2, 0.04); succes(); };
const btnRec = $("#btn-recommencer");
if (btnRec) btnRec.onclick = () => { try { localStorage.removeItem("fz-prog"); } catch (e) {} delete document.body.dataset.nuit; rendreTitre(); montrer("#ecran-titre"); };
const btnTitre2 = $("#btn-titre2");
if (btnTitre2) btnTitre2.onclick = () => { delete document.body.dataset.nuit; rendreTitre(); montrer("#ecran-titre"); };
'''

LIGNE_ALLERFIN = '''  const genBtn = $("#btn-generique");
  if (genBtn) genBtn.style.display = (indexNuit + 1 === NUITS.length) ? "inline-block" : "none";
'''

# --- 1. index.html : bouton générique + section générique ---
f = os.path.join(BASE, "index.html")
html = lire(f)
if "ecran-generique" in html:
    print("⏭️  index.html déjà modifié")
else:
    cible_btn = '<button class="btn" id="btn-suite" style="display:none"></button>'
    if cible_btn not in html:
        sys.exit("❌ Bouton btn-suite introuvable dans index.html")
    html = html.replace(cible_btn, cible_btn + '\n        <button class="btn" id="btn-generique" style="display:none">🎬 Générique de fin</button>', 1)
    if "</main>" not in html:
        sys.exit("❌ Balise </main> introuvable dans index.html")
    html = html.replace("</main>", GEN_HTML + "</main>", 1)
    ecrire(f, html)
    print("✅ index.html")

# --- 2. style.css : habillage du générique ---
f = os.path.join(BASE, "css", "style.css")
c = lire(f)
if "GÉNÉRIQUE DE FIN" in c:
    print("⏭️  css/style.css déjà modifié")
else:
    ecrire(f, c + GEN_CSS)
    print("✅ css/style.css")

# --- 3. game.js : affichage conditionnel + handlers ---
f = os.path.join(BASE, "js", "game.js")
c = lire(f)
modif = False
if "genBtn" not in c:
    cible = 'montrer("#ecran-fin");'
    if cible not in c:
        sys.exit("❌ Ligne montrer(#ecran-fin) introuvable dans game.js")
    c = c.replace(cible, LIGNE_ALLERFIN + cible, 1)
    modif = True
if "GÉNÉRIQUE ----------" not in c:
    c += GEN_JS
    modif = True
if modif:
    ecrire(f, c)
    print("✅ js/game.js")
else:
    print("⏭️  js/game.js déjà modifié")

print("\n🎉 Générique de fin intégré !")
print('git add . && git commit -m "🎬 Générique de fin + recommencer" && git push')