import json
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

THEMES = {
    "Violet": ("#7C5CFC", "#D16BFF", "#4FD1F5"),
    "Océan": ("#0EA5E9", "#6366F1", "#22D3EE"),
    "Émeraude": ("#10B981", "#14B8A6", "#84CC16"),
    "Soleil": ("#F97316", "#EC4899", "#FACC15"),
}
PERIODES = {"30 jours": 30, "90 jours": 90, "6 mois": 182, "12 mois": 365}
PAGES = {"Vue d'ensemble": ":material/dashboard:",
         "Produits": ":material/inventory_2:",
         "Clients": ":material/groups:"}

st.set_page_config(page_title="Ventix", page_icon="◐", layout="wide")


# ---------- Outils ----------
def rgb(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
def rgba(h, a): r, g, b = rgb(h); return f"rgba({r},{g},{b},{a})"
def tint(h): return "#%02x%02x%02x" % tuple((v + 255) // 2 for v in rgb(h))
def fmt(x): return f"{x:,.0f}".replace(",", " ")


def delta_html(c, p):
    if not p or pd.isna(p):
        return '<span class="lab">—</span>'
    d = (c - p) / p * 100
    cls, fl = ("up", "▲") if d >= 0 else ("down", "▼")
    return f'<span class="{cls}">{fl} {abs(d):.1f}%</span>'


@st.cache_data
def charger():
    return pd.read_csv("data/ventes.csv", parse_dates=["date"])


df = charger()

# ---------- Barre de gauche ----------
if "page" not in st.session_state:
    st.session_state.page = "Vue d'ensemble"


def aller(p):
    st.session_state.page = p


with st.sidebar:
    st.markdown('<div class="logo"><div class="logo-dot"></div>Ventix</div>'
                '<div class="nav-label">MENU</div>', unsafe_allow_html=True)
    for i, (nom, ico) in enumerate(PAGES.items()):
        actif = st.session_state.page == nom
        st.button(nom, icon=ico, key=f"{'navon' if actif else 'nav'}_{i}",
                  on_click=aller, args=(nom,), use_container_width=True)

    st.markdown('<div class="nav-label">THÈME</div>', unsafe_allow_html=True)
    theme_nom = st.pills("Thème", list(THEMES), default="Violet",
                         label_visibility="collapsed") or "Violet"

    st.markdown('<div class="nav-label">DONNÉES</div>', unsafe_allow_html=True)
    with st.expander("Filtres"):
        produits = st.multiselect("Produits", sorted(df["produit"].unique()),
                                  default=sorted(df["produit"].unique()))
        villes = st.multiselect("Villes", sorted(df["ville"].unique()),
                                default=sorted(df["ville"].unique()))

A, B, C = THEMES[theme_nom]
PAL = [A, B, C, tint(A), tint(B), tint(C)]
ROOT = (f":root{{--a:{A};--b:{B};--c:{C};"
        f"--soft:{rgba(A, .10)};--glow:{rgba(A, .35)};}}")

# ---------- Style de la page ----------
st.markdown(f"<style>{ROOT}</style>", unsafe_allow_html=True)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
.stApp { background: linear-gradient(180deg, #F4F5FB, #ECEEFB); }
header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 1.5rem; max-width: 1400px; }

section[data-testid="stSidebar"] { background: #fff; border-right: 1px solid #ECEEF7; }
.logo { display:flex; align-items:center; gap:12px; font-size:1.35rem; font-weight:700;
        color:#1F2347; margin: 4px 0 10px 4px; }
.logo-dot { width:36px; height:36px; border-radius:50%;
            background: linear-gradient(135deg, var(--a), var(--c));
            box-shadow: 0 6px 16px var(--glow); animation: pulse 3s ease-in-out infinite; }
@keyframes pulse { 50% { transform: scale(1.1); } }
.nav-label { font-size:.7rem; letter-spacing:2px; color:#A0A5C3; font-weight:600;
             margin: 24px 0 8px 6px; }

[class*="st-key-nav"] button { border:none; border-radius:14px; padding:.75rem 1rem;
                               transition: all .25s ease; box-shadow:none; }
[class*="st-key-nav"] button > div { justify-content:flex-start; width:100%; gap:.6rem; }
[class*="st-key-nav_"] button { background: transparent; }
[class*="st-key-nav_"] button p, [class*="st-key-nav_"] button span
    { color:#5B6190; font-weight:500; font-size:.95rem; }
[class*="st-key-nav_"] button:hover { background: var(--soft); transform: translateX(6px); }
[class*="st-key-nav_"] button:hover p, [class*="st-key-nav_"] button:hover span
    { color: var(--a); }
[class*="st-key-navon_"] button { background: linear-gradient(90deg, var(--a), var(--b));
                                  box-shadow: 0 8px 22px var(--glow); }
[class*="st-key-navon_"] button p, [class*="st-key-navon_"] button span
    { color:#fff; font-weight:600; font-size:.95rem; }

.page-title { font-size:1.7rem; font-weight:600; color:#1F2347; margin:4px 0 0 0;
              animation: fade .6s ease backwards; }
.page-sub { color:#8A8FB0; font-size:.9rem; }
@keyframes fade { from { opacity:0; transform: translateY(-10px); } }
.stDownloadButton button { border-radius:12px; border:1px solid var(--a); color:var(--a); }
.stDownloadButton button:hover { background: var(--a); color:#fff; }

/* ========== Pills THÈME + période (compatible thème) ========== */
[data-testid="stBaseButton-pills"] {
  background: transparent !important;
  border: 1px solid #E2E5F0 !important;
  color: #5B6190 !important;
  border-radius: 20px !important;
  font-weight: 500 !important;
  transition: all .2s ease !important;
}
[data-testid="stBaseButton-pills"]:hover {
  background: var(--soft) !important;
  border-color: var(--a) !important;
  color: var(--a) !important;
}
[kind="pillsActive"][data-testid="stBaseButton-pillsActive"],
[data-testid="stBaseButton-pillsActive"] {
  background: linear-gradient(90deg, var(--a), var(--b)) !important;
  border: none !important;
  color: #fff !important;
  box-shadow: 0 4px 14px var(--glow) !important;
  font-weight: 600 !important;
}

/* ========== Chips + conteneur Produits / Villes ========== */
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
  background-color: #ffffff !important;
  border: 1px solid #E2E5F0 !important;
  border-radius: 12px !important;
}

section[data-testid="stSidebar"] span[data-baseweb="tag"] {
  background-color: var(--a) !important;
  color: #ffffff !important;
  border-radius: 8px !important;
  border: none !important;
  font-weight: 500 !important;
}

section[data-testid="stSidebar"] span[data-baseweb="tag"] span {
  color: #ffffff !important;
}

section[data-testid="stSidebar"] span[data-baseweb="tag"] span[role="button"] {
  color: rgba(255,255,255,.85) !important;
}

section[data-testid="stSidebar"] span[data-baseweb="tag"] span[role="button"]:hover {
  color: #ffffff !important;
}

/* ========== Rendre le mot "Filtres" bien lisible ========== */
section[data-testid="stSidebar"] [data-testid="stExpander"] details summary {
  background: var(--soft) !important;
  border-radius: 10px !important;
  color: var(--a) !important;
  font-weight: 600 !important;
  border: 1px solid transparent !important;
}
section[data-testid="stSidebar"] [data-testid="stExpander"] details summary:hover {
  background: var(--a) !important;
  color: #fff !important;
}
section[data-testid="stSidebar"] [data-testid="stExpander"] details summary p,
section[data-testid="stSidebar"] [data-testid="stExpander"] details summary span {
  color: inherit !important;
  font-weight: 600 !important;
}

/* ========== Même style pour les libellés Produits et Villes ========== */
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
  background: var(--soft) !important;
  color: var(--a) !important;
  font-weight: 600 !important;
  padding: 4px 10px !important;
  border-radius: 8px !important;
  display: inline-block !important;
}

/* ========== CONTENU Produits & Villes (Dropdown & Popover) – Harmonisés en mode clair/thème ========== */
div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
div[data-baseweb="menu"],
ul[role="listbox"] {
  background-color: #ffffff !important;
  border: 1px solid var(--a) !important;
  border-radius: 12px !important;
  box-shadow: 0 8px 24px var(--glow) !important;
}

div[data-baseweb="popover"] li,
div[data-baseweb="menu"] li,
ul[role="listbox"] li,
li[role="option"] {
  background-color: #ffffff !important;
  color: #1F2347 !important;
  font-weight: 500 !important;
  border-radius: 8px !important;
  margin: 2px 6px !important;
}

div[data-baseweb="popover"] li:hover,
div[data-baseweb="menu"] li:hover,
ul[role="listbox"] li:hover,
li[role="option"]:hover {
  background-color: var(--soft) !important;
  color: var(--a) !important;
}

div[data-baseweb="popover"] li[aria-selected="true"],
div[data-baseweb="menu"] li[aria-selected="true"],
ul[role="listbox"] li[aria-selected="true"],
li[role="option"][aria-selected="true"] {
  background-color: var(--a) !important;
  color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- Cartes animées (HTML + CSS + JS) ----------
BASE = """
*{box-sizing:border-box;margin:0;font-family:'Poppins',sans-serif}
html,body{height:100%}
body{background:transparent;padding:8px;color:#1F2347}
.card{background:#fff;border-radius:20px;padding:20px 24px;height:calc(100vh - 16px);
 box-shadow:0 6px 24px rgba(31,35,71,.08);animation:in .6s ease backwards;
 transition:transform .25s,box-shadow .25s}
.card:hover{transform:translateY(-5px);box-shadow:0 16px 36px rgba(31,35,71,.16)}
@keyframes in{from{opacity:0;transform:translateY(20px)}}
.head{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
.t{font-weight:600;font-size:1rem}
.big{font-weight:600;font-size:1.4rem;color:var(--a)}
.up{color:#22C55E;font-size:.8rem;font-weight:600}
.down{color:#EF4444;font-size:.8rem;font-weight:600}
.lab{color:#8A8FB0;font-size:.85rem}
"""
COUNT = """
document.querySelectorAll('[data-v]').forEach(function(el){
 var t=+el.dataset.v,u=el.dataset.u||'',s=performance.now();
 (function f(n){var p=Math.min((n-s)/1300,1),e=1-Math.pow(1-p,3);
  el.textContent=Math.round(t*e).toLocaleString('fr-FR')+u;
  if(p<1)requestAnimationFrame(f)})(s)});
"""
PLOTLY = "<script src='https://cdn.plot.ly/plotly-2.35.2.min.js'></script>"


def html_card(body, h, css="", js="", lib=""):
    components.html(
        "<!doctype html><html><head><meta charset='utf-8'>"
        "<link href='https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap' rel='stylesheet'>"
        f"<style>{ROOT}{BASE}{css}</style>{lib}</head>"
        f"<body>{body}<script>{COUNT}{js}</script></body></html>", height=h)


KPI_CSS = """
.g{display:grid;grid-template-columns:1fr 1fr;gap:16px;height:calc(100vh - 16px)}
.k{height:auto}
.ico{width:38px;height:38px;border-radius:12px;background:var(--soft);display:flex;
 align-items:center;justify-content:center;font-size:18px}
.v{font-size:1.8rem;font-weight:600;margin-top:12px}
.gr{background:linear-gradient(135deg,var(--a),var(--b) 55%,var(--c));color:#fff}
.gr .lab{color:rgba(255,255,255,.85)} .gr .ico{background:rgba(255,255,255,.25)}
.gr .up,.gr .down{color:#fff}
"""


def kpi_grid(items):
    cartes = ""
    for i, (ico, lab, val, suf, delta, grad) in enumerate(items):
        cartes += (f'<div class="card k{" gr" if grad else ""}" style="animation-delay:{i * .1}s">'
                   f'<div class="head"><div class="ico">{ico}</div>{delta}</div>'
                   f'<div class="v" data-v="{val:.0f}" data-u="{suf}">0</div>'
                   f'<div class="lab">{lab}</div></div>')
    html_card(f'<div class="g">{cartes}</div>', 340, KPI_CSS)


LINE_JS = """
var x=%X%,y=%Y%;
Plotly.newPlot('c',[{x:x,y:y.map(function(){return 0}),type:'scatter',mode:'lines',
 line:{color:'%A%',width:3,shape:'spline'},fill:'tozeroy',fillcolor:'%F%',
 hovertemplate:'<b>%{y:,.0f} DT</b><br>%{x|%d %b %Y}<extra></extra>'}],
 {margin:{l:55,r:10,t:10,b:30},paper_bgcolor:'rgba(0,0,0,0)',plot_bgcolor:'rgba(0,0,0,0)',
  font:{family:'Poppins',color:'#8A8FB0',size:11},hovermode:'x',
  xaxis:{showgrid:false,showspikes:true,spikemode:'across',spikecolor:'%A%',spikethickness:1,spikedash:'solid'},
  yaxis:{gridcolor:'#EEF0F8',zeroline:false,range:[0,%M%]},
  hoverlabel:{bgcolor:'#1F2347',bordercolor:'#1F2347',font:{color:'#fff',family:'Poppins'}}},
 {displayModeBar:false,responsive:true}
).then(function(g){Plotly.animate(g,{data:[{y:y}]},
 {transition:{duration:1400,easing:'cubic-in-out'},frame:{duration:1400}})});
"""


def courbe(d, jours, total):
    regle = "D" if jours <= 30 else "W" if jours <= 182 else "MS"
    s = d.set_index("date")["montant"].resample(regle).sum().reset_index()
    js = (LINE_JS.replace("%X%", json.dumps(s["date"].dt.strftime("%Y-%m-%d").tolist()))
          .replace("%Y%", json.dumps([int(round(v)) for v in s["montant"]]))
          .replace("%A%", A).replace("%F%", rgba(A, .10))
          .replace("%M%", str(int(s["montant"].max() * 1.15) + 1)))
    body = ("<div class='card'><div class='head'><span class='t'>Chiffre d'affaires</span>"
            f"<span class='big' data-v='{total:.0f}' data-u=' DT'>0</span></div>"
            "<div id='c' style='height:250px'></div></div>")
    html_card(body, 340, "", js, PLOTLY)


DONUT_CSS = """
.row{display:flex;gap:20px;align-items:center}
.mini{flex:1;border-collapse:collapse;font-size:.9rem}
.mini th{text-align:left;color:#8A8FB0;font-weight:500;padding:8px 6px;background:#F7F8FD}
.mini td{padding:10px 6px;border-bottom:1px solid #F0F1F8}
.r{text-align:right;font-weight:600}
.dot{display:inline-block;width:10px;height:10px;border-radius:4px;margin-right:10px}
.ring{position:relative;width:200px;height:200px;flex:none}
.ring svg{width:100%;height:100%}
.ring circle{animation:draw 1.2s ease backwards;transition:stroke-width .2s}
.ring circle:hover{stroke-width:18}
.mid{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center}
.mid b{font-size:1.9rem;color:var(--a)} .mid span{color:#8A8FB0;font-size:.8rem}
@keyframes draw{from{stroke-dasharray:0 290}}
"""


def anneau(titre, serie):
    serie = serie.sort_values(ascending=False).head(6)
    tot, R = serie.sum(), 46
    circ, off, cercles, lignes = 2 * 3.14159265 * R, 0, "", ""
    for i, (nom, v) in enumerate(serie.items()):
        L = v / tot * circ
        cercles += (f'<circle cx="60" cy="60" r="{R}" fill="none" stroke="{PAL[i]}" stroke-width="14" '
                    f'stroke-dasharray="{max(L - 2, 0):.2f} {circ:.2f}" stroke-dashoffset="{-off:.2f}" '
                    f'transform="rotate(-90 60 60)" style="animation-delay:{.3 + i * .15}s"/>')
        off += L
        lignes += (f'<tr><td><span class="dot" style="background:{PAL[i]}"></span>{i + 1}</td>'
                   f'<td>{nom}</td><td class="r">{v / tot * 100:.0f}%</td></tr>')
    body = (f"<div class='card'><div class='head'><span class='t'>{titre}</span></div><div class='row'>"
            f"<table class='mini'><tr><th>#</th><th>Nom</th><th style='text-align:right'>Part</th></tr>{lignes}</table>"
            f"<div class='ring'><svg viewBox='0 0 120 120'>{cercles}</svg>"
            f"<div class='mid'><b data-v='{serie.iloc[0] / tot * 100:.0f}' data-u='%'>0%</b>"
            f"<span>{serie.index[0]}</span></div></div></div></div>")
    html_card(body, 300, DONUT_CSS)


BARS_CSS = """
.b{display:grid;grid-template-columns:110px 1fr 100px 60px;gap:12px;align-items:center;
 padding:7px 0;font-size:.9rem}
.n{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-weight:500}
.tr{height:12px;background:#F0F1F8;border-radius:8px;overflow:hidden}
.f{height:100%;width:var(--w);border-radius:8px;background:linear-gradient(90deg,var(--a),var(--b));
 animation:grow 1.1s cubic-bezier(.2,.8,.2,1) backwards}
@keyframes grow{from{width:0}}
.val{text-align:right;font-weight:600}
"""


def barres(titre, serie, deltas=None):
    serie = serie.sort_values(ascending=False).head(10)
    mx, lignes = serie.max(), ""
    for i, (nom, v) in enumerate(serie.items()):
        dh = "<span></span>"
        if deltas is not None and deltas.get(nom) is not None and not pd.isna(deltas.get(nom)):
            d = deltas[nom]
            dh = f'<span class="{"up" if d >= 0 else "down"}">{"▲" if d >= 0 else "▼"} {abs(d):.0f}%</span>'
        lignes += (f'<div class="b"><span class="n">{nom}</span><div class="tr">'
                   f'<div class="f" style="--w:{v / mx * 100:.1f}%;animation-delay:{i * .08}s"></div></div>'
                   f'<span class="val">{fmt(v)} DT</span>{dh}</div>')
    body = f"<div class='card'><div class='head'><span class='t'>{titre}</span></div>{lignes}</div>"
    html_card(body, 90 + len(serie) * 42, BARS_CSS)


# ---------- Filtres et période ----------
df = df[df["produit"].isin(produits) & df["ville"].isin(villes)]
if df.empty:
    st.warning("Aucune donnée pour ces filtres.")
    st.stop()

h1, h2 = st.columns([3, 2])
h1.markdown('<p class="page-title">Statistiques des ventes</p>'
            '<p class="page-sub">Performance commerciale en temps réel</p>', unsafe_allow_html=True)
with h2:
    periode = st.pills("Période", list(PERIODES), default="30 jours",
                       label_visibility="collapsed") or "30 jours"

jours = PERIODES[periode]
fin = df["date"].max()
actuel = df[df["date"] > fin - pd.Timedelta(days=jours)]
precedent = df[(df["date"] <= fin - pd.Timedelta(days=jours)) &
               (df["date"] > fin - pd.Timedelta(days=2 * jours))]
if actuel.empty:
    st.warning("Aucune vente sur cette période.")
    st.stop()
st.write("")

page = st.session_state.page

# ---------- Pages ----------
if page == "Vue d'ensemble":
    ca, ca_p = actuel["montant"].sum(), precedent["montant"].sum()
    g, d = st.columns([1.25, 1])
    with g:
        courbe(actuel, jours, ca)
    with d:
        kpi_grid([
            ("💰", "Chiffre d'affaires", ca, " DT", delta_html(ca, ca_p), True),
            ("🧾", "Nombre de ventes", len(actuel), "", delta_html(len(actuel), len(precedent)), False),
            ("🛒", "Panier moyen", actuel["montant"].mean(), " DT",
             delta_html(actuel["montant"].mean(), precedent["montant"].mean() if len(precedent) else 0), False),
            ("👤", "Clients actifs", actuel["client"].nunique(), "",
             delta_html(actuel["client"].nunique(), precedent["client"].nunique()), False),
        ])
    c1, c2 = st.columns(2)
    with c1:
        anneau("Répartition par ville", actuel.groupby("ville")["montant"].sum())
    with c2:
        anneau("Répartition par catégorie", actuel.groupby("categorie")["montant"].sum())

elif page == "Produits":
    cur = actuel.groupby("produit")["montant"].sum()
    prev = precedent.groupby("produit")["montant"].sum()
    deltas = {p: ((cur[p] - prev[p]) / prev[p] * 100 if p in prev and prev[p] else None) for p in cur.index}
    g, d = st.columns([1.2, 1])
    with g:
        barres("Chiffre d'affaires par produit", cur, deltas)
    with d:
        anneau("Part par catégorie", actuel.groupby("categorie")["montant"].sum())

else:
    g, d = st.columns([1.2, 1])
    with g:
        barres("Top 10 clients", actuel.groupby("client")["montant"].sum())
    with d:
        anneau("Clients par ville", actuel.groupby("ville")["montant"].sum())

st.sidebar.download_button("⬇ Exporter la période (CSV)",
                           data=actuel.to_csv(index=False).encode("utf-8"),
                           file_name="ventes_periode.csv", mime="text/csv")