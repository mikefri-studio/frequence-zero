/* ============ DONNÉES — NUIT 2 « SONIA » ============ */
const NUIT2 = {
  titreNuit: "Nuit 2 — Sonia",
  intro: {
    titre: "1 h 12 — Studio B",
    texte: "Deuxième nuit d'antenne. Le rapport du standard n'a pas bougé de ton bureau : LIGNE 0.\nCe soir, le voyant s'allume avant même la première chanson."
  },
  auditeur: "Sonia",

  transcript: [
    { t: "00:02", qui: "Sonia", texte: "Bonsoir. Sonia. Je suis veilleuse de nuit à l'entrepôt Mirabeau, en face de votre station." },
    { t: "00:14", qui: "Sonia", texte: "Hier, à 1 h 47 pendant ma ronde, j'ai vu une silhouette dans votre studio. Quelqu'un qui me faisait signe." },
    { t: "00:30", qui: "Toi",   texte: "À 1 h 47, j'étais en direct. Le néon « ON AIR » était allumé, comme chaque nuit." },
    { t: "00:36", qui: "Sonia", texte: "Non, non… votre enseigne était ÉTEINTE. Le studio était noir. Il n'y avait que cette cigarette qui rougeoyait." },
    { t: "00:51", qui: "Sonia", texte: "Et la personne est partie dans une camionnette. Dessus, il y avait écrit « USDTIO B ». Bizarre, non ?" },
    { t: "01:03", qui: "Sonia", texte: "Enfin… si vous le dites. Bonne nuit." }
  ],

  enigmes: [
    {
      id: "croise",
      titre: "1. Témoignages croisés",
      question: "Compare son récit à ta propre nuit d'hier. Qu'est-ce qui est impossible ?",
      type: "choix",
      choix: [
        "L'entrepôt Mirabeau n'existe pas en face de la station.",
        "À 1 h 47, ton néon « ON AIR » était allumé : le studio ne pouvait pas être noir.",
        "Une veilleuse n'a pas le droit de faire des rondes à cette heure-là.",
        "Personne ne fume dans le quartier."
      ],
      bonne: 1,
      indice: "Hier, à 1 h 47, tu étais en direct. Relis ta propre réponse dans l'appel.",
      note: "Son « studio noir » contredit ton direct. Sonia ne regardait pas ton studio… ou Sonia n'était pas dehors."
    },
    {
      id: "anagramme",
      titre: "2. L'anagramme de la camionnette",
      question: "« USDTIO B » : remets les lettres dans l'ordre. Quel mot se cache là ?",
      type: "saisie",
      reponse: ["studio", "studio b", "le studio"],
      indice: "C'est l'endroit où tu es assis en ce moment même.",
      note: "USDTIO B = STUDIO B. La camionnette portait le nom de TON studio."
    },
    {
      id: "origine",
      titre: "3. Vérifie le standard",
      question: "Avant de la rappeler, tu contrôles l'origine de son appel. Le standard affiche…",
      type: "choix",
      choix: [
        "LIGNE 2 — appel mobile, quartier Mirabeau.",
        "LIGNE 5 — cabine publique de la gare.",
        "LIGNE 0 — poste intérieur."
      ],
      bonne: 2,
      indice: "Comme hier. Toujours la même ligne.",
      note: "Deux nuits, deux voix, une seule origine : le poste intérieur. Quelqu'un émet du sous-sol."
    }
  ],

  rappel: {
    question: "Sonia décroche. Une seule question pour la piéger. Laquelle ?",
    choix: [
      { texte: "« Sonia, pourquoi regardez-vous mon studio si tard ? »", bon: false,
        reaction: "« Parce qu'il y a de la lumière. Comme chaque nuit. » Tu n'avances pas." },
      { texte: "« Sonia… vous n'êtes pas en face. Vous êtes en BAS, n'est-ce pas ? »", bon: true,
        reaction: "Le grésillement change. Comme si la voix venait désormais du plancher. « …montez nous voir. »" },
      { texte: "« Sonia, la camionnette vous appartient, avouez. »", bon: false,
        reaction: "Un petit rire. « Je n'ai même pas le permis. » Clic." }
    ]
  },

  fin: {
    crt: "APPEL : LIGNE 0\nORIGINE : POSTE INTÉRIEUR — SOUS-SOL",
    texte: "Deux nuits. Deux voix. Une seule origine.\nLe poste intérieur du sous-sol. Celui de la cabine qui a brûlé il y a vingt ans."
  }
};