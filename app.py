"""
Basketball Player Portfolio & Stats Tracker
Renad Soliman "Renoo" -- Point Guard #23
"""

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import date
import os

# Page Config
st.set_page_config(
    page_title="Renad Soliman #23 — بطلة الثلاثيات",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Global CSS
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;900&family=Roboto+Mono:wght@400;600&display=swap');
  @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');

  html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 1.2rem; padding-bottom: 2rem; }
  .stApp {
      background: radial-gradient(ellipse at 10% 0%, #0f172a 0%, #020617 60%, #0f172a 100%);
  }
  .stTabs [data-baseweb="tab-list"] {
      gap: 6px; background: rgba(255,255,255,0.04); border-radius: 14px;
      padding: 6px; border: 1px solid rgba(255,255,255,0.08);
  }
  .stTabs [data-baseweb="tab"] {
      border-radius: 10px; padding: 10px 28px; font-weight: 600;
      font-size: 0.95rem; color: #94a3b8; transition: all 0.3s ease;
  }
  .stTabs [aria-selected="true"] {
      background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
      color: #fff !important; box-shadow: 0 4px 20px rgba(59,130,246,0.45);
  }
  .hero-card {
      background: linear-gradient(135deg, rgba(255,255,255,0.07) 0%, rgba(255,255,255,0.02) 100%);
      border: 1px solid rgba(59,130,246,0.2); border-radius: 24px; padding: 2rem 2.2rem;
      backdrop-filter: blur(12px); box-shadow: 0 8px 40px rgba(0,0,0,0.5);
      margin-bottom: 2rem;
  }
  .profile-img {
      width: 100%; max-width: 320px; border-radius: 20px;
      border: 2px solid rgba(59,130,246,0.35);
      box-shadow: 0 12px 35px rgba(0,0,0,0.6), 0 0 25px rgba(59,130,246,0.25);
      display: block; margin: 0 auto; object-fit: cover;
  }
  .hero-name {
      font-size: 3.2rem; font-weight: 900; line-height: 1.05;
      background: linear-gradient(135deg, #ffffff 0%, #38bdf8 50%, #3b82f6 100%);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
      background-clip: text; margin: 0; letter-spacing: -0.02em;
  }
  .hero-nickname { font-size: 1.1rem; color: #7dd3fc; font-style: italic; margin-top: 0.1rem; }
  .hero-sub { font-size: 0.95rem; color: #64748b; margin-top: 0.3rem; font-weight: 400; }
  .badge {
      display: inline-block; background: linear-gradient(135deg, #3b82f6, #1d4ed8);
      color: #fff; font-weight: 700; font-size: 0.78rem; letter-spacing: 0.08em;
      padding: 4px 14px; border-radius: 50px; margin-right: 6px; margin-top: 10px;
  }
  .badge-gold { background: linear-gradient(135deg, #f59e0b, #d97706); }
  .slogan-ar {
      font-family: 'Cairo', sans-serif; font-size: 1.5rem; font-weight: 900;
      color: #fbbf24; margin-top: 1rem; letter-spacing: 0.02em;
      text-shadow: 0 0 20px rgba(251,191,36,0.4);
  }
  .playstyle-text { color: #cbd5e1; font-size: 0.95rem; line-height: 1.75; margin-top: 0.8rem; font-weight: 300; }
  .section-header {
      font-size: 1.4rem; font-weight: 700; color: #f1f5f9;
      border-left: 4px solid #3b82f6; padding-left: 14px; margin: 2rem 0 1.2rem 0;
  }
  .timeline-card {
      background: linear-gradient(135deg, rgba(255,255,255,0.06) 0%, rgba(255,255,255,0.02) 100%);
      border: 1px solid rgba(255,255,255,0.1); border-radius: 18px; padding: 1.2rem 1rem;
      text-align: center; transition: transform 0.25s, box-shadow 0.25s; height: 100%;
  }
  .timeline-card:hover { transform: translateY(-5px); box-shadow: 0 10px 30px rgba(59,130,246,0.2); border-color: rgba(59,130,246,0.3); }
  .club-tag { font-size: 0.6rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; padding: 3px 10px; border-radius: 50px; display: inline-block; margin-bottom: 0.6rem; }
  .tag-current  { background:rgba(59,130,246,0.2); color:#60a5fa; border:1px solid rgba(59,130,246,0.4); }
  .tag-previous { background:rgba(99,102,241,0.2); color:#818cf8; border:1px solid rgba(99,102,241,0.35); }
  .tag-first    { background:rgba(20,184,166,0.2); color:#2dd4bf; border:1px solid rgba(20,184,166,0.35); }
  .tag-youth    { background:rgba(234,179,8,0.2);  color:#facc15; border:1px solid rgba(234,179,8,0.35); }
  .club-num     { font-size:0.65rem; color:#475569; font-weight:600; margin-bottom:0.2rem; }
  .club-name    { font-size:0.95rem; font-weight:700; color:#f1f5f9; margin:0.4rem 0 0.1rem 0; }
  .club-years   { font-size:0.75rem; color:#64748b; }
  .metric-grid {
      display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-top: 1.2rem;
  }
  @media (max-width: 640px) {
      .metric-grid { grid-template-columns: repeat(2, 1fr); gap: 8px; }
  }
  .metric-box {
      background: linear-gradient(135deg, rgba(59,130,246,0.12), rgba(29,78,216,0.07));
      border: 1px solid rgba(59,130,246,0.25); border-radius: 14px; padding: 0.8rem 0.6rem;
      text-align: center;
  }
  .metric-lbl { color: #94a3b8; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 2px; }
  .metric-num { color: #60a5fa; font-size: 1.55rem; font-weight: 900; font-family: 'Roboto Mono', monospace; }
  [data-testid="stMetric"] {
      background: linear-gradient(135deg, rgba(59,130,246,0.12), rgba(29,78,216,0.07));
      border: 1px solid rgba(59,130,246,0.25); border-radius: 14px; padding: 1rem 1.2rem;
  }
  [data-testid="stMetricLabel"] { color: #94a3b8 !important; }
  [data-testid="stMetricValue"] { color: #60a5fa !important; font-family: 'Roboto Mono', monospace; }
  .lock-card {
      background: linear-gradient(135deg, rgba(255,255,255,0.07), rgba(255,255,255,0.02));
      border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 2.5rem;
      max-width: 420px; margin: 4rem auto; text-align: center;
  }
  .lock-icon  { font-size: 3rem; margin-bottom: 1rem; }
  .lock-title { font-size: 1.4rem; font-weight: 700; color: #f1f5f9; margin-bottom: 0.4rem; }
  .lock-sub   { font-size: 0.9rem; color: #64748b; margin-bottom: 1.5rem; }
  .db-warning {
      background: linear-gradient(135deg, rgba(234,179,8,0.1), rgba(161,98,7,0.07));
      border: 1px solid rgba(234,179,8,0.25); border-radius: 12px; padding: 0.8rem 1.2rem;
      color: #fbbf24; font-size: 0.85rem; margin-bottom: 1rem;
  }
  hr { border-color: rgba(255,255,255,0.06) !important; }
  @media (max-width: 640px) { .hero-name { font-size: 2rem; } .slogan-ar { font-size: 1.2rem; } }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Database helpers
# ─────────────────────────────────────────────
def _try_connect(db_url: str):
    try:
        engine = create_engine(db_url, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS pg23_stats (
                    id           SERIAL PRIMARY KEY,
                    match_date   DATE          NOT NULL,
                    opponent     VARCHAR(120)  NOT NULL,
                    minutes      NUMERIC(5,1)  NOT NULL DEFAULT 0,
                    fg2_made     INT           NOT NULL DEFAULT 0,
                    fg3_made     INT           NOT NULL DEFAULT 0,
                    total_points INT           NOT NULL DEFAULT 0,
                    assists      INT           NOT NULL DEFAULT 0,
                    rebounds     INT           NOT NULL DEFAULT 0,
                    steals       INT           NOT NULL DEFAULT 0,
                    logged_at    TIMESTAMP     NOT NULL DEFAULT NOW()
                );
            """))
            conn.commit()
        return engine
    except Exception:
        return None


@st.cache_resource(show_spinner=False)
def get_engine():
    try:
        db_url = st.secrets["database"]["url"]
    except Exception:
        return None
    if not db_url or "HOST" in db_url or "PASSWORD" in db_url:
        return None
    return _try_connect(db_url)


def load_stats(engine) -> pd.DataFrame:
    if engine is None:
        return pd.DataFrame()
    try:
        with engine.connect() as conn:
            return pd.read_sql(
                text("SELECT * FROM pg23_stats ORDER BY match_date DESC"), conn
            )
    except Exception:
        return pd.DataFrame()


def insert_match(engine, data: dict) -> bool:
    if engine is None:
        return False
    try:
        sql = text("""
            INSERT INTO pg23_stats
                (match_date, opponent, minutes, fg2_made, fg3_made,
                 total_points, assists, rebounds, steals)
            VALUES
                (:match_date, :opponent, :minutes, :fg2_made, :fg3_made,
                 :total_points, :assists, :rebounds, :steals)
        """)
        with engine.connect() as conn:
            conn.execute(sql, data)
            conn.commit()
        return True
    except Exception:
        return False


def season_averages(df: pd.DataFrame) -> dict:
    if df.empty:
        return {k: 0.0 for k in ["ppg", "apg", "rpg", "spg", "mpg", "games"]}
    return {
        "ppg":   round(df["total_points"].mean(), 1),
        "apg":   round(df["assists"].mean(), 1),
        "rpg":   round(df["rebounds"].mean(), 1),
        "spg":   round(df["steals"].mean(), 1),
        "mpg":   round(df["minutes"].mean(), 1),
        "games": len(df),
    }


# ─────────────────────────────────────────────
#  Password gate
# ─────────────────────────────────────────────
def check_tracker_access() -> bool:
    if "tracker_unlocked" not in st.session_state:
        st.session_state["tracker_unlocked"] = False
    if st.session_state["tracker_unlocked"]:
        return True
    st.markdown("""
    <div class='lock-card'>
      <div class='lock-icon'>🔐</div>
      <div class='lock-title'>Private Tracker</div>
      <div class='lock-sub'>Enter your password to log match data.</div>
    </div>
    """, unsafe_allow_html=True)
    _, col, _ = st.columns([1, 2, 1])
    with col:
        pwd = st.text_input("Password", type="password",
                            label_visibility="collapsed",
                            placeholder="Enter password...",
                            key="tracker_pwd")
        if st.button("🔓  Unlock", use_container_width=True):
            correct = st.secrets.get("tracker", {}).get("password", "pg23")
            if pwd == correct:
                st.session_state["tracker_unlocked"] = True
                st.rerun()
            else:
                st.error("Incorrect password.")
    return False


# ═══════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════
def main():
    engine = get_engine()
    db_ok  = engine is not None
    df_all = load_stats(engine)
    avgs   = season_averages(df_all)

    tab1, tab2 = st.tabs(["🏀  Athlete Portfolio", "📊  Match Tracker"])

    # ══════════════════════════════════════════
    #  TAB 1 - PORTFOLIO
    # ══════════════════════════════════════════
    with tab1:

        # -- Hero --
        profile_path = next(
            (p for p in ["profile.png", "profile.jpg", "Renoo_ Point Guard 23.png"]
             if os.path.exists(p)),
            None
        )
        col_img, col_info = st.columns([1, 2], gap="large")

        with col_img:
            if profile_path:
                import base64
                with open(profile_path, "rb") as f:
                    prof_b64 = base64.b64encode(f.read()).decode()
                mime = "image/png" if profile_path.endswith(".png") else "image/jpeg"
                st.markdown(
                    f'<div style="text-align:center;padding:0.5rem 0;"><img src="data:{mime};base64,{prof_b64}" class="profile-img" alt="Renad Soliman"/></div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown("""
                <div style="aspect-ratio:1;background:linear-gradient(135deg,#0f2a4a,#020617);
                    border:2px dashed rgba(59,130,246,0.35);border-radius:20px;
                    display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;">
                  <span style="font-size:5rem;">🏀</span>
                  <span style="color:#475569;font-size:0.78rem;text-align:center;padding:0 1rem;">
                    Add profile.png<br>to the project folder
                  </span>
                </div>
                """, unsafe_allow_html=True)

        with col_info:
            st.markdown("""
            <p class='hero-name'>Renad Soliman</p>
            <p class='hero-nickname'>"Renoo"</p>
            <p class='hero-sub'>Born 9 December 2003 &nbsp;&middot;&nbsp; 22 years old</p>
            <div style="margin-top:0.6rem;">
              <span class='badge'>#23</span>
              <span class='badge'>Point Guard</span>
              <span class='badge badge-gold'>🏆 FIBA</span>
              <span class='badge' style='background:linear-gradient(135deg,#0ea5e9,#0369a1);'>Misr Petroleum</span>
            </div>
            <p class='slogan-ar'>« بطلة الثلاثيات »</p>
            <p class='playstyle-text'>
              A fearless, floor-generalising Point Guard who has become synonymous
              with the long ball — her nickname <em>"Queen of Three-Pointers"</em>
              is earned shot by shot. Renad commands the court with surgical
              court-vision, a devastating first step off the dribble, and the ice-cold
              composure to drain logo-range threes in crunch time.
              Having represented seven clubs across her career, she brings
              championship pedigree and leadership to every locker room she enters.
            </p>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class='metric-grid'>
              <div class='metric-box'><div class='metric-lbl'>🏀 PPG</div><div class='metric-num'>{avgs["ppg"]}</div></div>
              <div class='metric-box'><div class='metric-lbl'>🎯 APG</div><div class='metric-num'>{avgs["apg"]}</div></div>
              <div class='metric-box'><div class='metric-lbl'>💪 RPG</div><div class='metric-num'>{avgs["rpg"]}</div></div>
              <div class='metric-box'><div class='metric-lbl'>🎮 GP</div><div class='metric-num'>{avgs["games"]}</div></div>
            </div>
            """, unsafe_allow_html=True)

        # -- Player Avatar Showcase --
        st.markdown("<div class='section-header'>🌟 Player Avatar</div>",
                    unsafe_allow_html=True)

        avatar_path = next((p for p in ["avatar.png", "avatar.jpg"] if os.path.exists(p)), None)
        if avatar_path:
            import base64, streamlit.components.v1 as components
            with open(avatar_path, "rb") as f:
                avatar_b64 = base64.b64encode(f.read()).decode()
            mime = "image/png" if avatar_path.endswith(".png") else "image/jpeg"

            avatar_html = (
                """<!DOCTYPE html>
<html><head><meta charset="UTF-8"/>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:'Outfit',sans-serif; overflow:hidden; }
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&family=Cairo:wght@700;900&family=Roboto+Mono:wght@600&display=swap');
@keyframes floatAvatar { 0%,100%{transform:translateY(0);} 50%{transform:translateY(-10px);} }
@keyframes pulseGlow {
  0%,100%{box-shadow:0 0 40px rgba(59,130,246,.45),0 20px 60px rgba(0,0,0,.5);}
  50%{box-shadow:0 0 70px rgba(59,130,246,.75),0 20px 60px rgba(0,0,0,.5);}
}
@keyframes shimmer { 0%{background-position:-200% center;} 100%{background-position:200% center;} }
@keyframes drift { 0%{transform:translateY(0) scale(1);opacity:.7;} 100%{transform:translateY(-90px) scale(0);opacity:0;} }
.showcase {
  display:flex; align-items:center; gap:2.5rem;
  background:linear-gradient(135deg,rgba(255,255,255,.05),rgba(59,130,246,.06));
  border:1px solid rgba(59,130,246,.25); border-radius:24px; padding:2rem;
  position:relative; overflow:hidden; height:100%;
}
.showcase::before {
  content:''; position:absolute; inset:0;
  background:radial-gradient(ellipse at 25% 50%,rgba(59,130,246,.1) 0%,transparent 65%);
  pointer-events:none;
}
.img-wrap { position:relative; flex-shrink:0; animation:floatAvatar 4s ease-in-out infinite; }
.img-wrap img { width:240px; border-radius:18px; display:block; animation:pulseGlow 3s ease-in-out infinite; }
.num-tag {
  position:absolute; top:10px; right:10px;
  background:linear-gradient(135deg,#3b82f6,#1d4ed8);
  color:#fff; font-weight:900; font-size:1.3rem; width:48px; height:48px;
  border-radius:50%; display:flex; align-items:center; justify-content:center;
  box-shadow:0 4px 18px rgba(59,130,246,.6); font-family:'Roboto Mono',monospace;
}
.info { flex:1; }
.av-name {
  font-size:1.9rem; font-weight:900;
  background:linear-gradient(135deg,#fff 0%,#93c5fd 50%,#3b82f6 100%);
  background-size:200% auto; -webkit-background-clip:text;
  -webkit-text-fill-color:transparent; background-clip:text;
  animation:shimmer 4s linear infinite; margin-bottom:.2rem;
}
.av-pos { color:#7dd3fc; font-size:.9rem; font-weight:600; letter-spacing:.1em; text-transform:uppercase; margin-bottom:1rem; }
.stat-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:.7rem; margin-bottom:1.2rem; }
.stat-card { background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.08); border-radius:12px; padding:.7rem .9rem; }
.stat-lbl { font-size:.6rem; font-weight:700; color:#475569; text-transform:uppercase; letter-spacing:.08em; }
.stat-val { font-size:1.15rem; font-weight:900; color:#60a5fa; font-family:'Roboto Mono',monospace; margin-top:2px; }
.quote { font-family:'Cairo',sans-serif; font-size:1.2rem; font-weight:900; color:#fbbf24; text-shadow:0 0 20px rgba(251,191,36,.4); }
.pt { position:absolute; width:4px; height:4px; border-radius:50%; animation:drift linear infinite; }
@media (max-width: 640px) {
  body { overflow: visible; }
  .showcase {
    flex-direction: column;
    text-align: center;
    gap: 1.2rem;
    padding: 1.4rem 1rem;
    height: auto;
  }
  .img-wrap img { width: 135px; }
  .av-name { font-size: 1.45rem; }
  .av-pos { font-size: 0.8rem; margin-bottom: 0.8rem; }
  .stat-grid { gap: 0.5rem; margin-bottom: 0.8rem; }
  .stat-card { padding: 0.5rem 0.6rem; }
  .stat-lbl { font-size: 0.55rem; }
  .stat-val { font-size: 1rem; }
  .quote { font-size: 1.1rem; }
  .num-tag { width: 38px; height: 38px; font-size: 1rem; top: 6px; right: 6px; }
}
</style></head>
<body style="background:linear-gradient(135deg,#0a1628,#0d1f3c);">
<div class="showcase">
  <div class="pt" style="left:8%;bottom:15%;animation-duration:3.5s;background:#3b82f6;"></div>
  <div class="pt" style="left:18%;bottom:8%;animation-duration:4.2s;animation-delay:.9s;background:#38bdf8;"></div>
  <div class="pt" style="left:80%;bottom:12%;animation-duration:3.9s;animation-delay:1.5s;background:#a78bfa;"></div>
  <div class="pt" style="left:90%;bottom:20%;animation-duration:5s;animation-delay:.4s;background:#fbbf24;"></div>
  <div class="img-wrap">
    <img src="data:__MIME__;base64,__B64__" alt="Renad Soliman"/>
    <div class="num-tag">#23</div>
  </div>
  <div class="info">
    <div class="av-name">Renad Soliman</div>
    <div class="av-pos">&#x1F3C0; Point Guard &nbsp;&middot;&nbsp; Misr Petroleum</div>
    <div class="stat-grid">
      <div class="stat-card"><div class="stat-lbl">&#x1F3AF; Specialty</div><div class="stat-val" style="font-size:.88rem;color:#fbbf24;">3-Point Queen</div></div>
      <div class="stat-card"><div class="stat-lbl">&#x1F3C6; Competition</div><div class="stat-val" style="font-size:.88rem;color:#34d399;">FIBA Africa</div></div>
      <div class="stat-card"><div class="stat-lbl">&#x1F4CD; Clubs</div><div class="stat-val">7</div></div>
      <div class="stat-card"><div class="stat-lbl">&#x1F382; Age</div><div class="stat-val">22</div></div>
    </div>
    <div class="quote">« بطلة الثلاثيات »</div>
  </div>
</div>
</body></html>"""
                .replace("__MIME__", mime)
                .replace("__B64__", avatar_b64)
            )
            components.html(avatar_html, height=490, scrolling=False)
        else:
            st.info("Add avatar.png to the project folder to display the player avatar.", icon="🖼️")

        # -- Club Journey --
        st.markdown("<div class='section-header'>🏆 Club Journey</div>",
                    unsafe_allow_html=True)

        journey_path = "club_journey.jpg"
        if os.path.exists(journey_path):
            st.image(journey_path, use_container_width=True,
                     caption="Renad's Club Journey — 7 clubs, same passion")
        else:
            clubs = [
                {"num":"1","tag":"tag-youth",    "label":"YOUTH START",  "name":"Ghaba",          "years":"Youth"},
                {"num":"2","tag":"tag-previous", "label":"CLUB 2",       "name":"Al Ahly",        "years":""},
                {"num":"3","tag":"tag-previous", "label":"CLUB 3",       "name":"Zohour",         "years":""},
                {"num":"4","tag":"tag-previous", "label":"CLUB 4",       "name":"Tawfkia",        "years":""},
                {"num":"5","tag":"tag-first",    "label":"FIRST STINT",  "name":"Misr Petroleum", "years":""},
                {"num":"6","tag":"tag-previous", "label":"CLUB 6",       "name":"Tyran SC",       "years":""},
                {"num":"7","tag":"tag-current",  "label":"CURRENT CLUB", "name":"Misr Petroleum", "years":"Present"},
            ]

            def render_club_card(club):
                logo_path = f"logos/{club['name'].lower().replace(' ','_')}.png"
                img_tag = ""
                if os.path.exists(logo_path):
                    with open(logo_path, "rb") as f:
                        b64 = base64.b64encode(f.read()).decode()
                    img_tag = f'<img src="data:image/png;base64,{b64}" style="width:58px;height:58px;object-fit:contain;margin:0.5rem auto;display:block;filter:drop-shadow(0 4px 10px rgba(0,0,0,0.5));"/>'
                else:
                    lbl = "👑" if club["tag"] == "tag-current" else "🛡️"
                    img_tag = f'<div style="font-size:2.2rem;margin:0.5rem 0;">{lbl}</div>'

                hi = "border-color:rgba(59,130,246,0.55);box-shadow:0 0 20px rgba(59,130,246,0.18);" if club["tag"] == "tag-current" else ""
                years_text = club["years"] if club["years"] else "&nbsp;"
                return f"""
                <div class='timeline-card' style='{hi}'>
                  <div class='club-num'>CLUB #{club["num"]}</div>
                  <span class='club-tag {club["tag"]}'>{club["label"]}</span>
                  {img_tag}
                  <p class='club-name'>{club["name"]}</p>
                  <p class='club-years'>{years_text}</p>
                </div>
                """

            row1 = st.columns(4, gap="small")
            for col, club in zip(row1, clubs[:4]):
                with col:
                    st.markdown(render_club_card(club), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            _, c5, c6, c7, _ = st.columns([0.5, 1, 1, 1, 0.5], gap="small")
            for col, club in zip([c5, c6, c7], clubs[4:]):
                with col:
                    st.markdown(render_club_card(club), unsafe_allow_html=True)

        # -- Season Averages --
        st.markdown("<div class='section-header'>📈 Season Averages</div>",
                    unsafe_allow_html=True)

        if not db_ok:
            st.markdown("""
            <div class='db-warning'>
              ⚠️ Database not connected — check your Neon connection string in
              <code>.streamlit/secrets.toml</code>.
            </div>
            """, unsafe_allow_html=True)
        elif df_all.empty:
            st.info("No match data yet. Log your first game in the Match Tracker tab!", icon="📋")
        else:
            m1, m2, m3, m4, m5 = st.columns(5)
            m1.metric("🏀 PPG", avgs["ppg"], help="Points per game")
            m2.metric("🎯 APG", avgs["apg"], help="Assists per game")
            m3.metric("💪 RPG", avgs["rpg"], help="Rebounds per game")
            m4.metric("⚡ SPG", avgs["spg"], help="Steals per game")
            m5.metric("⏱️ MPG", avgs["mpg"], help="Minutes per game")
            st.markdown("<br>", unsafe_allow_html=True)
            chart_df = (
                df_all.sort_values("match_date").tail(10)
                [["match_date", "total_points"]]
                .rename(columns={"match_date": "Date", "total_points": "Points"})
                .set_index("Date")
            )
            st.markdown("<p style='color:#64748b;font-size:0.8rem;margin-bottom:4px;'>Last 10 games — scoring trend</p>",
                        unsafe_allow_html=True)
            st.line_chart(chart_df, color="#3b82f6", height=180)

    # ══════════════════════════════════════════
    #  TAB 2 - MATCH TRACKER
    # ══════════════════════════════════════════
    with tab2:
        if not check_tracker_access():
            return

        if not db_ok:
            st.error(
                "⚠️ **Database not configured.** Open `.streamlit/secrets.toml` and "
                "replace the placeholder URL with your real Neon connection string.",
                icon="🔌"
            )
            return

        st.markdown("<div class='section-header'>➕ Log a New Match</div>",
                    unsafe_allow_html=True)

        with st.form("match_form", clear_on_submit=True):
            r1c1, r1c2 = st.columns(2)
            match_date = r1c1.date_input("📅 Match Date", value=date.today())
            opponent   = r1c2.text_input("🆚 Opponent", placeholder="e.g. Ahly")

            r2c1, r2c2, r2c3 = st.columns(3)
            minutes  = r2c1.number_input("⏱️ Minutes",         min_value=0.0, max_value=60.0, step=0.5, value=0.0)
            fg2_made = r2c2.number_input("🎯 2-Pointers Made", min_value=0,   max_value=30,   step=1,   value=0)
            fg3_made = r2c3.number_input("🏹 3-Pointers Made", min_value=0,   max_value=15,   step=1,   value=0)

            r3c1, r3c2, r3c3 = st.columns(3)
            assists  = r3c1.number_input("🤝 Assists",  min_value=0, max_value=30, step=1, value=0)
            rebounds = r3c2.number_input("💪 Rebounds", min_value=0, max_value=30, step=1, value=0)
            steals   = r3c3.number_input("⚡ Steals",   min_value=0, max_value=15, step=1, value=0)

            total_points = int(fg2_made) * 2 + int(fg3_made) * 3

            st.markdown(f"""
            <div style='margin:1rem 0 .5rem 0;padding:1rem 1.4rem;
              background:linear-gradient(135deg,rgba(59,130,246,.15),rgba(29,78,216,.08));
              border:1px solid rgba(59,130,246,.3);border-radius:12px;
              display:flex;align-items:center;gap:16px;'>
              <span style='font-size:1.8rem;'>🏀</span>
              <div>
                <div style='color:#94a3b8;font-size:.72rem;font-weight:600;text-transform:uppercase;letter-spacing:.07em;'>
                  Total Points (auto-calculated)
                </div>
                <div style='color:#60a5fa;font-size:2rem;font-weight:900;font-family:"Roboto Mono",monospace;line-height:1.1;'>
                  {total_points}
                </div>
                <div style='color:#475569;font-size:.75rem;'>
                  {int(fg2_made)} x 2pt + {int(fg3_made)} x 3pt =
                  <strong style='color:#93c5fd;'>{total_points} pts</strong>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            submitted = st.form_submit_button("💾  Save Match", use_container_width=True, type="primary")

        if submitted:
            if not opponent.strip():
                st.warning("Please enter the opponent's name.", icon="⚠️")
            else:
                ok = insert_match(engine, {
                    "match_date":   match_date,
                    "opponent":     opponent.strip(),
                    "minutes":      float(minutes),
                    "fg2_made":     int(fg2_made),
                    "fg3_made":     int(fg3_made),
                    "total_points": total_points,
                    "assists":      int(assists),
                    "rebounds":     int(rebounds),
                    "steals":       int(steals),
                })
                if ok:
                    st.success(f"✅ Match vs **{opponent}** saved — **{total_points} pts**!", icon="🏀")
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error("Failed to save — check your database connection.")

        # -- Match History --
        st.markdown("<div class='section-header'>📋 Match History</div>",
                    unsafe_allow_html=True)
        df_display = load_stats(engine)

        if df_display.empty:
            st.info("No matches logged yet. Fill in the form above to get started!", icon="📋")
        else:
            cols_map = {
                "match_date": "Date",   "opponent": "Opponent", "minutes": "MIN",
                "fg2_made":   "2PM",    "fg3_made": "3PM",      "total_points": "PTS",
                "assists":    "AST",    "rebounds": "REB",      "steals": "STL",
            }
            df_show = (
                df_display[list(cols_map.keys())]
                .rename(columns=cols_map)
                .sort_values("Date", ascending=False)
            )
            st.dataframe(df_show, use_container_width=True, hide_index=True,
                column_config={
                    "Date": st.column_config.DateColumn("📅 Date", format="MMM DD, YYYY"),
                    "PTS":  st.column_config.NumberColumn("🏀 PTS", format="%d"),
                    "MIN":  st.column_config.NumberColumn("⏱️ MIN", format="%.1f"),
                    "2PM":  st.column_config.NumberColumn("🎯 2PM"),
                    "3PM":  st.column_config.NumberColumn("🏹 3PM"),
                    "AST":  st.column_config.NumberColumn("🤝 AST"),
                    "REB":  st.column_config.NumberColumn("💪 REB"),
                    "STL":  st.column_config.NumberColumn("⚡ STL"),
                })

            st.markdown("<div class='section-header'>📈 Scoring Trend</div>",
                        unsafe_allow_html=True)
            chart_df = (
                df_display[["match_date", "total_points", "assists", "rebounds"]]
                .sort_values("match_date")
                .rename(columns={"match_date":"Date","total_points":"Points",
                                  "assists":"Assists","rebounds":"Rebounds"})
                .set_index("Date")
            )
            st.line_chart(chart_df, height=280)

            st.markdown("<div class='section-header'>🏅 Season Summary</div>",
                        unsafe_allow_html=True)
            al = season_averages(df_display)
            sm1, sm2, sm3, sm4, sm5, sm6 = st.columns(6)
            sm1.metric("Games", al["games"])
            sm2.metric("PPG",   al["ppg"])
            sm3.metric("APG",   al["apg"])
            sm4.metric("RPG",   al["rpg"])
            sm5.metric("SPG",   al["spg"])
            sm6.metric("MPG",   al["mpg"])

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔒  Lock Tracker", key="lock_btn"):
                st.session_state["tracker_unlocked"] = False
                st.rerun()


if __name__ == "__main__":
    main()
