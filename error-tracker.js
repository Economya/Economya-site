// Economya.fr — suivi des erreurs JS en production (tâche #75)
// Envoie un signalement minimal à Supabase quand une erreur JS non
// gérée ou une promesse rejetée non gérée se produit sur une page.
// Autonome : ne dépend d'aucune variable définie par la page qui le charge.
(function () {
  var SUPABASE_URL = 'https://awelbxqiltokhsoddako.supabase.co';
  var SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF3ZWxieHFpbHRva2hzb2RkYWtvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODkzNTM1MjIsImV4cCI6MjEwNDkyOTUyMn0.pao4Gxw9S7bdfTFExd3W1idWEV76VvykeiZSSf3mQxw';
  var MAX_REPORTS = 5; // evite qu'une boucle d'erreurs ne sature la table
  var sentCount = 0;
  var seen = {};

  function getUserPseudo() {
    try { return localStorage.getItem('eco_user') || null; } catch (e) { return null; }
  }

  function report(message, stack) {
    if (sentCount >= MAX_REPORTS) return;
    message = String(message || '').slice(0, 500);
    stack = String(stack || '').slice(0, 2000);
    var key = message + '|' + stack.slice(0, 200);
    if (seen[key]) return;
    seen[key] = true;
    sentCount++;
    try {
      fetch(SUPABASE_URL + '/rest/v1/js_errors', {
        method: 'POST',
        headers: {
          apikey: SUPABASE_KEY,
          'Content-Type': 'application/json',
          Prefer: 'return=minimal'
        },
        body: JSON.stringify({
          message: message,
          stack: stack,
          url: location.href,
          user_agent: navigator.userAgent,
          user_pseudo: getUserPseudo()
        }),
        keepalive: true
      }).catch(function () {});
    } catch (e) {}
  }

  window.addEventListener('error', function (e) {
    // ignore le "Script error." generique sans info utile (erreurs cross-origin)
    if (e.message === 'Script error.' && !e.filename) return;
    report(e.message, e.error && e.error.stack);
  });

  window.addEventListener('unhandledrejection', function (e) {
    var reason = e.reason;
    var message = reason && reason.message ? reason.message : String(reason);
    var stack = reason && reason.stack ? reason.stack : '';
    report('Promesse rejetee non geree: ' + message, stack);
  });
})();
