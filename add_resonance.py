# add_resonance.py — ajoute le mini-jeu "Mode Résonance" (Fréquences fantômes)
import os, sys

BASE = "docs"

def lire(f):
    with open(f, encoding="utf-8") as fh:
        return fh.read()

def ecrire(f, c):
    with open(f, "w", encoding="utf-8") as fh:
        fh.write(c)

# ==========================================
# 1. CONTENU À INJECTER
# ==========================================

RESONANCE_JS = r'''/* ============ MODE RÉSONANCE — Fréquences Fantômes ============ */
let ctxResonance = null;
let oscResonance = null;
let gainResonance = null;
let animFrameResonance = null;
let freqCible = 0;
let freqActuelle = 440;
let messageActuel = "";
let charsReveles = 0;
let isDraggingRes = false;
let startXRes = 0;
let startFreqRes = 440;

const messagesSecrets = [
  "Sonia sait", "L'Ancien ment", "2006 brûle", 
  "Ouvre la porte", "Marco revient", "La ligne 0 appelle", "Écoute le spectre"
];

function initAudioResonance() {
  if (!ctxResonance) {
    ctxResonance = new (window.AudioContext || window.webkitAudioContext)();
  }
  if (ctxResonance.state === "suspended") ctxResonance.resume();
}

function jouerBruitBlanc(duree = 0.1, volume = 0.05) {
  initAudioResonance();
  const buf = ctxResonance.createBuffer(1, ctxResonance.sampleRate * duree, ctxResonance.sampleRate);
  const d = buf.getChannelData(0);
  for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
  const src = ctxResonance.createBufferSource(); src.buffer = buf;
  const f = ctxResonance.createBiquadFilter(); f.type = "bandpass"; f.frequency.value = freqActuelle; f.Q.value = 5;
  const g = ctxResonance.createGain(); g.gain.value = volume;
  src.connect(f); f.connect(g); g.connect(ctxResonance.destination); src.start();
}

function jouerTon(freq, duree = 0.15, vol = 0.1) {
  initAudioResonance();
  const o = ctxResonance.createOscillator(); const g = ctxResonance.createGain();
  o.type = "sine"; o.frequency.value = freq;
  const t0 = ctxResonance.currentTime;
  g.gain.setValueAtTime(0, t0);
  g.gain.linearRampToValueAtTime(vol, t0 + 0.01);
  g.gain.linearRampToValueAtTime(0, t0 + duree);
  o.connect(g); g.connect(ctxResonance.destination);
  o.start(t0); o.stop(t0 + duree + 0.05);
}

function calculerForceSignal() {
  const dist = Math.abs(freqActuelle - freqCible);
  const maxDist = (1080 - 88) / 3;
  return Math.max(0, Math.floor((1 - dist / maxDist) * 100));
}

function mettreAJourSignal() {
  const force = calculerForceSignal();
  const bar = $("#res-signal-bar");
  const txt = $("#res-signal-percent");
  if (bar) bar.style.width = force + "%";
  if (txt) txt.textContent = force;

  if (force > 70 && messageActuel) {
    if (charsReveles < messageActuel.length) {
      setTimeout(() => {
        charsReveles++;
        mettreAJourTexteDecode();
        jouerTon(880, 0.05, 0.05);
      }, 150);
    }
  } else if (force < 50) {
    if (charsReveles > 0) {
      charsReveles--;
      mettreAJourTexteDecode();
    }
  }
}

function mettreAJourTexteDecode() {
  const zone = $("#res-decoded-text");
  if (!zone) return;
  if (!messageActuel) {
    zone.innerHTML = "<em>Signal trop faible...</em>";
    return;
  }
  let html = "";
  for (let i = 0; i < messageActuel.length; i++) {
    const char = messageActuel[i] === " " ? "&nbsp;" : messageActuel[i];
    if (i < charsReveles) {
      html += `<span class="decoded-char visible">${char}</span>`;
    } else {
      html += `<span class="decoded-char">?</span>`;
    }
  }
  zone.innerHTML = html;
}

function dessinerSpectrogramme() {
  const canvas = $("#res-canvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const w = canvas.width; const h = canvas.height;
  const imgData = ctx.createImageData(w, h);
  const data = imgData.data;
  const force = calculerForceSignal() / 100;

  for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) {
      const i = (y * w + x) * 4;
      let noise = Math.random() * (isDraggingRes ? 100 : 40);
      const dist = Math.abs(freqActuelle - freqCible);
      const maxDist = (1080 - 88) / 4;
      const sig = Math.max(0, 1 - dist / maxDist);
      
      if (sig > 0.1) {
        const wave = Math.sin(x * 0.1 + y * 0.05 + Date.now() * 0.005) * sig * 150;
        data[i] = Math.min(255, noise + 50 + wave);
        data[i+1] = Math.min(255, noise + 100 + wave);
        data[i+2] = Math.min(255, noise + 50);
        data[i+3] = 255;
      } else {
        data[i] = noise; data[i+1] = noise * 0.5; data[i+2] = noise * 0.8; data[i+3] = 255;
      }
    }
  }
  ctx.putImageData(imgData, 0, 0);
  if (isDraggingRes) animFrameResonance = requestAnimationFrame(dessinerSpectrogramme);
}

function lancerResonance() {
  montrer("#ecran-resonance");
  initAudioResonance();
  freqCible = 88 + Math.random() * (1080 - 88);
  messageActuel = messagesSecrets[Math.floor(Math.random() * messagesSecrets.length)];
  charsReveles = 0;
  freqActuelle = 440;
  mettreAJourPositionTuner();
  mettreAJourTexteDecode();
  $("#res-target-freq").textContent = "???";
  $("#res-status").textContent = "Ajustez le tuner pour capturer la fréquence résiduelle...";
  jouerBruitBlanc(0.5, 0.05);
}

function mettreAJourPositionTuner() {
  const pct = ((freqActuelle - 88) / (1080 - 88)) * 100;
  const knob = $("#res-tuner-knob");
  if (knob) knob.style.left = `calc(${pct}% - 20px)`;
}

// --- Événements du Tuner ---
const knob = $("#res-tuner-knob");
if (knob) {
  knob.addEventListener("mousedown", (e) => {
    isDraggingRes = true; startXRes = e.clientX; startFreqRes = freqActuelle;
    initAudioResonance();
  });
  document.addEventListener("mousemove", (e) => {
    if (!isDraggingRes) return;
    const delta = e.clientX - startXRes;
    const scale = (1080 - 88) / (window.innerWidth * 0.9);
    freqActuelle = Math.max(88, Math.min(1080, startFreqRes + delta * scale));
    mettreAJourPositionTuner();
    jouerBruitBlanc(0.05, 0.03);
    mettreAJourSignal();
    cancelAnimationFrame(animFrameResonance);
    dessinerSpectrogramme();
  });
  document.addEventListener("mouseup", () => { isDraggingRes = false; });
  
  // Touch support
  knob.addEventListener("touchstart", (e) => {
    isDraggingRes = true; startXRes = e.touches[0].clientX; startFreqRes = freqActuelle;
    initAudioResonance();
  });
  document.addEventListener("touchmove", (e) => {
    if (!isDraggingRes) return;
    const delta = e.touches[0].clientX - startXRes;
    const scale = (1080 - 88) / (window.innerWidth * 0.9);
    freqActuelle = Math.max(88, Math.min(1080, startFreqRes + delta * scale));
    mettreAJourPositionTuner();
    jouerBruitBlanc(0.05, 0.03);
    mettreAJourSignal();
    cancelAnimationFrame(animFrameResonance);
    dessinerSpectrogramme();
  });
  document.addEventListener("touchend", () => { isDraggingRes = false; });
}

// --- Boutons ---
const btnScan = $("#res-btn-scan");
if (btnScan) btnScan.onclick = () => {
  $("#res-status").textContent = "📡 Recherche de fréquences résiduelles...";
  $("#res-status").classList.add("scanning");
  let scans = 0;
  const int = setInterval(() => {
    freqActuelle = 88 + Math.random() * (1080 - 88);
    mettreAJourPositionTuner();
    jouerBruitBlanc(0.08, 0.04);
    dessinerSpectrogramme();
    scans++;
    if (scans > 15) {
      clearInterval(int);
      $("#res-status").classList.remove("scanning");
      freqCible = 88 + Math.random() * (1080 - 88);
      messageActuel = messagesSecrets[Math.floor(Math.random() * messagesSecrets.length)];
      charsReveles = 0;
      $("#res-target-freq").textContent = Math.floor(freqCible);
      $("#res-status").textContent = `✨ Fréquence détectée ! Ajustez autour de ${Math.floor(freqCible)} Hz`;
      jouerTon(660, 0.1, 0.1); jouerTon(880, 0.2, 0.1);
    }
  }, 150);
};

const btnReset = $("#res-btn-reset");
if (btnReset) btnReset.onclick = () => {
  freqActuelle = 440; freqCible = 0; messageActuel = ""; charsReveles = 0;
  $("#res-target-freq").textContent = "???";
  $("#res-status").textContent = "Ajustez le tuner pour capturer la fréquence résiduelle...";
  mettreAJourPositionTuner(); mettreAJourTexteDecode();
  jouerTon(440, 0.1, 0.1);
};

const btnBack = $("#res-btn-back");
if (btnBack) btnBack.onclick = () => {
  if (ctxResonance) ctxResonance.close();
  ctxResonance = null;
  cancelAnimationFrame(animFrameResonance);
  montrer("#ecran-titre");
};
'''

