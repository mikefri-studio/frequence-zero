/* ============ FRÉQUENCE ZÉRO — moteur multi-nuits ============ */
const $ = (sel) => document.querySelector(sel);
const NUITS = [NUIT1, NUIT2, NUIT3, NUIT4];
let nuit = NUITS[0];
let indexNuit = 0;
const resolu = {};
let timeouts = [];
let tickMinuteur = null;

function montrer(id) {
  document.querySelectorAll(".ecran").forEach((e) => e.classList.remove("actif"));
  $(id).classList.add("actif");
}

function progresse() { return parseInt(localStorage.getItem("fz-prog") || "0", 10); }

function normaliser(s) {
  return s.toLowerCase()
    .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]/g, "");
}

/* ---------- AUDIO ---------- */
let ctxAudio = null;
function audio() {
  if (!ctxAudio) ctxAudio = new (window.AudioContext || window.webkitAudioContext)();
  if (ctxAudio.state === "suspended") ctxAudio.resume();
  return ctxAudio;
}
function gresillement(duree, volume) {
  const ctx = audio();
  const n = Math.floor(ctx.sampleRate * duree);
  const buf = ctx.createBuffer(1, n, ctx.sampleRate);
  const d = buf.getChannelData(0);
  for (let i = 0; i < n; i++) d[i] = Math.random() * 2 - 1;
  const src = ctx.createBufferSource(); src.buffer = buf;
  const f = ctx.createBiquadFilter(); f.type = "lowpass"; f.frequency.value = 1500;
  const g = ctx.createGain(); g.gain.value = volume;
  src.connect(f); f.connect(g); g.connect(ctx.destination); src.start();
}
function bip(freq, debut, duree, volume = 0.12) {
  const ctx = audio();
  const o = ctx.createOscillator(); const g = ctx.createGain();
  o.type = "sine"; o.frequency.value = freq;
  const t0 = ctx.currentTime + debut;
  g.gain.setValueAtTime(0, t0);
  g.gain.linearRampToValueAtTime(volume, t0 + 0.015);
  g.gain.setValueAtTime(volume, t0 + duree - 0.02);
  g.gain.linearRampToValueAtTime(0, t0 + duree);
  o.connect(g); g.connect(ctx.destination);
  o.start(t0); o.stop(t0 + duree + 0.05);
}
const MORSE = {A:".-",B:"-...",C:"-.-.",D:"-..",E:".",F:"..-.",G:"--.",H:"....",I:"..",J:".---",K:"-.-",L:".-..",M:"--",N:"-.",O:"---",P:".--.",Q:"--.-",R:".-.",S:"...",T:"-",U:"..-",V:"...-",W:".--",X:"-..-",Y:"-.--",Z:"--.."};
function jouerMorse(mot) {
  const U = 0.09; let t = 0.1;
  for (const lettre of mot.toUpperCase()) {
    const code = MORSE[lettre]; if (!code) continue;
    for (const s of code) { const d = (s === ".") ? U : U * 3; bip(640, t, d); t += d + U; }
    t += U * 2;
  }
}
function codeMorse(mot) {
  return mot.toUpperCase().split("").map((l) => MORSE[l] || "").join("   ");
}
function sonnerie() { bip(480, 0, .15); bip(480, .3, .15); bip(480, .6, .15); }
function succes()   { bip(660, 0, .12); bip(880, .15, .2); }
function erreur()   { bip(160, 0, .25, .2); }

/* ---------- TITRE ---------- */
function rendreTitre() {
  const zone = $("#liste-nuits");
  zone.innerHTML = "";
  NUITS.forEach((n, i) => {
    const ok = i <= progresse();
    const b = document.createElement("button");
    b.className = "btn";
    b.disabled = !ok;
    b.textContent = (ok ? "🌙 " : "🔒 ") + n.titreNuit;
    if (ok) b.onclick = () => demarrerNuit(i);
    zone.appendChild(b);
  });
}

function demarrerNuit(i) {
  indexNuit = i; nuit = NUITS[i];
  for (const k in resolu) delete resolu[k];
  $("#intro-titre").textContent = nuit.intro.titre;
  $("#intro-texte").innerHTML = nuit.intro.texte.replace(/\n/g, "<br>");
  $("#nom-auditeur").textContent = nuit.auditeur;
  $("#portrait").src = nuit.portrait;
  $("#portrait").style.filter = nuit.portraitStyle || "";
  reglerAmbiance(i + 1);
  montrer("#ecran-intro");
}

