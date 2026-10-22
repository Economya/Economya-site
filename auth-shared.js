// auth-shared.js
//
// Logique d'authentification Supabase partagee entre connexion.html (page
// dediee) et forum-astuces.html (popup) : memes regles de validation, memes
// appels API, meme format de session stockee. Avant ce fichier, les deux
// pages avaient chacune leur propre copie de ce code, avec le risque qu'un
// futur correctif (ex. regle d'age, message d'erreur) soit fait dans une
// seule des deux copies sans que personne ne s'en rende compte.
//
// Chaque page garde sa propre interface (popup qui reste sur place vs page
// de connexion separee) et son propre code d'affichage/navigation : ce
// fichier ne contient que les regles et les appels reseau, identiques
// partout.

const AUTH_SUPABASE_URL = 'https://awelbxqiltokhsoddako.supabase.co';
const AUTH_SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF3ZWxieHFpbHRva2hzb2RkYWtvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODkzNTM1MjIsImV4cCI6MjEwNDkyOTUyMn0.pao4Gxw9S7bdfTFExd3W1idWEV76VvykeiZSSf3mQxw';

// Affiche un message dans un bandeau d'erreur/succes (meme logique que les
// showAuthError/showForgotMsg/showResetError auparavant dupliques).
function authShowMessage(elId, msg, ok){
  const el = document.getElementById(elId);
  if(!el) return;
  el.textContent = msg;
  el.style.background = ok ? '#F0FDF4' : '#FEF2F2';
  el.style.color = ok ? '#16A34A' : '#DC2626';
  el.style.display = 'block';
}

// Valide pseudo + date de naissance (15 ans min) + CGU pour une inscription.
// Retourne null si tout est valide, sinon le message d'erreur a afficher.
function authValidateSignup(pseudo, birthVal, cguChecked){
  if(!pseudo){ return 'Choisissez un pseudo.'; }
  if(!birthVal){ return 'Indiquez votre date de naissance.'; }
  const birth = new Date(birthVal);
  const today = new Date();
  let age = today.getFullYear() - birth.getFullYear();
  const m = today.getMonth() - birth.getMonth();
  if(m < 0 || (m === 0 && today.getDate() < birth.getDate())) age--;
  if(age < 15){ return 'Vous devez avoir au moins 15 ans pour créer un compte sur Economya.'; }
  if(!cguChecked){ return 'Vous devez accepter les CGU pour créer un compte.'; }
  return null;
}

// Appelle Supabase pour une inscription ou une connexion par mot de passe.
// authMode: 'signup' | 'login'. Retourne {ok:true, data} ou {ok:false, msg}.
async function authSubmit(authMode, email, password, pseudo, captchaToken, birthDate){
  let res;
  if(authMode === 'signup'){
    res = await fetch(AUTH_SUPABASE_URL + '/auth/v1/signup', {
      method: 'POST',
      headers: {'apikey': AUTH_SUPABASE_KEY, 'Content-Type': 'application/json'},
      body: JSON.stringify({email, password, data: {pseudo, birth_date: birthDate || null}, gotrue_meta_security: {captcha_token: captchaToken}})
    });
  } else {
    res = await fetch(AUTH_SUPABASE_URL + '/auth/v1/token?grant_type=password', {
      method: 'POST',
      headers: {'apikey': AUTH_SUPABASE_KEY, 'Content-Type': 'application/json'},
      body: JSON.stringify({email, password, gotrue_meta_security: {captcha_token: captchaToken}})
    });
  }
  const data = await res.json();
  if(!res.ok){
    const msg = data.msg || data.error_description || data.error || 'Une erreur est survenue.';
    return {ok:false, msg: msg === 'Invalid login credentials' ? 'Email ou mot de passe incorrect.' : msg};
  }
  return {ok:true, data};
}

// Construit l'objet session a partir de la reponse Supabase et le sauvegarde
// dans localStorage (eco_session + eco_user, meme format qu'avant). Retourne
// la session construite pour que la page appelante mette a jour son propre
// etat (variables globales, re-rendu, etc.).
function authSaveSession(data){
  const session = {
    access_token: data.access_token,
    refresh_token: data.refresh_token,
    expires_at: Date.now() + (data.expires_in || 3600) * 1000,
    user: data.user
  };
  localStorage.setItem('eco_session', JSON.stringify(session));
  const pseudo = (session.user.user_metadata && session.user.user_metadata.pseudo) || session.user.email;
  localStorage.setItem('eco_user', pseudo);
  return session;
}

// Envoie l'email "mot de passe oublie". Retourne {ok:true} ou {ok:false, msg}.
async function authRecover(email, redirectTo){
  try {
    const res = await fetch(AUTH_SUPABASE_URL + '/auth/v1/recover', {
      method: 'POST',
      headers: {'apikey': AUTH_SUPABASE_KEY, 'Content-Type': 'application/json'},
      body: JSON.stringify({ email, options: { redirect_to: redirectTo } })
    });
    if(!res.ok){
      const data = await res.json().catch(()=>({}));
      return {ok:false, msg: data.msg || data.error_description || 'Une erreur est survenue.'};
    }
    return {ok:true};
  } catch(e){
    return {ok:false, msg: e.message};
  }
}

// Verifie un code de recuperation de mot de passe a 6 chiffres (recu par
// email suite a authRecover) et retourne une session (access_token /
// refresh_token) si le code est valide. Utilise a la place du lien
// cliquable historique : certains clients mail (Gmail en tete, mais pas
// seulement) pre-visitent automatiquement les liens contenus dans un email
// pour les scanner avant que l'utilisateur ne clique dessus, ce qui
// "consomme" le lien a usage unique et le rend invalide des que
// l'utilisateur clique vraiment dessus (erreur otp_expired). Un code que
// l'utilisateur recopie lui-meme est immunise contre ce probleme, quelle
// que soit la messagerie utilisee.
async function authVerifyRecovery(email, token){
  try {
    const res = await fetch(AUTH_SUPABASE_URL + '/auth/v1/verify', {
      method: 'POST',
      headers: {'apikey': AUTH_SUPABASE_KEY, 'Content-Type': 'application/json'},
      body: JSON.stringify({ type: 'recovery', email, token })
    });
    const data = await res.json();
    if(!res.ok){
      const msg = data.msg || data.error_description || data.error || 'Code invalide ou expiré.';
      return {ok:false, msg};
    }
    return {ok:true, data};
  } catch(e){
    return {ok:false, msg: e.message};
  }
}

// Definit un nouveau mot de passe pour l'utilisateur identifie par
// accessToken (obtenu via authVerifyRecovery, ou via l'ancien lien
// cliquable dans le hash de l'URL). Retourne {ok:true, data} (l'utilisateur
// a jour) ou {ok:false, msg}.
async function authSetNewPassword(accessToken, password){
  try {
    const res = await fetch(AUTH_SUPABASE_URL + '/auth/v1/user', {
      method: 'PUT',
      headers: {'apikey': AUTH_SUPABASE_KEY, 'Authorization': 'Bearer ' + accessToken, 'Content-Type': 'application/json'},
      body: JSON.stringify({ password })
    });
    const data = await res.json();
    if(!res.ok){
      return {ok:false, msg: data.msg || data.error_description || 'Une erreur est survenue.'};
    }
    return {ok:true, data};
  } catch(e){
    return {ok:false, msg: e.message};
  }
}
