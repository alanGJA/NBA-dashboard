import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import rcParams

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NBA Stats Dashboard",
    page_icon="🏀",
    layout="wide",
)

# ── NBA color palette ─────────────────────────────────────────────────────────
WIN_COLOR  = "#1D428A"   # NBA blue  → wins
LOSS_COLOR = "#C8102E"   # NBA red   → losses
BG_DARK    = "#0A1628"
BG_CARD    = "#122040"

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Barlow', sans-serif; }

.stApp { background-color: #0A1628; color: #FFFFFF; }

section[data-testid="stSidebar"] {
    background-color: #122040 !important;
    border-right: 3px solid #C8102E;
}
section[data-testid="stSidebar"] * { color: #FFFFFF !important; }
section[data-testid="stSidebar"] label {
    color: #AABBD4 !important;
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 0.85rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.stSelectbox div[data-baseweb="select"] > div {
    background-color: #1D3461 !important;
    border: 1px solid #1D428A !important;
    border-radius: 6px !important;
    color: #FFFFFF !important;
}

div[data-testid="stPills"] button {
    background-color: #1D3461 !important;
    color: #AABBD4 !important;
    border: 1px solid #1D428A !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-weight: 600 !important;
}
div[data-testid="stPills"] button[aria-checked="true"] {
    background-color: #C8102E !important;
    color: #FFFFFF !important;
    border: 1px solid #C8102E !important;
}

.metric-card {
    background: linear-gradient(135deg, #122040 0%, #1D3461 100%);
    border: 1px solid #1D428A;
    border-radius: 12px;
    padding: 20px 24px;
    text-align: center;
    margin-bottom: 8px;
}
.metric-label {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 0.75rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #AABBD4;
    margin-bottom: 4px;
}
.metric-value {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    line-height: 1;
}
.metric-win  { color: #4A90D9; }
.metric-loss { color: #C8102E; }
.metric-pct  { color: #F5C842; }

.section-header {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #AABBD4;
    border-left: 4px solid #C8102E;
    padding-left: 12px;
    margin: 24px 0 16px 0;
}

.nba-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: #FFFFFF;
    line-height: 1;
}
.nba-subtitle {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.1rem;
    color: #AABBD4;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-top: 4px;
}
.title-divider {
    height: 3px;
    background: linear-gradient(90deg, #C8102E, #1D428A, transparent);
    margin: 12px 0 24px 0;
    border-radius: 2px;
}
</style>
""", unsafe_allow_html=True)

# ── Matplotlib global style ───────────────────────────────────────────────────
rcParams.update({
    "font.family":      "DejaVu Sans",
    "axes.facecolor":   BG_CARD,
    "figure.facecolor": BG_CARD,
    "text.color":       "#FFFFFF",
    "axes.labelcolor":  "#AABBD4",
    "xtick.color":      "#AABBD4",
    "ytick.color":      "#AABBD4",
    "axes.edgecolor":   "#1D3461",
    "grid.color":       "#1D3461",
    "grid.alpha":       0.5,
    "axes.spines.top":  False,
    "axes.spines.right": False,
})

# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("nba_all_elo.csv")

df = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:16px 0 24px 0;'>
        <span style='font-family:"Barlow Condensed",sans-serif; font-size:2rem;
                     font-weight:800; color:#FFFFFF; letter-spacing:0.06em;'>
            🏀 NBA STATS
        </span>
    </div>
    """, unsafe_allow_html=True)

    years = sorted(df["year_id"].unique())
    selected_year = st.selectbox("Año", years, index=len(years) - 1)

    teams_in_year = sorted(df[df["year_id"] == selected_year]["team_id"].unique())
    selected_team = st.selectbox("Equipo", teams_in_year)

    game_type = st.pills(
        "Tipo de juego",
        options=["Temporada regular", "Playoffs", "Ambos"],
        default="Ambos",
    )

    st.markdown("<hr style='border-color:#1D3461; margin:24px 0 16px 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-family:"Barlow Condensed",sans-serif; font-size:0.7rem;
                color:#AABBD4; letter-spacing:0.1em; text-transform:uppercase;'>
        Fuente: FiveThirtyEight NBA ELO
    </div>
    """, unsafe_allow_html=True)

# ── Filter ────────────────────────────────────────────────────────────────────
filtered = df[
    (df["year_id"] == selected_year) & (df["team_id"] == selected_team)
].copy()

if game_type == "Temporada regular":
    filtered = filtered[filtered["is_playoffs"] == 0]
elif game_type == "Playoffs":
    filtered = filtered[filtered["is_playoffs"] == 1]

filtered = filtered.sort_values("seasongame").reset_index(drop=True)
filtered["cum_wins"]   = (filtered["game_result"] == "W").cumsum()
filtered["cum_losses"] = (filtered["game_result"] == "L").cumsum()

total_w = int((filtered["game_result"] == "W").sum())
total_l = int((filtered["game_result"] == "L").sum())
total_g = total_w + total_l
win_pct = (total_w / total_g * 100) if total_g > 0 else 0

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="nba-title">{selected_team} <span style="color:#C8102E;">·</span> {selected_year}</div>
<div class="nba-subtitle">{game_type} &nbsp;·&nbsp; {total_g} juegos disputados</div>
<div class="title-divider"></div>
""", unsafe_allow_html=True)

# ── Metric cards ──────────────────────────────────────────────────────────────
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Victorias</div>
        <div class="metric-value metric-win">{total_w}</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Derrotas</div>
        <div class="metric-value metric-loss">{total_l}</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">% Victorias</div>
        <div class="metric-value metric-pct">{win_pct:.1f}%</div>
    </div>""", unsafe_allow_html=True)

if total_g == 0:
    st.warning("No hay datos para los filtros seleccionados.")
    st.stop()

# ── Line chart ────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Acumulado de victorias y derrotas</div>', unsafe_allow_html=True)

fig, ax = plt.subplots(figsize=(11, 4))
x = filtered.index + 1

ax.fill_between(x, filtered["cum_wins"],   alpha=0.15, color=WIN_COLOR)
ax.fill_between(x, filtered["cum_losses"], alpha=0.15, color=LOSS_COLOR)
ax.plot(x, filtered["cum_wins"],   color=WIN_COLOR,  linewidth=2.5, label="Victorias")
ax.plot(x, filtered["cum_losses"], color=LOSS_COLOR, linewidth=2.5, label="Derrotas")
ax.scatter([int(x[-1])], [filtered["cum_wins"].iloc[-1]],   color=WIN_COLOR,  s=80, zorder=5)
ax.scatter([int(x[-1])], [filtered["cum_losses"].iloc[-1]], color=LOSS_COLOR, s=80, zorder=5)

ax.set_xlabel("Juego #", fontsize=10, labelpad=8)
ax.set_ylabel("Acumulado", fontsize=10, labelpad=8)
ax.legend(
    handles=[
        mpatches.Patch(color=WIN_COLOR,  label=f"Victorias ({total_w})"),
        mpatches.Patch(color=LOSS_COLOR, label=f"Derrotas ({total_l})"),
    ],
    facecolor="#1D3461", edgecolor="#1D428A",
    labelcolor="white", fontsize=10, loc="upper left",
)
ax.grid(axis="y", linestyle="--")
fig.tight_layout(pad=1.5)
st.pyplot(fig)

# ── Pie chart ─────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Distribución de resultados</div>', unsafe_allow_html=True)

_, col_pie, _ = st.columns([1.5, 2, 1.5])
with col_pie:
    fig2, ax2 = plt.subplots(figsize=(5, 5), subplot_kw=dict(aspect="equal"))
    wedges, texts, autotexts = ax2.pie(
        [total_w, total_l],
        labels=["Victorias", "Derrotas"],
        colors=[WIN_COLOR, LOSS_COLOR],
        autopct="%1.1f%%",
        startangle=90,
        pctdistance=0.75,
        wedgeprops=dict(width=0.55, edgecolor=BG_DARK, linewidth=3),
    )
    for t in texts:
        t.set_color("#AABBD4"); t.set_fontsize(11)
    for at in autotexts:
        at.set_color("#FFFFFF"); at.set_fontsize(12); at.set_fontweight("bold")

    ax2.text(0, 0, f"{win_pct:.0f}%\nW",
             ha="center", va="center",
             fontsize=20, fontweight="bold", color="#FFFFFF")
    fig2.tight_layout(pad=0.5)
    st.pyplot(fig2)