RESONANCE_CSS = '''
/* ----- MODE RÉSONANCE ----- */
#ecran-resonance {
  display: none; flex-direction: column; align-items: center; justify-content: center;
  min-height: 100vh; padding: 20px; text-align: center;
}
#ecran-resonance.actif { display: flex; }

#res-canvas {
  width: 90%; max-width: 700px; height: 180px;
  background: #0a0e14; border: 2px solid #2a3440; border-radius: 8px;
  margin-bottom: 20px; box-shadow: 0 0 20px rgba(137, 119, 89, 0.1);
}

#res-tuner-container {
  width: 90%; max-width: 700px; position: relative; margin: 20px 0;
}
#res-frequency-scale {
  width: 100%; height: 50px;
  background: linear-gradient(90deg, #0f1520 0%, #1a2230 50%, #0f1520 100%);
  border: 2px solid #3a4450; border-radius: 4px; position: relative;
}
#res-tuner-knob {
  position: absolute; top: -10px; width: 40px; height: 70px;
  background: linear-gradient(180deg, #897759 0%, #5a4d39 100%);
  border: 3px solid #c9b99a; border-radius: 8px; cursor: ew-resize;
  box-shadow: 0 4px 12px rgba(0,0,0,0.6); z-index: 5;
}
#res-tuner-knob:active { box-shadow: 0 0 20px rgba(201, 185, 154, 0.4); }
#res-tuner-knob::after {
  content: ""; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
  width: 4px; height: 20px; background: #1a2230; border-radius: 2px;
}

#res-signal-meter {
  width: 90%; max-width: 400px; height: 30px;
  background: #0a0e14; border: 2px solid #2a3440; border-radius: 15px;
  margin: 20px 0; position: relative; overflow: hidden;
}
#res-signal-bar {
  height: 100%; background: linear-gradient(90deg, #1a4a1a 0%, #2a8a2a 50%, #3aca3a 100%);
  width: 0%; transition: width 0.2s; box-shadow: 0 0 10px rgba(58, 202, 58, 0.3);
}
#res-signal-text {
  position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
  font-size: 0.8rem; font-weight: bold; text-shadow: 0 0 5px #000; z-index: 2;
}

#res-decoder {
  width: 90%; max-width: 600px; min-height: 80px;
  background: #0a0e14; border: 2px solid #3a4450; border-radius: 8px;
  padding: 20px; margin: 20px 0; font-size: 1.3rem; text-align: center;
  letter-spacing: 4px; color: #3aca3a;
}
.decoded-char { display: inline-block; opacity: 0.3; transition: opacity 0.3s; }
.decoded-char.visible { opacity: 1; animation: flicker 0.5s ease-in-out; }
@keyframes flicker { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }

#res-controls { display: flex; gap: 15px; flex-wrap: wrap; justify-content: center; margin-top: 10px; }
#res-status { margin-top: 20px; font-size: 0.85rem; color: #4a5460; min-height: 1.2em; }
.scanning { animation: scan 1s ease-in-out infinite; }
@keyframes scan { 0%, 100% { opacity: 0.3; } 50% { opacity: 1; } }
#res-target-indicator { position: absolute; top: 20px; right: 20px; font-size: 0.8rem; color: #897759; }
'''

