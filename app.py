import streamlit as st
from datetime import date
import pandas as pd
from modules.data_manager import save_entry, get_last_n_days, get_all_data
import plotly.graph_objects as go
import plotly.express as px

# --- Page Config ---
st.set_page_config(
    page_title="ADHD Habit Tracker",
    page_icon="🧠",
    layout="wide"
)

# --- Custom CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Space+Mono:wght@400;700&display=swap');

/* ── Root & Background ── */
:root {
    --pink:    #FF6B9D;
    --purple:  #A855F7;
    --cyan:    #22D3EE;
    --yellow:  #FFD60A;
    --green:   #4ADE80;
    --orange:  #FB923C;
    --bg:      #0D0D1A;
    --surface: #161628;
    --card:    #1E1E38;
    --border:  rgba(255,255,255,0.08);
    --text:    #F0EEFF;
    --muted:   #8B87B0;
}

            
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    font-family: 'Nunito', sans-serif !important;
    color: var(--text) !important;
}

[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at 10% 0%,   rgba(168,85,247,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 90% 100%, rgba(255,107,157,0.15) 0%, transparent 60%),
        radial-gradient(ellipse 50% 40% at 50% 50%,  rgba(34,211,238,0.07) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #130F2A 0%, #0D0D1A 100%) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

.sidebar-logo {
    text-align: center;
    padding: 1.5rem 0 1rem;
    font-size: 3rem;
    animation: pulse-glow 3s ease-in-out infinite;
}
@keyframes pulse-glow {
    0%,100% { filter: drop-shadow(0 0 8px rgba(168,85,247,0.6)); }
    50%      { filter: drop-shadow(0 0 20px rgba(255,107,157,0.8)); }
}

.sidebar-title {
    text-align: center;
    font-size: 1.2rem;
    font-weight: 900;
    background: linear-gradient(135deg, var(--pink), var(--purple), var(--cyan));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
    letter-spacing: -0.5px;
}
.sidebar-sub {
    text-align: center;
    font-size: 0.7rem;
    color: var(--muted) !important;
    margin-bottom: 1.5rem;
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* Nav pills */
[data-testid="stSidebar"] .stRadio label {
    display: flex !important;
    align-items: center !important;
    padding: 0.65rem 1rem !important;
    margin: 0.25rem 0.5rem !important;
    border-radius: 12px !important;
    border: 1px solid transparent !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(168,85,247,0.15) !important;
    border-color: rgba(168,85,247,0.3) !important;
}
[data-testid="stSidebar"] .stRadio [data-checked="true"] label,
[data-testid="stSidebar"] .stRadio label:has(input:checked) {
    background: linear-gradient(135deg, rgba(168,85,247,0.25), rgba(255,107,157,0.15)) !important;
    border-color: rgba(168,85,247,0.5) !important;
}
[data-testid="stSidebar"] .stRadio input { display: none !important; }

/* ── Page Header ── */
.page-header {
    margin-bottom: 2rem;
    position: relative;
}
.page-header h1 {
    font-size: 2.4rem !important;
    font-weight: 900 !important;
    line-height: 1.1 !important;
    background: linear-gradient(135deg, #fff 0%, var(--purple) 60%, var(--pink) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 !important;
}
.page-header p {
    color: var(--muted);
    font-size: 0.95rem;
    margin-top: 0.4rem;
}

/* ── Cards ── */
.glass-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.glass-card::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 20px;
    background: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, transparent 60%);
    pointer-events: none;
}
.glass-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(168,85,247,0.15);
}

.card-label {
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    color: var(--muted);
}
.card-value {
    font-size: 2.2rem;
    font-weight: 900;
    font-family: 'Space Mono', monospace;
    line-height: 1;
}
.card-sub {
    font-size: 0.8rem;
    color: var(--muted);
    margin-top: 0.3rem;
}

/* Section titles */
.section-title {
    font-size: 1rem;
    font-weight: 800;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--muted);
    margin: 1.5rem 0 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── Sliders & Inputs ── */
.stSlider > div > div > div > div { background: var(--purple) !important; }
.stSlider [data-baseweb="slider"] > div:first-child {
    background: rgba(168,85,247,0.2) !important;
    border-radius: 99px !important;
}
.stSelectbox > div > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
}
.stDateInput > div > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}

/* Slider labels */
.stSlider label, .stSelectbox label, .stDateInput label {
    color: var(--text) !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
}