/* ---------- APPEL ---------- */
function jouerTranscript() {
  timeouts.forEach(clearTimeout); timeouts = [];
  clearInterval(tickMinuteur);
  const zone = $("#transcript");
  zone.innerHTML = "";
  gresillement(2, 0.04);
  let sec = 0;
  $("#minuteur").textContent = "00:00";
  tickMinuteur = setInterval(() => {
    sec++;
    $("#minuteur").textContent =
      String(Math.floor(sec / 60)).padStart(2, "0") + ":" + String(sec % 60).padStart(2, "0");
  }, 1000);
  let delai = 500;
  nuit.transcript.forEach((ligne) => {
    timeouts.push(setTimeout(() => ecrireLigne(ligne), delai));
    delai += 1200 + ligne.texte.length * 45;
  });
  timeouts.push(setTimeout(() => clearInterval(tickMinuteur), delai));
}

function ecrireLigne(ligne) {
  const zone = $("#transcript");
  const p = document.createElement("p");
  p.className = "ligne" + (ligne.qui === "Toi" ? " toi" : "") + (ligne.murmure ? " murmure" : "");
  const t = document.createElement("span");
  t.className = "t"; t.textContent = "[" + ligne.t + "]";
  const txt = document.createElement("span");
  p.appendChild(t); p.appendChild(txt);
  zone.appendChild(p);
  const complet = " " + ligne.qui + " — " + ligne.texte;
  let i = 0;
  const v = setInterval(() => {
    i++;
    txt.textContent = complet.slice(0, i);
    zone.scrollTop = zone.scrollHeight;
    if (i >= complet.length) clearInterval(v);
  }, ligne.murmure ? 90 : 28);
}

/* ---------- CARNET ---------- */
function afficherMorse(bloc, mot) {
  let p = bloc.querySelector(".morse-visuel");
  if (!p) {
    p = document.createElement("p");
    p.className = "indice morse-visuel";
    bloc.appendChild(p);
  }
  p.textContent = "🔊 " + codeMorse(mot);
}

function afficherIndice(bloc, en) {
  if (bloc.querySelector(".indice:not(.morse-visuel)")) return;
  const p = document.createElement("p");
  p.className = "indice"; p.textContent = "💡 " + en.indice;
  bloc.appendChild(p);
}

function secouer(el) {
  el.classList.remove("secousse");
  void el.offsetWidth;
  el.classList.add("secousse");
}

function rendreCarnet() {
  const zone = $("#enigmes");
  zone.innerHTML = "";
  nuit.enigmes.forEach((en) => {
    const bloc = document.createElement("div");
    bloc.className = "enigme";
    const h = document.createElement("h3");
    h.textContent = en.titre + (resolu[en.id] ? "  ✅" : "");
    bloc.appendChild(h);
    const q = document.createElement("p");
    q.className = "question"; q.textContent = en.question;
    bloc.appendChild(q);

    if (resolu[en.id]) {
      const n = document.createElement("p");
      n.className = "note"; n.textContent = "📌 " + en.note;
      bloc.appendChild(n);
      if (en.oeufMorse) {
        const o = document.createElement("button");
        o.className = "lien"; o.textContent = en.oeufMorse.texte;
        o.onclick = () => { gresillement(2, 0.03); jouerMorse(en.oeufMorse.mot); afficherMorse(bloc, en.oeufMorse.mot); try { localStorage.setItem("fz-oeuf", en.oeufMorse.mot.toLowerCase()); } catch (e) {} };
        bloc.appendChild(o);
      }

    } else {
      if (en.boutonMorse) {
        const m = document.createElement("button");
        m.className = "btn petit"; m.textContent = "🎧 Écouter le fond sonore";
        m.onclick = () => { gresillement(1.4, 0.03); jouerMorse("ICI"); afficherMorse(bloc, "ICI"); };
        bloc.appendChild(m);
      }
      if (en.boutonAudio) {
        const m = document.createElement("button");
        m.className = "btn petit"; m.textContent = en.boutonAudio.texte;
        m.onclick = () => { gresillement(1.8, 0.04); jouerMorse(en.boutonAudio.mot); afficherMorse(bloc, en.boutonAudio.mot); };
        bloc.appendChild(m);
      }
      if (en.type === "choix") {
        en.choix.forEach((c, i) => {
          const b = document.createElement("button");
          b.className = "choix"; b.textContent = c;
          b.onclick = () => {
            if (i === en.bonne) { resolu[en.id] = true; succes(); rendreCarnet(); }
            else { erreur(); secouer(b); afficherIndice(bloc, en); }
          };
          bloc.appendChild(b);
        });
      } else {
        const champ = document.createElement("input");
        champ.type = "text"; champ.placeholder = "Ta réponse…";
        const ok = document.createElement("button");
        ok.className = "btn petit"; ok.textContent = "Valider";
        ok.onclick = () => {
          const val = normaliser(champ.value);
          if (en.reponse.map(normaliser).includes(val)) { resolu[en.id] = true; succes(); rendreCarnet(); }
          else { erreur(); secouer(champ); afficherIndice(bloc, en); }
        };
        champ.addEventListener("keydown", (e) => { if (e.key === "Enter") ok.click(); });
        bloc.appendChild(champ); bloc.appendChild(ok);
      }
      const li = document.createElement("button");
      li.className = "lien"; li.textContent = "💡 Demander un indice";
      li.onclick = () => afficherIndice(bloc, en);
      bloc.appendChild(li);
    }
    zone.appendChild(bloc);
  });
  $("#btn-rappeler").disabled = !nuit.enigmes.every((e) => resolu[e.id]);
}