RESONANCE_HTML = '''
  <!-- ÉCRAN MODE RÉSONANCE -->
  <div id="ecran-resonance" class="ecran">
    <div id="res-target-indicator">Fréquence cible: <span id="res-target-freq">???</span> Hz</div>
    <canvas id="res-canvas" width="700" height="180"></canvas>
    
    <div id="res-tuner-container">
      <div id="res-frequency-scale"></div>
      <div id="res-tuner-knob"></div>
    </div>

    <div id="res-signal-meter">
      <div id="res-signal-bar"></div>
      <div id="res-signal-text">SIGNAL: <span id="res-signal-percent">0</span>%</div>
    </div>

    <div id="res-decoder">
      <span id="res-decoded-text"><em>En attente de signal...</em></span>
    </div>

    <div id="res-controls">
      <button id="res-btn-scan" class="btn">📡 Scanner</button>
      <button id="res-btn-reset" class="btn">Réinitialiser</button>
      <button id="res-btn-back" class="btn">← Retour au titre</button>
    </div>
    <div id="res-status">Ajustez le tuner pour capturer la fréquence résiduelle...</div>
  </div>
'''

# ==========================================
# 2. INJECTION DANS LES FICHIERS
# ==========================================

# --- 1. Créer js/resonance.js ---
f = os.path.join(BASE, "js", "resonance.js")
if os.path.exists(f):
    print("⏭️  js/resonance.js existe déjà")
