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