/* ---------- RAPPEL ---------- */
function rendreRappel() {
  const zone = $("#choix-rappel");
  zone.innerHTML = "<p class='question'>" + nuit.rappel.question + "</p>";
  nuit.rappel.choix.forEach((c) => {
    const b = document.createElement("button");
    b.className = "choix"; b.textContent = c.texte;
    b.onclick = () => {
      zone.querySelectorAll(".reaction, #btn-fin").forEach((r) => r.remove());
      const r = document.createElement("p");
      r.className = "reaction" + (c.bon ? " ok" : "");
      r.textContent = c.reaction;
      zone.appendChild(r);
      if (c.bon) {
        succes();
        zone.querySelectorAll(".choix").forEach((x) => x.disabled = true);
        const s = document.createElement("button");
        s.className = "btn"; s.id = "btn-fin";
        s.textContent = "📼 Consulter le rapport du standard";
        s.onclick = allerFin;
        zone.appendChild(s);
      } else { erreur(); }
    };
    zone.appendChild(b);
  });
}

/* ---------- FIN ---------- */
function allerFin() {
  $("#crt-fin").innerHTML = nuit.fin.crt.replace(/\n/g, "<br>");
  $("#fin-texte").innerHTML = nuit.fin.texte.replace(/\n/g, "<br>");
  $("#fin-nuit-titre").textContent = "FIN DE LA NUIT " + (indexNuit + 1);
  localStorage.setItem("fz-prog", String(Math.max(progresse(), indexNuit + 1)));
  const suite = $("#btn-suite");
  if (indexNuit + 1 < NUITS.length) {
    suite.style.display = "inline-block";
    suite.textContent = "🌙 " + NUITS[indexNuit + 1].titreNuit;
  } else { suite.style.display = "none"; }
    const artBtn = $("#btn-article-fin");
  if (artBtn) artBtn.style.display = (indexNuit + 1 === NUITS.length) ? "inline-block" : "none";
montrer("#ecran-fin");
  gresillement(3, 0.05);
  bip(120, 0.5, 0.6, 0.15);
}

/* ---------- BOUTONS ---------- */
$("#btn-appel").onclick = () => { montrer("#ecran-appel"); sonnerie(); jouerTranscript(); };
$("#btn-reecouter").onclick = () => jouerTranscript();
$("#btn-carnet").onclick = () => { montrer("#ecran-carnet"); rendreCarnet(); };
$("#btn-retour-appel").onclick = () => montrer("#ecran-appel");
$("#btn-rappeler").onclick = () => { montrer("#ecran-rappel"); sonnerie(); rendreRappel(); };
$("#btn-suite").onclick = () => demarrerNuit(indexNuit + 1);
$("#btn-rejouer").onclick = () => demarrerNuit(indexNuit);
$("#btn-titre").onclick = () => { rendreTitre(); montrer("#ecran-titre"); };
const btnRes = $("#btn-resonance");
if (btnRes) btnRes.onclick = () => lancerResonance();

rendreTitre();
/* ---------- ÉPILOGUE : ARTICLE ---------- */
function ouvrirArticle() { const m = $("#modale-article"); if (m) { m.hidden = false; gresillement(1.2, 0.03); } }
function fermerArticle() { const m = $("#modale-article"); if (m) m.hidden = true; }
document.querySelectorAll(".btn-article, #btn-article-fin").forEach((b) => b.onclick = ouvrirArticle);
const btnFermerArticle = $("#btn-fermer-article");
if (btnFermerArticle) btnFermerArticle.onclick = fermerArticle;
const modaleArticle = $("#modale-article");
if (modaleArticle) modaleArticle.addEventListener("click", (e) => { if (e.target === modaleArticle) fermerArticle(); });

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
