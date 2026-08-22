/* ============ MODE RÉSONANCE — Fréquences Fantômes ============ */
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
