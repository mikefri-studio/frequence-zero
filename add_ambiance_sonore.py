# add_ambiance_sonore.py — pluie et vent en fond, intensité par nuit
import os, sys

BASE = "docs"

def lire(f):
    with open(f, encoding="utf-8") as fh:
        return fh.read()

def ecrire(f, c):
    with open(f, "w", encoding="utf-8") as fh:
        fh.write(c)

AMBIANCE_JS = '''
/* ---------- AMBIANCE SONORE DE FOND ---------- */
let ambianceOn = true;
let ambianceNodes = null;
function ambiance() {
  if (ambianceNodes) return ambianceNodes;
  const ctx = audio();
  const buf = ctx.createBuffer(1, ctx.sampleRate * 2, ctx.sampleRate);
  const d = buf.getChannelData(0);
  for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
  const pluie = ctx.createBufferSource(); pluie.buffer = buf; pluie.loop = true;
  const lp = ctx.createBiquadFilter(); lp.type = "lowpass"; lp.frequency.value = 900;
  const gPluie = ctx.createGain(); gPluie.gain.value = 0;
  pluie.connect(lp); lp.connect(gPluie); gPluie.connect(ctx.destination);
  const vent = ctx.createBufferSource(); vent.buffer = buf; vent.loop = true; vent.playbackRate.value = .7;
  const bp = ctx.createBiquadFilter(); bp.type = "bandpass"; bp.frequency.value = 300; bp.Q.value = .8;
  const gVent = ctx.createGain(); gVent.gain.value = 0;
  const lfo = ctx.createOscillator(); lfo.frequency.value = .07;
  const lfoGain = ctx.createGain(); lfoGain.gain.value = 140;
  lfo.connect(lfoGain); lfoGain.connect(bp.frequency);
  vent.connect(bp); bp.connect(gVent); gVent.connect(ctx.destination);
  pluie.start(); vent.start(); lfo.start();
  ambianceNodes = { gPluie, gVent };
  return ambianceNodes;
}
function reglerAmbiance(num) {
  if (!ambianceOn) return;
  const a = ambiance();
  const ctx = audio(); const t = ctx.currentTime;
  const niveaux = { 0: [.025, .014], 1: [.03, .018], 2: [.022, .026], 3: [.012, .03], 4: [.007, .016] };
  const nv = niveaux[num] || [.03, .018];
  a.gPluie.gain.cancelScheduledValues(t); a.gVent.gain.cancelScheduledValues(t);
  a.gPluie.gain.setValueAtTime(a.gPluie.gain.value, t);
  a.gVent.gain.setValueAtTime(a.gVent.gain.value, t);
  a.gPluie.gain.linearRampToValueAtTime(nv[0], t + 2);
  a.gVent.gain.linearRampToValueAtTime(nv[1], t + 2);
}
const btnAmbiance = $("#btn-ambiance");
if (btnAmbiance) btnAmbiance.onclick = () => {
  ambianceOn = !ambianceOn;
  btnAmbiance.textContent = ambianceOn ? "🔊" : "🔇";
  if (ambianceOn) { reglerAmbiance(indexNuit + 1); }
  else {
    const a = ambianceNodes;
    if (a) { const ctx = audio(); const t = ctx.currentTime;
      a.gPluie.gain.linearRampToValueAtTime(0, t + .5);
      a.gVent.gain.linearRampToValueAtTime(0, t + .5); }
  }
};
'''

LIGNE_DEMARRER = "  reglerAmbiance(i + 1);\n"

BTN_HTML = '''<button id="btn-ambiance" class="btn-ambiance" title="Ambiance sonore" aria-label="Activer ou couper l'ambiance sonore">🔊</button>'''

AMBIANCE_CSS = '''
/* ----- bouton ambiance ----- */
.btn-ambiance {
  position: fixed; right: 14px; bottom: 14px; z-index: 9;
  background: rgba(8,12,16,.7); border: 1px solid #2a3440; color: var(--gris-texte);
  border-radius: 20px; padding: 6px 12px; font-family: inherit; font-size: .85rem;
  cursor: pointer; transition: .2s;
}
.btn-ambiance:hover { border-color: var(--ambre); color: var(--ambre); }
'''

# --- 1. game.js : moteur d'ambiance + appel au démarrage des nuits ---
f = os.path.join(BASE, "js", "game.js")
c = lire(f)
modif = False
if "AMBIANCE SONORE" not in c:
    c += AMBIANCE_JS
    modif = True
if "reglerAmbiance(i + 1)" not in c:
    cible = '  montrer("#ecran-intro");'
    if cible not in c:
        sys.exit("❌ Ligne montrer(#ecran-intro) introuvable dans game.js")
    c = c.replace(cible, LIGNE_DEMARRER + cible, 1)
    modif = True
if modif:
    ecrire(f, c)
    print("✅ js/game.js")
else:
    print("⏭️  js/game.js déjà modifié")

# --- 2. index.html : bouton 🔊 ---
f = os.path.join(BASE, "index.html")
html = lire(f)
if "btn-ambiance" in html:
    print("⏭️  index.html déjà modifié")
else:
    cible = '<div id="pluie"></div>'
    if cible not in html:
        sys.exit("❌ Div #pluie introuvable dans index.html")
    ecrire(f, html.replace(cible, cible + "\n" + BTN_HTML, 1))
    print("✅ index.html")

# --- 3. style.css : habillage du bouton ---
f = os.path.join(BASE, "css", "style.css")
c = lire(f)
if "bouton ambiance" in c:
    print("⏭️  css/style.css déjà modifié")
else:
    ecrire(f, c + AMBIANCE_CSS)
    print("✅ css/style.css")

print("\n🎧 Ambiance sonore intégrée !")
print('git add . && git commit -m "🎧 Ambiance sonore : pluie et vent" && git push')