/* ── Buttons ── */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, var(--purple), var(--pink)) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.85rem 2rem !important;
    font-weight: 800 !important;
    font-size: 1rem !important;
    font-family: 'Nunito', sans-serif !important;
    letter-spacing: 0.5px !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(168,85,247,0.4) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(168,85,247,0.6) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Dataframe ── */
.stDataFrame { border-radius: 16px !important; overflow: hidden !important; }
iframe[title="st_dataframe"] { border-radius: 16px !important; }

/* ── Alerts ── */
.stSuccess { background: rgba(74,222,128,0.12) !important; border-color: var(--green) !important; border-radius: 12px !important; }
.stWarning { background: rgba(251,146,60,0.12) !important; border-color: var(--orange) !important; border-radius: 12px !important; }
.stInfo    { background: rgba(34,211,238,0.10) !important; border-color: var(--cyan) !important; border-radius: 12px !important; }

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }

/* ── Mood badge ── */
.mood-row { display: flex; gap: 0.5rem; flex-wrap: wrap; margin: 0.5rem 0; }
.mood-badge {
    padding: 0.3rem 0.8rem;
    border-radius: 99px;
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.5px;
}

/* ── Streak widget ── */
.streak-box {
    background: linear-gradient(135deg, rgba(255,214,10,0.15), rgba(251,146,60,0.1));
    border: 1px solid rgba(255,214,10,0.3);
    border-radius: 16px;
    padding: 1rem 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
}

