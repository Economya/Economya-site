// Système de rangs Economya Community — source unique partagée
// entre forum-astuces.html et profil.html (évite la duplication).
//
// Chaque palier exige à la fois un nombre d'astuces publiées ET un
// nombre de votes reçus, pour récompenser la qualité (être utile aux
// autres) et pas seulement le volume de publications.
const RANKS=[
  {minPosts:0,  minVotes:0,   l:'🌱 Débutant',     c:'#6B7280',bg:'#F3F4F6'},
  {minPosts:3,  minVotes:5,   l:'🔍 Chasseur',     c:'#3B82F6',bg:'#EFF6FF'},
  {minPosts:6,  minVotes:15,  l:'📈 Contributeur', c:'#0EA5E9',bg:'#F0F9FF'},
  {minPosts:12, minVotes:40,  l:'⚡ Expert',       c:'#8B5CF6',bg:'#F5F3FF'},
  {minPosts:20, minVotes:80,  l:'🔥 Maître',       c:'#F97316',bg:'#FFF7ED'},
  {minPosts:30, minVotes:150, l:'💎 Virtuose',     c:'#EC4899',bg:'#FDF2F8'},
  {minPosts:50, minVotes:300, l:'👑 Légende',      c:'#B45309',bg:'#FFFBEB'},
];
// votes est optionnel pour compatibilité : si omis, seul le nombre
// d'astuces compte (comportement de secours).
function rank(posts, votes){
  const v = votes === undefined ? Infinity : votes;
  return RANKS.filter(r => posts >= r.minPosts && v >= r.minVotes).pop() || RANKS[0];
}

// Astuce « verifiee » (action 81) : au moins 3 personnes l'ont testee ET score de
// fiabilite d'au moins 80 %. Source unique partagee par la page d'une astuce et le profil.
const VERIF_MIN_TESTS = 3;
const VERIF_MIN_REL = 80;
function verifState(n, relScore){
  const verified = n >= VERIF_MIN_TESTS && relScore !== null && relScore !== undefined && relScore >= VERIF_MIN_REL;
  return { verified: verified, n: n, missing: Math.max(0, VERIF_MIN_TESTS - n) };
}
function verifText(n, relScore){
  if (verifState(n, relScore).verified) return { ok:true, text:'\u2705 V\u00e9rifi\u00e9e : test\u00e9e par ' + n + ' personnes' };
  if (n >= VERIF_MIN_TESTS) return { ok:false, text:'En cours de v\u00e9rification (test\u00e9e par ' + n + ' personnes, fiabilit\u00e9 \u00e0 confirmer)' };
  return { ok:false, text:'En cours de v\u00e9rification (' + n + ' test' + (n>1?'s':'') + ' sur ' + VERIF_MIN_TESTS + ')' };
}