else:
    ecrire(f, RESONANCE_JS)
    print("✅ js/resonance.js créé")

# --- 2. Modifier index.html (ajouter l'écran et le script) ---
f = os.path.join(BASE, "index.html")
html = lire(f)
modif_html = False

if "ecran-resonance" not in html:
    # Insérer l'écran juste avant la fermeture de </main> ou </body>
    cible = "</body>"
    if cible in html:
        html = html.replace(cible, RESONANCE_HTML + "\n" + cible)
        modif_html = True

if 'src="js/resonance.js"' not in html:
    cible = '<script src="js/game.js"></script>'
    if cible in html:
        html = html.replace(cible, '<script src="js/resonance.js"></script>\n  ' + cible)
        modif_html = True

if modif_html:
    ecrire(f, html)
    print("✅ index.html modifié (écran + script)")
else:
    print("⏭️  index.html déjà à jour")

# --- 3. Modifier css/style.css ---
f = os.path.join(BASE, "css", "style.css")
c = lire(f)
if "MODE RÉSONANCE" not in c:
    ecrire(f, c + "\n" + RESONANCE_CSS)
    print("✅ css/style.css mis à jour")
else:
    print("⏭️  css/style.css déjà à jour")

# --- 4. Modifier js/game.js (ajouter le bouton de lancement) ---
f = os.path.join(BASE, "js", "game.js")
c = lire(f)
modif_game = False

if "lancerResonance" not in c:
    # Ajouter la fonction de lancement si elle n'est pas déjà dans resonance.js, 
    # mais on va ajouter un bouton dans l'écran titre pour y accéder.
    cible = '$("#btn-titre").onclick = () => { rendreTitre(); montrer("#ecran-titre"); };'
    if cible in c:
        # On ajoute un bouton dans le HTML via JS, ou on modifie game.js pour écouter un nouveau bouton
        # Le plus simple : on ajoute l'écouteur directement ici
        c = c.replace(cible, cible + '\nconst btnRes = $("#btn-resonance");\nif (btnRes) btnRes.onclick = () => lancerResonance();')
        modif_game = True

if modif_game:
    ecrire(f, c)
    print("✅ js/game.js mis à jour (lien vers résonance)")
else:
    print("⏭️  js/game.js déjà à jour")

# --- 5. Ajouter un bouton d'accès dans l'écran titre (via index.html ou JS) ---
# On va injecter un petit bouton discret dans index.html s'il n'existe pas
f = os.path.join(BASE, "index.html")
html = lire(f)
if 'id="btn-resonance"' not in html:
    # Chercher un bon endroit, par exemple après le bouton "Commencer" ou dans le footer
    cible = '<button id="btn-casque"'
    if cible in html:
        html = html.replace(cible, '<button id="btn-resonance" class="btn" style="margin-right: 10px; font-size: 0.8rem;">📡 Résonance</button>\n  ' + cible)
        ecrire(f, html)
        print("✅ index.html : bouton 'Résonance' ajouté à l'écran titre")
    else:
        print("⚠️  Impossible de trouver l'emplacement pour le bouton Résonance dans index.html")
else:
    print("⏭️  Bouton Résonance déjà présent dans index.html")

print("\n📡 Mode Résonance intégré avec succès !")
print('git add . && git commit -m "📡 Ajout du Mode Résonance (fréquences fantômes)" && git push')