/* ── Tip box ── */
.tip-box {
    background: linear-gradient(135deg, rgba(34,211,238,0.1), rgba(168,85,247,0.08));
    border: 1px solid rgba(34,211,238,0.25);
    border-radius: 16px;
    padding: 1rem 1.2rem;
    font-size: 0.88rem;
    color: var(--cyan);
    margin-top: 1rem;
}

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden !important; }
.block-container { padding-top: 2rem !important; padding-bottom: 2rem !important; max-width: 1100px !important; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🧠</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">ADHD Tracker</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Your focus companion</div>', unsafe_allow_html=True)

    page = st.radio("", [
        "📝  Log Habits",
        "📊  Dashboard",
        "🔍  Pattern Insights"
    ], label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='padding:1rem;background:rgba(255,255,255,0.04);border-radius:14px;border:1px solid rgba(255,255,255,0.07);font-size:0.78rem;color:#8B87B0;line-height:1.6'>
        💡 <b style='color:#F0EEFF'>Quick Tips</b><br>
        Log every day for best insights.<br>
        Even 1 minute counts!
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# PAGE 1 — LOG HABITS
# ─────────────────────────────────────────
if "Log" in page:
    st.markdown("""
    <div class='page-header'>
        <h1>Log Today's Habits ✍️</h1>
        <p>Small consistent steps unlock big pattern insights.</p>
    </div>
    """, unsafe_allow_html=True)

    # Streak info
    recent = get_last_n_days(30)
    streak = len(recent) if not recent.empty else 0
    st.markdown(f"""
    <div class='streak-box'>
        <span style='font-size:2rem'>🔥</span>
        <div>
            <div style='font-size:1.4rem;font-weight:900;color:#FFD60A;font-family:Space Mono'>{streak} day streak</div>
            <div style='font-size:0.78rem;color:#8B87B0'>Keep it up — consistency is your superpower!</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("<div class='section-title'>⏰ Time & Body</div>", unsafe_allow_html=True)
        with st.container():
            log_date = st.date_input("📅 Date", value=date.today())
            sleep = st.slider("😴 Sleep Hours", 0.0, 12.0, 7.0, 0.5,
                              help="How many hours did you sleep last night?")
            exercise = st.selectbox("🏃 Exercise Today?", ["Yes", "No"],
                                    help="Even a short walk counts!")
            study = st.slider("📚 Study / Focus Hours", 0.0, 12.0, 3.0, 0.5,
                              help="Deep work, studying, or focused tasks")

    with col2:
        st.markdown("<div class='section-title'>😊 Mind & Screen</div>", unsafe_allow_html=True)
        with st.container():
            phone = st.slider("📱 Phone / Screen Usage (hrs)", 0.0, 12.0, 2.0, 0.5,
                              help="Total recreational screen time")
            mood = st.selectbox("🌈 Mood", [
                "😊 Happy", "😐 Neutral", "😰 Anxious",
                "😔 Sad", "⚡ Energetic", "😴 Tired"
            ])
            productivity = st.slider("⚡ Productivity Score", 1, 10, 5,
                                     help="Rate how productive you felt today (1=low, 10=high)")

    st.markdown("<br>", unsafe_allow_html=True)

    # Visual score indicator
    score_color = "#4ADE80" if productivity >= 7 else "#FFD60A" if productivity >= 4 else "#FF6B9D"
    score_label = "Great day! 🎉" if productivity >= 7 else "Decent day 👍" if productivity >= 4 else "Tough day 💙"
    st.markdown(f"""
    <div class='glass-card' style='border-color:rgba(255,255,255,0.1);text-align:center;padding:1.2rem'>
        <span style='font-size:0.75rem;font-weight:800;letter-spacing:2px;text-transform:uppercase;color:#8B87B0'>Productivity Preview</span>
        <div style='font-size:3rem;font-weight:900;font-family:Space Mono;color:{score_color};margin:0.3rem 0'>{productivity}<span style='font-size:1.2rem;color:#8B87B0'>/10</span></div>
        <div style='font-size:0.9rem;color:{score_color}'>{score_label}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("💾  Save Today's Entry", width='stretch'):
        mood_clean = mood.split(" ", 1)[1] if " " in mood else mood
        success, message = save_entry(
            log_date, sleep, exercise,
            study, phone, mood_clean, productivity
        )
        if success:
            st.cache_data.clear()  
            st.success(message)
            st.balloons()
        else:
            st.warning(message)

    st.markdown("<div class='section-title'>📋 Recent Entries</div>", unsafe_allow_html=True)
    recent = get_last_n_days(7)
    if recent.empty:
        st.markdown("""
        <div class='tip-box'>
            🌱 No entries yet! Log your first habit above to start discovering your patterns.
        </div>
        """, unsafe_allow_html=True)
    else:
        recent["Date"] = pd.to_datetime(recent["Date"]).dt.date
        st.dataframe(recent, width='stretch', hide_index=True)


elif "Dashboard" in page:
    st.markdown("""
    <div class='page-header'>
        <h1>Your Dashboard 📊</h1>
        <p>Visual breakdown of your habits and productivity trends.</p>
    </div>
    """, unsafe_allow_html=True)

    df = get_all_data()

    if df.empty or len(df) < 2:
        st.markdown("""
        <div class='tip-box'>
            📊 You need at least 2 entries to see your dashboard. Keep logging!
        </div>
        """, unsafe_allow_html=True)
    else:
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date")

        # ── Top Stat Cards ──
        st.markdown("<div class='section-title'>📈 Your Averages</div>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)

        avg_sleep  = round(df["Sleep Hours"].mean(), 1)
        avg_study  = round(df["Study Hours"].mean(), 1)
        avg_phone  = round(df["Phone Usage"].mean(), 1)
        avg_prod   = round(df["Productivity Score"].mean(), 1)

        sleep_color = "#4ADE80" if avg_sleep >= 7 else "#FFD60A" if avg_sleep >= 6 else "#FF6B9D"
        study_color = "#4ADE80" if avg_study >= 4 else "#FFD60A" if avg_study >= 2 else "#FF6B9D"
        phone_color = "#4ADE80" if avg_phone <= 3 else "#FFD60A" if avg_phone <= 5 else "#FF6B9D"
        prod_color  = "#4ADE80" if avg_prod  >= 7 else "#FFD60A" if avg_prod  >= 4 else "#FF6B9D"

        with c1:
            st.markdown(f"""
            <div class='glass-card' style='text-align:center'>
                <div class='card-label'>😴 Avg Sleep</div>
                <div class='card-value' style='color:{sleep_color}'>{avg_sleep}</div>
                <div class='card-sub'>hours / night</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class='glass-card' style='text-align:center'>
                <div class='card-label'>📚 Avg Study</div>
                <div class='card-value' style='color:{study_color}'>{avg_study}</div>
                <div class='card-sub'>hours / day</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class='glass-card' style='text-align:center'>
                <div class='card-label'>📱 Avg Screen</div>
                <div class='card-value' style='color:{phone_color}'>{avg_phone}</div>
                <div class='card-sub'>hours / day</div>
            </div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""
            <div class='glass-card' style='text-align:center'>
                <div class='card-label'>⚡ Avg Productivity</div>
                <div class='card-value' style='color:{prod_color}'>{avg_prod}</div>
                <div class='card-sub'>out of 10</div>
            </div>""", unsafe_allow_html=True)

        # ── Charts ──
        

        PLOT_THEME = dict(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Nunito", color="#8B87B0"),
            xaxis=dict(showgrid=False, color="#8B87B0"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)", color="#8B87B0"),
            margin=dict(l=10, r=10, t=40, b=10)
        )

        st.markdown("<div class='section-title'>📉 Trends Over Time</div>", unsafe_allow_html=True)
        col_a, col_b = st.columns(2, gap="large")

        with col_a:
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(
                x=df["Date"], y=df["Productivity Score"],
                mode="lines+markers",
                line=dict(color="#A855F7", width=3),
                marker=dict(size=8, color="#FF6B9D",
                            line=dict(color="#A855F7", width=2)),
                fill="tozeroy",
                fillcolor="rgba(168,85,247,0.1)",
                name="Productivity"
            ))
            fig1.update_layout(title="⚡ Productivity Score", **PLOT_THEME)
            st.plotly_chart(fig1, width='stretch')

        with col_b:
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=df["Date"], y=df["Sleep Hours"],
                mode="lines+markers",
                line=dict(color="#22D3EE", width=3),
                marker=dict(size=8, color="#22D3EE"),
                fill="tozeroy",
                fillcolor="rgba(34,211,238,0.1)",
                name="Sleep"
            ))
            fig2.update_layout(title="😴 Sleep Hours", **PLOT_THEME)
            st.plotly_chart(fig2, width='stretch')

        col_c, col_d = st.columns(2, gap="large")

        with col_c:
            fig3 = go.Figure()
            fig3.add_trace(go.Bar(
                x=df["Date"], y=df["Study Hours"],
                marker=dict(
                    color=df["Study Hours"],
                    colorscale=[[0,"#1E1E38"],[1,"#4ADE80"]],
                    showscale=False
                ),
                name="Study Hours"
            ))
            fig3.update_layout(title="📚 Study Hours", **PLOT_THEME)
            st.plotly_chart(fig3, width='stretch')

        with col_d:
            fig4 = go.Figure()
            fig4.add_trace(go.Bar(
                x=df["Date"], y=df["Phone Usage"],
                marker=dict(
                    color=df["Phone Usage"],
                    colorscale=[[0,"#1E1E38"],[1,"#FF6B9D"]],
                    showscale=False
                ),
                name="Phone Usage"
            ))
            fig4.update_layout(title="📱 Phone Usage", **PLOT_THEME)
            st.plotly_chart(fig4, width='stretch')

        # ── Mood Distribution ──
        st.markdown("<div class='section-title'>🌈 Mood Distribution</div>", unsafe_allow_html=True)
        mood_counts = df["Mood"].value_counts().reset_index()
        mood_counts.columns = ["Mood", "Count"]
        mood_colors = ["#FF6B9D","#A855F7","#22D3EE","#4ADE80","#FFD60A","#FB923C"]
        fig5 = px.pie(mood_counts, names="Mood", values="Count",
                      color_discrete_sequence=mood_colors, hole=0.5)
        fig5.update_layout(**PLOT_THEME)
        fig5.update_traces(textfont=dict(family="Nunito", color="white"))
        st.plotly_chart(fig5, width='stretch')

        # ── Exercise Impact ──
        st.markdown("<div class='section-title'>🏃 Exercise vs Productivity</div>", unsafe_allow_html=True)
        ex_group = df.groupby("Exercise")["Productivity Score"].mean().reset_index()
        fig6 = px.bar(ex_group, x="Exercise", y="Productivity Score",
                      color="Exercise",
                      color_discrete_map={"Yes":"#4ADE80","No":"#FF6B9D"})
        fig6.update_layout(showlegend=False, **PLOT_THEME)
        st.plotly_chart(fig6, width='stretch')

elif "Pattern" in page:
    from modules.pattern_detection import (
        get_correlations, get_clusters,
        predict_productive_day, get_best_worst_days
    )
    from modules.insights import generate_insights

    st.markdown("""
    <div class='page-header'>
        <h1>Pattern Insights 🔍</h1>
        <p>AI-powered analysis of your habit patterns.</p>
    </div>
    """, unsafe_allow_html=True)

    df = get_all_data()

    if df.empty or len(df) < 3:
        st.markdown("""
        <div class='tip-box'>
            🧠 You need at least 3 entries for pattern detection.
            Keep logging your habits daily!
        </div>
        """, unsafe_allow_html=True)
    else:

        PLOT_THEME = dict(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Nunito", color="#8B87B0"),
            xaxis=dict(showgrid=False, color="#8B87B0"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)", color="#8B87B0"),
            margin=dict(l=10, r=10, t=40, b=10)
        )

        # ── Correlations ──
        st.markdown("<div class='section-title'>🔗 Habit Correlations</div>",
                    unsafe_allow_html=True)
        correlations = get_correlations(df)

        for habit, corr in correlations.items():
            name = habit.replace("_encoded","").replace("_"," ")
            color = "#4ADE80" if corr > 0 else "#FF6B9D"
            bar_width = abs(corr) * 100
            st.markdown(f"""
            <div class='glass-card' style='padding:1rem 1.5rem;margin-bottom:0.6rem'>
                <div style='display:flex;justify-content:space-between;margin-bottom:0.4rem'>
                    <span style='font-weight:700;font-size:0.9rem'>{name}</span>
                    <span style='font-family:Space Mono;color:{color};font-weight:700'>{corr:+.2f}</span>
                </div>
                <div style='background:rgba(255,255,255,0.06);border-radius:99px;height:8px;overflow:hidden'>
                    <div style='width:{bar_width}%;background:{color};height:100%;
                    border-radius:99px;transition:width 0.5s ease'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ── Feature Importance ──
        st.markdown("<div class='section-title'>🌳 Productivity Predictors</div>",
                    unsafe_allow_html=True)
        clf, importances = predict_productive_day(df)

        if importances:
            fig = go.Figure(go.Bar(
                x=list(importances.values()),
                y=[k.replace("_encoded","").replace("_"," ")
                   for k in importances.keys()],
                orientation='h',
                marker=dict(
                    color=list(importances.values()),
                    colorscale=[[0,"#1E1E38"],[0.5,"#A855F7"],[1,"#FF6B9D"]],
                    showscale=False
                )
            ))
            fig.update_layout(title="What predicts your productive days?", **PLOT_THEME)
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("Need more varied data to predict productive days.")

        # ── Best vs Worst Day ──
        st.markdown("<div class='section-title'>🏆 Best vs Worst Day</div>",
                    unsafe_allow_html=True)
        best, worst = get_best_worst_days(df)
        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.markdown(f"""
            <div class='glass-card' style='border-color:rgba(74,222,128,0.3)'>
                <div style='color:#4ADE80;font-weight:800;margin-bottom:0.8rem'>
                    🏆 Best Day — {str(best["Date"]).split()[0]}
                </div>
                <div style='display:grid;gap:0.4rem;font-size:0.88rem'>
                    <div>😴 Sleep: <b>{best["Sleep Hours"]} hrs</b></div>
                    <div>🏃 Exercise: <b>{best["Exercise"]}</b></div>
                    <div>📚 Study: <b>{best["Study Hours"]} hrs</b></div>
                    <div>📱 Phone: <b>{best["Phone Usage"]} hrs</b></div>
                    <div>😊 Mood: <b>{best["Mood"]}</b></div>
                    <div>⚡ Score: <b style='color:#4ADE80'>{best["Productivity Score"]}/10</b></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class='glass-card' style='border-color:rgba(255,107,157,0.3)'>
                <div style='color:#FF6B9D;font-weight:800;margin-bottom:0.8rem'>
                    📉 Worst Day — {str(worst["Date"]).split()[0]}
                </div>
                <div style='display:grid;gap:0.4rem;font-size:0.88rem'>
                    <div>😴 Sleep: <b>{worst["Sleep Hours"]} hrs</b></div>
                    <div>🏃 Exercise: <b>{worst["Exercise"]}</b></div>
                    <div>📚 Study: <b>{worst["Study Hours"]} hrs</b></div>
                    <div>📱 Phone: <b>{worst["Phone Usage"]} hrs</b></div>
                    <div>😊 Mood: <b>{worst["Mood"]}</b></div>
                    <div>⚡ Score: <b style='color:#FF6B9D'>{worst["Productivity Score"]}/10</b></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ── AI Insights ──
        st.markdown("<div class='section-title'>🧠 AI Insights</div>",
                    unsafe_allow_html=True)
        insights = generate_insights(correlations, importances, df)

        color_map = {
            "positive":  ("rgba(74,222,128,0.1)",  "rgba(74,222,128,0.3)"),
            "negative":  ("rgba(255,107,157,0.1)", "rgba(255,107,157,0.3)"),
            "neutral":   ("rgba(34,211,238,0.1)",  "rgba(34,211,238,0.3)"),
            "highlight": ("rgba(168,85,247,0.1)",  "rgba(168,85,247,0.3)"),
        }

        for ins in insights:
            bg, border = color_map.get(ins["type"], color_map["neutral"])
            st.markdown(f"""
            <div style='background:{bg};border:1px solid {border};border-radius:14px;
            padding:1rem 1.2rem;margin-bottom:0.6rem;font-size:0.92rem;font-weight:600'>
                {ins["icon"]} {ins["text"]}
            </div>
            """, unsafe_allow_html=True)