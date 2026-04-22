import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

st.set_page_config(page_title="NBA Dashboard", page_icon="🏀", layout="wide")

# ── Colores NBA ───────────────────────────────────────────────────────────────
WIN_COLOR  = "#1D428A"
LOSS_COLOR = "#C8102E"

# ── CSS mínimo ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stSidebar"] { background-color: #f7f7f7; }
div[data-testid="stPills"] button[aria-checked="true"] {
    background-color: #1D428A !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("nba_all_elo.csv")

df = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.title("🏀 NBA Dashboard")
st.sidebar.markdown("---")

years = sorted(df["year_id"].unique())
selected_year = st.sidebar.selectbox("Año", years, index=len(years) - 1)

teams = sorted(df[df["year_id"] == selected_year]["team_id"].unique())
selected_team = st.sidebar.selectbox("Equipo", teams)

game_type = st.sidebar.pills(
    "Tipo de juego",
    options=["Temporada regular", "Playoffs", "Ambos"],
    default="Ambos",
)

# ── Filtrado ──────────────────────────────────────────────────────────────────
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
st.title(f"🏀 {selected_team} · {selected_year}")
st.caption(f"{game_type}  ·  {total_g} juegos disputados")
st.divider()

if total_g == 0:
    st.warning("No hay datos para los filtros seleccionados.")
    st.stop()

# ── Métricas ──────────────────────────────────────────────────────────────────
c1, c2, c3 = st.columns(3)
c1.metric("Victorias",  total_w)
c2.metric("Derrotas",   total_l)
c3.metric("% Victorias", f"{win_pct:.1f}%")

st.divider()

# ── Gráfica de líneas ─────────────────────────────────────────────────────────
st.subheader("Acumulado de victorias y derrotas")

fig, ax = plt.subplots(figsize=(10, 4))
x = filtered.index + 1

ax.plot(x, filtered["cum_wins"],   color=WIN_COLOR,  linewidth=2, label=f"Victorias ({total_w})")
ax.plot(x, filtered["cum_losses"], color=LOSS_COLOR, linewidth=2, label=f"Derrotas ({total_l})")
ax.fill_between(x, filtered["cum_wins"],   alpha=0.1, color=WIN_COLOR)
ax.fill_between(x, filtered["cum_losses"], alpha=0.1, color=LOSS_COLOR)

ax.set_xlabel("Juego #")
ax.set_ylabel("Acumulado")
ax.legend()
ax.grid(alpha=0.3, linestyle="--")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.tight_layout()
st.pyplot(fig)

st.divider()

# ── Gráfica de pastel ─────────────────────────────────────────────────────────
st.subheader("Distribución de resultados")

_, col, _ = st.columns([1.5, 2, 1.5])
with col:
    fig2, ax2 = plt.subplots(figsize=(5, 5))
    wedges, texts, autotexts = ax2.pie(
        [total_w, total_l],
        labels=["Victorias", "Derrotas"],
        colors=[WIN_COLOR, LOSS_COLOR],
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops=dict(edgecolor="white", linewidth=2),
    )
    for at in autotexts:
        at.set_fontsize(12)
        at.set_fontweight("bold")
        at.set_color("white")
    fig2.tight_layout()
    st.pyplot(fig2)
