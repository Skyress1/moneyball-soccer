import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings

warnings.filterwarnings('ignore')

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Moneyball Pro Analytics",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# CUSTOM CSS & THEME
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    /* Import Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    /* General Settings */
    * { 
        font-family: 'Outfit', sans-serif; 
        color: #e2e8f0; /* Light gray text for everything by default */
    }
    
    .stApp {
        background-color: #0f172a; /* Darker slate blue background */
    }
    
    /* Force white text for all headers and labels */
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {
        color: #f8fafc !important;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 10px; }
    ::-webkit-scrollbar-track { background: #0f172a; }
    ::-webkit-scrollbar-thumb { background: #3b82f6; border-radius: 5px; }

    /* Cards & Containers */
    .glass-card {
        background: rgba(30, 41, 59, 0.7); /* Slightly more opaque for better contrast */
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }

    /* Metric Values */
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(45deg, #60a5fa, #a78bfa); /* Lighter gradients */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 2px 10px rgba(96, 165, 250, 0.3);
    }
    .metric-label {
        color: #cbd5e1 !important; /* Lighter gray for labels */
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }

    /* Streamlit Widget Fixes - Input Box */
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #1e293b !important;
        color: #f8fafc !important;
        border-color: #475569 !important;
    }
    
    /* FIX: Aggressive Dropdown Menu Styling */
    /* Target the popover container */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    div[data-baseweb="menu"],
    div[role="listbox"] {
        background-color: #0f172a !important; /* Very dark blue */
        border: 1px solid #334155 !important;
    }

    /* Target the options list */
    ul[data-baseweb="menu"] {
        background-color: #0f172a !important;
    }

    /* Target individual options */
    li[data-baseweb="option"],
    li[role="option"],
    div[role="option"] {
        background-color: #0f172a !important;
        color: #f8fafc !important; /* Bright white text */
    }

    /* Target Hover & Selected States */
    li[data-baseweb="option"]:hover,
    li[role="option"]:hover,
    div[role="option"]:hover,
    li[aria-selected="true"],
    div[aria-selected="true"] {
        background-color: #3b82f6 !important; /* Bright Blue */
        color: white !important;
    }
    
    /* Fix for virtualized lists (if used) */
    .virtualized-list {
        background-color: #0f172a !important;
    }
    
    /* Dataframe Fixes */
    [data-testid="stDataFrame"] {
        background-color: #1e293b;
        border-radius: 10px;
        padding: 10px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1e293b;
        border-radius: 8px;
        color: #94a3b8;
        padding: 10px 20px;
        border: 1px solid #334155;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #fff;
        background-color: #334155;
        border-color: #475569;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #2563eb, #7c3aed) !important;
        color: white !important;
        border: none;
        font-weight: bold;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #020617;
        border-right: 1px solid #1e293b;
    }
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] label {
        color: #f1f5f9 !important;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATA LOADING & PROCESSING
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('players_real_data.csv')
        df = df.loc[:, ~df.columns.duplicated()]
        
        # Mapping
        column_mapping = {
            'player': 'Player', 'team': 'Squad', 'league': 'Comp', 'pos': 'Pos', 'age': 'Age',
            'Playing Time_MP': 'MP', 'Playing Time_Min': 'Min',
            'Performance_Gls': 'Gls', 'Performance_Ast': 'Ast',
            'Expected_xG': 'xG', 'Expected_xAG': 'xAG',
            'Progression_PrgC': 'PrgC', 'Progression_PrgP': 'PrgP',
            'Total_Cmp%': 'Cmp%', 'Tackles_Tkl': 'Tkl', 'Int': 'Int',
            'Blocks_Blocks': 'Blocks', 'Standard_Sh': 'Sh',
            'Per 90 Minutes_Gls': 'Gls_per90', 'Per 90 Minutes_Ast': 'Ast_per90'
        }
        
        existing_mapping = {k: v for k, v in column_mapping.items() if k in df.columns}
        df = df.rename(columns=existing_mapping)
        df = df.loc[:, ~df.columns.duplicated(keep='first')]
        
        # Ensure columns exist
        required_cols = ['Player', 'Squad', 'Comp', 'Pos', 'Age', 'MP', 'Min', 
                        'Gls', 'Ast', 'xG', 'xAG', 'PrgC', 'PrgP', 'Cmp%', 
                        'Tkl', 'Int', 'Blocks', 'Sh']
        for col in required_cols:
            if col not in df.columns: df[col] = 0
            
        df = df.fillna(0)
        
        # Market Value Calculation
        df['Market_Value_EUR'] = (
            df['Gls'] * 2000000 + df['Ast'] * 1500000 + 
            df['xG'] * 1800000 + df['xAG'] * 1200000 +
            (35 - df['Age']) * 500000
        ).clip(lower=500000, upper=150000000)
        
        return df
    except Exception as e:
        st.error(f"Data Error: {e}")
        return pd.DataFrame()

df = load_data()

# -----------------------------------------------------------------------------
# SIDEBAR FILTERS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🎯 SCOUT FILTERS")
    
    leagues = ['All'] + sorted(df['Comp'].unique().tolist())
    selected_league = st.selectbox("League", leagues)
    
    positions = ['All'] + sorted(df['Pos'].unique().tolist())
    selected_position = st.selectbox("Position", positions)
    
    age_range = st.slider("Age", int(df['Age'].min()), int(df['Age'].max()), (17, 28))
    
    max_val = int(df['Market_Value_EUR'].max() / 1000000)
    value_range = st.slider("Max Value (€M)", 0, max_val, 40)
    
    min_mins = st.slider("Min Minutes", 0, int(df['Min'].max()), 500)
    
    st.markdown("---")
    st.markdown("## ⚖️ WEIGHTS")
    w_goals = st.slider("Goals", 0.0, 5.0, 3.0)
    w_assists = st.slider("Assists", 0.0, 5.0, 2.0)
    w_xg = st.slider("xG", 0.0, 5.0, 2.5)
    w_prog = st.slider("Progressive", 0.0, 5.0, 1.5)
    w_def = st.slider("Defensive", 0.0, 5.0, 1.0)

# -----------------------------------------------------------------------------
# FILTERING & SCORING LOGIC
# -----------------------------------------------------------------------------
filtered_df = df.copy()
if selected_league != 'All': filtered_df = filtered_df[filtered_df['Comp'] == selected_league]
if selected_position != 'All': filtered_df = filtered_df[filtered_df['Pos'] == selected_position]
filtered_df = filtered_df[
    (filtered_df['Age'] >= age_range[0]) & (filtered_df['Age'] <= age_range[1]) &
    (filtered_df['Market_Value_EUR'] <= value_range * 1000000) & (filtered_df['Min'] >= min_mins)
]

def calculate_score(row):
    pos = row['Pos']
    if 'FW' in str(pos):
        score = (row['Gls']*w_goals + row['Ast']*w_assists + row['xG']*w_xg + 
                 (row['PrgC']+row['PrgP'])/10*w_prog)
    elif 'MF' in str(pos):
        score = (row['Gls']*w_goals*0.8 + row['Ast']*w_assists*1.5 + 
                 (row['PrgC']+row['PrgP'])/5*w_prog + (row['Tkl']+row['Int'])/10*w_def)
    elif 'DF' in str(pos):
        score = ((row['Tkl']+row['Int']+row['Blocks'])/5*w_def + 
                 row['PrgP']/10*w_prog + row['Cmp%']/10)
    else:
        score = row['Cmp%']/5 + row['PrgP']/5
        
    val_mil = row['Market_Value_EUR'] / 1000000
    return score / (val_mil**0.7) if val_mil > 0 else score

if not filtered_df.empty:
    filtered_df['Score'] = filtered_df.apply(calculate_score, axis=1)
    filtered_df['Score'] = (filtered_df['Score'] / filtered_df['Score'].max() * 100).fillna(0)
    filtered_df = filtered_df.sort_values('Score', ascending=False)

# -----------------------------------------------------------------------------
# MAIN DASHBOARD
# -----------------------------------------------------------------------------
st.title("⚽ Moneyball Pro Analytics")
st.markdown("### Next-Gen Player Scouting & Analysis Platform")

# TABS
tab1, tab2, tab3, tab4 = st.tabs(["🕵️ Scout Center", "⚔️ Player Comparison", "🏢 Team Analysis", "📊 League Stats"])

# --- TAB 1: SCOUT CENTER ---
with tab1:
    if filtered_df.empty:
        st.warning("No players found. Adjust filters.")
    else:
        # KPI Cards
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""<div class="glass-card"><div class="metric-label">Players Found</div>
                        <div class="metric-value">{len(filtered_df)}</div></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="glass-card"><div class="metric-label">Avg Age</div>
                        <div class="metric-value">{filtered_df['Age'].mean():.1f}</div></div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class="glass-card"><div class="metric-label">Avg Value</div>
                        <div class="metric-value">€{filtered_df['Market_Value_EUR'].mean()/1000000:.1f}M</div></div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class="glass-card"><div class="metric-label">Top Score</div>
                        <div class="metric-value">{filtered_df['Score'].max():.1f}</div></div>""", unsafe_allow_html=True)

        # Main Scatter Plot (Interactive)
        st.markdown("### 💎 Value vs Performance Matrix")
        
        fig_scatter = px.scatter(
            filtered_df, 
            x="Market_Value_EUR", 
            y="Score", 
            size="Min", 
            color="Score",
            hover_name="Player",
            hover_data=["Squad", "Age", "Pos", "Gls", "Ast"],
            color_continuous_scale="Viridis",
            template="plotly_dark",
            labels={"Market_Value_EUR": "Market Value (€)", "Score": "Moneyball Score"},
            height=500
        )
        fig_scatter.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

        # Top Players List
        st.markdown("### 🏆 Top Hidden Gems")
        top_players = filtered_df.head(10)[['Player', 'Squad', 'Pos', 'Age', 'Market_Value_EUR', 'Score', 'Gls', 'Ast']]
        top_players['Market_Value_EUR'] = top_players['Market_Value_EUR'].apply(lambda x: f"€{x/1000000:.1f}M")
        top_players['Score'] = top_players['Score'].apply(lambda x: f"{x:.1f}")
        
        st.dataframe(
            top_players, 
            use_container_width=True,
            column_config={
                "Score": st.column_config.ProgressColumn("Moneyball Score", format="%s", min_value=0, max_value=100),
            }
        )

# --- TAB 2: PLAYER COMPARISON ---
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        p1_name = st.selectbox("Select Player 1", df['Player'].unique(), index=0)
    with col2:
        p2_name = st.selectbox("Select Player 2", df['Player'].unique(), index=1)
        
    if p1_name and p2_name:
        p1 = df[df['Player'] == p1_name].iloc[0]
        p2 = df[df['Player'] == p2_name].iloc[0]
        
        # Radar Chart Data
        categories = ['Gls', 'Ast', 'xG', 'PrgP', 'Tkl', 'Int', 'Cmp%']
        
        # Normalize for chart (simple min-max for demo)
        def get_norm_val(player, cat):
            max_val = df[cat].max()
            return (player[cat] / max_val) * 100 if max_val > 0 else 0

        fig_radar = go.Figure()

        fig_radar.add_trace(go.Scatterpolar(
            r=[get_norm_val(p1, c) for c in categories],
            theta=categories,
            fill='toself',
            name=p1['Player'],
            line_color='#3b82f6'
        ))

        fig_radar.add_trace(go.Scatterpolar(
            r=[get_norm_val(p2, c) for c in categories],
            theta=categories,
            fill='toself',
            name=p2['Player'],
            line_color='#ef4444'
        ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], showticklabels=False, gridcolor='rgba(255,255,255,0.2)'),
                bgcolor='rgba(0,0,0,0)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=True,
            height=500
        )
        
        c1, c2 = st.columns([1, 1])
        with c1:
            st.plotly_chart(fig_radar, use_container_width=True)
        with c2:
            st.markdown("### Head-to-Head Stats")
            
            # Comparison Table
            comp_data = {
                'Metric': ['Age', 'Market Value', 'Goals', 'Assists', 'xG', 'Progressive Passes'],
                p1['Player']: [
                    int(p1['Age']), 
                    f"€{p1['Market_Value_EUR']/1000000:.1f}M",
                    int(p1['Gls']), int(p1['Ast']), f"{p1['xG']:.2f}", int(p1['PrgP'])
                ],
                p2['Player']: [
                    int(p2['Age']), 
                    f"€{p2['Market_Value_EUR']/1000000:.1f}M",
                    int(p2['Gls']), int(p2['Ast']), f"{p2['xG']:.2f}", int(p2['PrgP'])
                ]
            }
            st.dataframe(pd.DataFrame(comp_data), use_container_width=True, hide_index=True)

# --- TAB 3: TEAM ANALYSIS ---
with tab3:
    st.markdown("### 🏢 Team Performance Landscape")
    
    # Group by team
    team_stats = df.groupby('Squad').agg({
        'Age': 'mean',
        'Market_Value_EUR': 'mean',
        'Gls': 'sum',
        'xG': 'sum',
        'Player': 'count'
    }).reset_index()
    
    team_stats['Avg Value (€M)'] = team_stats['Market_Value_EUR'] / 1000000
    
    fig_team = px.scatter(
        team_stats,
        x="Age",
        y="Avg Value (€M)",
        size="Gls",
        color="xG",
        hover_name="Squad",
        text="Squad",
        color_continuous_scale="Turbo",
        template="plotly_dark",
        title="Team Age vs Average Market Value (Size = Total Goals)",
        height=600
    )
    fig_team.update_traces(textposition='top center')
    fig_team.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_team, use_container_width=True)
    
    # Treemap
    st.markdown("### 🗺️ Market Value Distribution by League & Team")
    fig_tree = px.treemap(
        df,
        path=[px.Constant("All Leagues"), 'Comp', 'Squad'],
        values='Market_Value_EUR',
        color='xG',
        color_continuous_scale='Viridis',
        template="plotly_dark"
    )
    fig_tree.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_tree, use_container_width=True)

# --- TAB 4: LEAGUE STATS ---
with tab4:
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("### ⚽ Top Scorers")
        top_scorers = df.sort_values('Gls', ascending=False).head(10)
        fig_goals = px.bar(
            top_scorers,
            x='Gls',
            y='Player',
            orientation='h',
            color='Gls',
            text='Gls',
            color_continuous_scale='Reds',
            template="plotly_dark"
        )
        fig_goals.update_layout(yaxis={'categoryorder':'total ascending'}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_goals, use_container_width=True)
        
    with c2:
        st.markdown("### 🎯 Top Assisters")
        top_assists = df.sort_values('Ast', ascending=False).head(10)
        fig_ast = px.bar(
            top_assists,
            x='Ast',
            y='Player',
            orientation='h',
            color='Ast',
            text='Ast',
            color_continuous_scale='Blues',
            template="plotly_dark"
        )
        fig_ast.update_layout(yaxis={'categoryorder':'total ascending'}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_ast, use_container_width=True)
    
    st.markdown("### 📊 xG vs Actual Goals (Finishing Efficiency)")
    df['Finishing'] = df['Gls'] - df['xG']
    top_finishers = df[df['Gls']>5].sort_values('Finishing', ascending=False).head(15)
    
    fig_finish = px.bar(
        top_finishers,
        x='Finishing',
        y='Player',
        color='Finishing',
        text='Finishing',  # Added text parameter
        title="Goals above Expected (xG) - Top Finishers",
        template="plotly_dark",
        color_continuous_scale='Tealgrn'
    )
    fig_finish.update_traces(texttemplate='%{text:.2f}', textposition='outside') # Format text
    fig_finish.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_finish, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("<center style='color: #64748b'>Moneyball Pro Analytics • Powered by FBref Data • 2025</center>", unsafe_allow_html=True)
