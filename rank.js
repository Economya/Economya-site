// Système de rangs Economya Community — source unique partagée
// entre forum-astuces.html et profil.html (évite la duplication).
const RANKS=[
  {min:0,l:'🌱 Débutant',c:'#6B7280',bg:'#F3F4F6'},
  {min:3,l:'🔍 Chasseur',c:'#3B82F6',bg:'#EFF6FF'},
  {min:8,l:'⚡ Expert',c:'#8B5CF6',bg:'#F5F3FF'},
  {min:15,l:'🔥 Maître',c:'#F97316',bg:'#FFF7ED'},
  {min:30,l:'👑 Légende',c:'#B45309',bg:'#FFFBEB'},
];
function rank(n){return RANKS.filter(r=>n>=r.min).pop();}
