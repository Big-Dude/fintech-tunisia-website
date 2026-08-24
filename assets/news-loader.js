// ── JSONBin.io connection ──────────────────────────────────────────────
// Once you've created your bin (see SETUP-NEWS.md), paste its Bin ID below.
// Leaving it as-is just uses the built-in sample articles from news-data.js.
const JSONBIN_ID = "REPLACE_WITH_YOUR_BIN_ID";

const JSONBIN_URL = (typeof JSONBIN_ID === "string" && JSONBIN_ID && JSONBIN_ID !== "REPLACE_WITH_YOUR_BIN_ID")
  ? "https://api.jsonbin.io/v3/b/" + JSONBIN_ID + "/latest"
  : null;

// Returns a Promise that resolves to an array of article objects.
// Tries JSONBin first (so daily edits there show up with zero redeploys);
// falls back to the local NEWS_ARTICLES array from news-data.js if the
// bin isn't set up yet, or the request fails for any reason.
function loadNewsArticles(){
  var fallback = (typeof NEWS_ARTICLES !== "undefined") ? NEWS_ARTICLES : [];
  if(!JSONBIN_URL){
    return Promise.resolve(fallback);
  }
  return fetch(JSONBIN_URL, { headers: { "X-Bin-Meta": "false" } })
    .then(function(res){
      if(!res.ok) throw new Error("JSONBin request failed: " + res.status);
      return res.json();
    })
    .then(function(data){
      var articles = data && data.articles ? data.articles : (data && data.record ? data.record.articles : null);
      return (Array.isArray(articles) && articles.length) ? articles : fallback;
    })
    .catch(function(err){
      console.warn("Falling back to local news-data.js —", err.message);
      return fallback;
    });
}
