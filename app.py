import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import os
import warnings

# Suppress sklearn unpickling and other warnings
warnings.filterwarnings('ignore')

# Set page layout and config
st.set_page_config(
    page_title="Multistate Bank - Customer Churn Detection",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium styling using dark gradient and glassmorphism UI
st.markdown("""
<style>
    /* Google Fonts import */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

    /* Darker Deep Ambient Background Gradient (Sunset Ember Theme) */
    .stApp {
        background: 
            radial-gradient(circle at 12% 15%, rgba(0, 200, 230, 0.06) 0%, transparent 40%),
            radial-gradient(circle at 88% 18%, rgba(120, 80, 220, 0.07) 0%, transparent 42%),
            radial-gradient(circle at 50% 50%, rgba(50, 110, 220, 0.04) 0%, transparent 45%),
            radial-gradient(circle at 82% 82%, rgba(0, 200, 230, 0.04) 0%, transparent 38%),
            radial-gradient(circle at 18% 85%, rgba(180, 60, 130, 0.04) 0%, transparent 40%),
            linear-gradient(135deg, #05060b 0%, #020205 50%, #07080e 100%);
        background-attachment: fixed;
        color: #f8f9fa;
        font-family: 'Inter', sans-serif;
    }
    
    /* Streamlit Sidebar Background Override */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(13, 15, 26, 0.95) 0%, rgba(7, 8, 14, 0.98) 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.07);
    }
    
    /* Title typography styling */
    .main-title {
        font-family: 'Outfit', sans-serif;
        background: linear-gradient(90deg, #7EC8FF 0%, #45F0FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.8rem;
        margin-bottom: 0.2rem;
        text-shadow: 0px 4px 15px rgba(0, 220, 242, 0.18);
    }
    
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        flex-wrap: wrap;
        margin-bottom: 0.2rem;
    }
    
    .social-links {
        display: flex;
        gap: 16px;
        align-items: center;
    }
    
    .social-link {
        color: rgba(255, 255, 255, 0.65);
        text-decoration: none;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .social-link:hover {
        color: #45F0FF;
        transform: translateY(-3px) scale(1.12);
        filter: drop-shadow(0px 0px 12px rgba(0, 220, 242, 0.6));
    }
    
    .subtitle {
        color: #a0aec0;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Premium Glassmorphism Cards */
    .glass-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.04) 0%, rgba(255, 255, 255, 0.015) 100%);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 12px 35px 0 rgba(0, 0, 0, 0.4);
        transition: transform 0.3s ease, box-shadow 0.3s ease, border 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 18px 40px 0 rgba(0, 220, 242, 0.08);
        border: 1px solid rgba(0, 220, 242, 0.18);
    }
    
    /* KPI dashboard container and items */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 16px;
        margin-bottom: 24px;
    }
    
    .kpi-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.035) 0%, rgba(255, 255, 255, 0.01) 100%);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 14px;
        padding: 20px 15px;
        text-align: center;
        box-shadow: 0 6px 22px rgba(0, 0, 0, 0.25);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    
    .kpi-card:hover {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 220, 242, 0.20);
        transform: translateY(-3px);
        box-shadow: 0 10px 28px rgba(0, 220, 242, 0.08);
    }
    
    .kpi-val {
        font-family: 'Outfit', sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #45F0FF;
        margin-top: 5px;
        text-shadow: 0 0 14px rgba(69, 240, 255, 0.35);
    }
    
    .kpi-title {
        font-size: 0.8rem;
        color: #a0aec0;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 600;
    }
    
    /* Custom Styling for Streamlit Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(255, 255, 255, 0.025);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.07);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        background-color: transparent;
        border-radius: 8px;
        color: #a0aec0;
        font-weight: 600;
        transition: all 0.2s ease;
        padding: 8px 20px;
        border: 1px solid transparent;
        font-family: 'Outfit', sans-serif;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #ffffff;
        background-color: rgba(255, 255, 255, 0.035);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(69, 240, 255, 0.16) 0%, rgba(79, 172, 254, 0.16) 100%) !important;
        color: #45F0FF !important;
        border: 1px solid rgba(69, 240, 255, 0.35) !important;
        box-shadow: 0 4px 15px rgba(69, 240, 255, 0.15);
    }
    
    /* Form Inputs and Select Boxes Customization */
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        background-color: rgba(12, 16, 30, 0.75) !important;
        border: 1px solid rgba(0, 220, 242, 0.18) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.4) !important;
    }
    
    div[data-baseweb="select"] > div:hover, div[data-baseweb="input"] > div:hover {
        border-color: #45F0FF !important;
        box-shadow: 0 0 12px rgba(0, 220, 242, 0.20) !important;
    }

    /* BaseWeb MultiSelect Tags / Badges styling */
    span[data-baseweb="tag"], div[data-baseweb="tag"] {
        background: linear-gradient(135deg, rgba(0, 220, 242, 0.18) 0%, rgba(139, 92, 246, 0.25) 100%) !important;
        border: 1px solid rgba(69, 240, 255, 0.4) !important;
        border-radius: 8px !important;
        padding: 3px 10px !important;
    }

    span[data-baseweb="tag"] span, div[data-baseweb="tag"] span {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        font-family: 'Outfit', sans-serif !important;
    }

    span[data-baseweb="tag"] svg, div[data-baseweb="tag"] svg {
        fill: #45F0FF !important;
    }

    /* Custom Streamlit Expander styling for Filter Panel */
    div[data-testid="stExpander"] {
        background: linear-gradient(135deg, rgba(15, 20, 38, 0.65) 0%, rgba(8, 12, 24, 0.75) 100%) !important;
        border: 1px solid rgba(69, 240, 255, 0.22) !important;
        border-radius: 14px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4) !important;
        margin-bottom: 8px !important;
        overflow: hidden;
    }

    div[data-testid="stExpander"] details summary {
        background: rgba(69, 240, 255, 0.06) !important;
        border-bottom: 1px solid rgba(69, 240, 255, 0.15) !important;
        padding: 14px 20px !important;
    }

    div[data-testid="stExpander"] details summary p {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        color: #45F0FF !important;
        font-size: 1.05rem !important;
        letter-spacing: 0.3px !important;
    }

    div[data-testid="stExpander"] details summary:hover {
        background: rgba(0, 220, 242, 0.08) !important;
    }

    /* Widget Labels Styling */
    label[data-testid="stWidgetLabel"] p, label p {
        font-family: 'Outfit', sans-serif !important;
        color: #cbd5e0 !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        letter-spacing: 0.4px !important;
        margin-bottom: 4px !important;
    }

    /* Dropdown Options Popup styling */
    div[data-baseweb="popover"] ul {
        background-color: #0b0f19 !important;
        border: 1px solid rgba(69, 240, 255, 0.35) !important;
        border-radius: 10px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6) !important;
    }

    div[data-baseweb="popover"] li {
        color: #e2e8f0 !important;
        font-family: 'Inter', sans-serif !important;
    }

    div[data-baseweb="popover"] li:hover {
        background-color: rgba(69, 240, 255, 0.18) !important;
        color: #45F0FF !important;
    }

    /* Prediction Banner Results */
    .result-banner {
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        font-size: 1.3rem;
        font-weight: bold;
        margin-top: 20px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    .result-banner.success {
        background: linear-gradient(135deg, rgba(56, 239, 125, 0.18) 0%, rgba(17, 153, 142, 0.18) 100%);
        border: 1px solid rgba(56, 239, 125, 0.5);
        color: #38EF7D;
        box-shadow: 0 0 20px rgba(56, 239, 125, 0.15);
    }
    
    .result-banner.danger {
        background: linear-gradient(135deg, rgba(255, 78, 80, 0.18) 0%, rgba(249, 212, 35, 0.18) 100%);
        border: 1px solid rgba(255, 78, 80, 0.5);
        color: #FF4E50;
        box-shadow: 0 0 20px rgba(255, 78, 80, 0.15);
    }
    
    /* Analysis text customization */
    .analysis-text {
        font-size: 0.95rem;
        line-height: 1.6;
        color: #cbd5e0;
    }
    
    .analysis-title {
        color: #45F0FF;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 10px;
    }

    /* Subheader customization */
    h3 {
        font-family: 'Outfit', sans-serif !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border-bottom: 1px solid rgba(255,255,255,0.07);
        padding-bottom: 8px;
    }
    
</style>
""", unsafe_allow_html=True)

# ----------------- DATA & MODEL LOADING -----------------

@st.cache_data
def load_data():
    csv_file = "Bank Customer Churn Prediction.csv"
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        return df
    else:
        st.error(f"Error: Dataset '{csv_file}' not found in the workspace!")
        return None

@st.cache_resource
def load_models_and_scaler():
    model_dir = "bank customer churn models"
    scaler = joblib.load(os.path.join(model_dir, "scaler.pkl"))
    lr = joblib.load(os.path.join(model_dir, "logistic_regression_model.pkl"))
    dt = joblib.load(os.path.join(model_dir, "decision_tree_model.pkl"))
    rf = joblib.load(os.path.join(model_dir, "random_forest_model.pkl"))
    return scaler, lr, dt, rf

# Load components
df = load_data()
models_loaded = False
try:
    scaler, lr_model, dt_model, rf_model = load_models_and_scaler()
    models_loaded = True
except Exception as e:
    st.error(f"Failed to load machine learning models: {e}")

# ----------------- APPLICATION HEADER -----------------

st.markdown("""
<div class="header-container">
    <div class="main-title">Multistate Bank Customer Churn Detection</div>
    <div class="social-links">
        <a href="https://www.linkedin.com/in/m-zain-khan-2555913a9/" target="_blank" class="social-link" title="LinkedIn">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="28px" height="28px">
                <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
            </svg>
        </a>
        <a href="https://github.com/Zain-Khan-AI" target="_blank" class="social-link" title="GitHub">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="28px" height="28px">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
            </svg>
        </a>
        <a href="https://orcid.org/0009-0005-6976-4636" target="_blank" class="social-link" title="ORCID">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="28px" height="28px">
                <path d="M12 0C5.372 0 0 5.372 0 12s5.372 12 12 12 12-5.372 12-12S18.628 0 12 0zm-3.41 17.52H6.93V6.48h1.66v11.04zm-.83-12.28c-.6 0-1.09-.49-1.09-1.09s.49-1.09 1.09-1.09 1.09.49 1.09 1.09-.49 1.09-1.09 1.09zm8.62 12.28h-3.23c-1.39 0-2.52-1.13-2.52-2.52v-6c0-1.39 1.13-2.52 2.52-2.52h3.23c1.39 0 2.52 1.13 2.52 2.52v6c0 1.39-1.13 2.52-2.52 2.52zm-.09-9.36h-3.05c-.46 0-.83.37-.83.83v5.04c0 .46.37.83.83.83h3.05c.46 0 .83-.37.83-.83V8.99c0-.46-.37-.83-.83-.83z"/>
            </svg>
        </a>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown('<div class="subtitle">Interactive Customer Churn Analysis & Machine Learning Predictions</div>', unsafe_allow_html=True)

# Create 4 tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Analytics Dashboard", 
    "🔮 Churn Predictor", 
    "📈 Model Evaluation", 
    "ℹ️ About Project"
])

# ----------------- TAB 1: ANALYTICS DASHBOARD -----------------
with tab1:
    if df is not None:
        # Filter Panel Container
        with st.expander("🔍 Interactive Analytics Filter Panel — Click to expand / collapse filters", expanded=True):
            f_col1, f_col2, f_col3, f_col4 = st.columns(4)
            
            countries = sorted(df['country'].dropna().unique().tolist())
            genders = sorted(df['gender'].dropna().unique().tolist())
            products = sorted(df['products_number'].dropna().unique().tolist())
            
            with f_col1:
                sel_countries = st.multiselect("🌍 Country", options=countries, default=countries, key="filter_country")
            with f_col2:
                sel_genders = st.multiselect("👤 Gender", options=genders, default=genders, key="filter_gender")
            with f_col3:
                sel_products = st.multiselect("📦 Products", options=products, default=products, key="filter_products")
            with f_col4:
                sel_active = st.selectbox("🛡️ Active Member", options=["All", "Active Only", "Inactive Only"], index=0, key="filter_active")
                
            f_col5, f_col6 = st.columns(2)
            min_age_val, max_age_val = int(df['age'].min()), int(df['age'].max())
            min_cs_val, max_cs_val = int(df['credit_score'].min()), int(df['credit_score'].max())
            
            with f_col5:
                sel_age = st.slider("🎂 Age Range (Years)", min_value=min_age_val, max_value=max_age_val, value=(min_age_val, max_age_val), key="filter_age")
            with f_col6:
                sel_credit = st.slider("💳 Credit Score Range", min_value=min_cs_val, max_value=max_cs_val, value=(min_cs_val, max_cs_val), key="filter_credit")

        
        # Vectorized filtering logic
        mask = (
            df['country'].isin(sel_countries) &
            df['gender'].isin(sel_genders) &
            df['products_number'].isin(sel_products) &
            df['age'].between(sel_age[0], sel_age[1]) &
            df['credit_score'].between(sel_credit[0], sel_credit[1])
        )
        if sel_active == "Active Only":
            mask &= (df['active_member'] == 1)
        elif sel_active == "Inactive Only":
            mask &= (df['active_member'] == 0)
        filtered_df = df[mask]
        
        # Count Badge / Information Bar
        total_count = len(df)
        filtered_count = len(filtered_df)
        pct_filtered = (filtered_count / total_count * 100) if total_count > 0 else 0
        
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(0, 242, 254, 0.06); border: 1px solid rgba(0, 242, 254, 0.2); border-radius: 12px; padding: 12px 20px; margin-bottom: 24px; backdrop-filter: blur(8px);">
            <span style="font-size: 0.98rem; color: #f8f9fa;">
                📊 <b>Filtered Dataset:</b> Displaying <span style="color:#45F0FF; font-weight:700;">{filtered_count:,}</span> of <b>{total_count:,}</b> customers (<b>{pct_filtered:.1f}%</b> of total data)
            </span>
            <span style="font-size: 0.85rem; color: #a0aec0; background: rgba(255,255,255,0.05); padding: 4px 12px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.08);">
                { '⚡ Filters Active' if filtered_count < total_count else '✓ All Records Selected' }
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        if filtered_count == 0:
            st.warning("⚠️ No customer records match the current filter selection. Please broaden your filter parameters above.")
        else:
            # Calculate KPIs using filtered_df
            total_customers = len(filtered_df)
            churned_customers = filtered_df['churn'].sum()
            churn_rate = (churned_customers / total_customers) * 100 if total_customers > 0 else 0
            avg_credit_score = filtered_df['credit_score'].mean() if total_customers > 0 else 0
            avg_balance = filtered_df['balance'].mean() if total_customers > 0 else 0
            active_member_rate = (filtered_df['active_member'].mean() * 100) if total_customers > 0 else 0
            
            # Display KPIs in grid
            st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-card">
                    <div class="kpi-title">Total Customers</div>
                    <div class="kpi-val">{total_customers:,}</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-title">Avg Credit Score</div>
                    <div class="kpi-val">{avg_credit_score:.1f}</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-title">Avg Balance</div>
                    <div class="kpi-val">${avg_balance:,.2f}</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-title">Active Member Rate</div>
                    <div class="kpi-val">{active_member_rate:.1f}%</div>
                </div>
                <div class="kpi-card" style="border: 1px solid rgba(255, 78, 80, 0.2);">
                    <div class="kpi-title" style="color: #FF4E50;">Churn Rate</div>
                    <div class="kpi-val" style="color: #FF4E50;">{churn_rate:.2f}%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Plotly theme updates for dark styling (enhanced)
            def update_plotly_theme(fig, height=420):
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='Inter', color='#e2e8f0', size=13),
                    title_font=dict(family='Outfit', size=18, color='#ffffff'),
                    title_pad=dict(t=10, b=10),
                    height=height,
                    margin=dict(l=20, r=20, t=60, b=20),
                    legend=dict(
                        font=dict(color='#e2e8f0', size=12),
                        bgcolor='rgba(255,255,255,0.04)',
                        bordercolor='rgba(255,255,255,0.08)',
                        borderwidth=1,
                        orientation='h',
                        yanchor='bottom',
                        y=1.02,
                        xanchor='right',
                        x=1
                    ),
                    xaxis=dict(
                        gridcolor='rgba(255,255,255,0.06)',
                        gridwidth=1,
                        zerolinecolor='rgba(255,255,255,0.12)',
                        tickfont=dict(color='#a0aec0', size=12),
                        title_font=dict(color='#cbd5e0', size=13),
                        showspikes=True,
                        spikecolor='rgba(0,242,254,0.4)',
                        spikethickness=1,
                        spikedash='dot'
                    ),
                    yaxis=dict(
                        gridcolor='rgba(255,255,255,0.06)',
                        gridwidth=1,
                        zerolinecolor='rgba(255,255,255,0.12)',
                        tickfont=dict(color='#a0aec0', size=12),
                        title_font=dict(color='#cbd5e0', size=13)
                    ),
                    hoverlabel=dict(
                        bgcolor='rgba(10,10,20,0.92)',
                        bordercolor='rgba(0,242,254,0.5)',
                        font=dict(family='Inter', size=13, color='#e2e8f0')
                    )
                )
                return fig

            def create_churn_bar(data, col, title, colors, x_label, hover_suffix="", bar_width=None):
                grp_df = data.groupby(col, observed=False)['churn'].mean().reset_index()
                grp_df['churn_rate'] = grp_df['churn'] * 100
                if col == 'active_member':
                    grp_df['active_member'] = grp_df['active_member'].map({0: 'Inactive', 1: 'Active'})
                
                fig = px.bar(
                    grp_df, x=col, y='churn_rate', title=title,
                    color=col, color_discrete_sequence=colors, text='churn_rate',
                    labels={col: x_label, 'churn_rate': 'Churn Rate (%)'}
                )
                trace_kwargs = dict(
                    marker_line_color='rgba(0,0,0,0.3)', marker_line_width=1.5,
                    texttemplate='%{text:.1f}%', textposition='outside', textfont=dict(size=13, color='#e2e8f0'),
                    hovertemplate=f'<b>%{{x}}{hover_suffix}</b><br>Churn Rate: <b>%{{y:.2f}}%</b><extra></extra>'
                )
                if bar_width:
                    trace_kwargs['width'] = bar_width
                fig.update_traces(**trace_kwargs)
                fig.update_layout(showlegend=False, bargap=0.4, coloraxis_showscale=False)
                if col == 'products_number':
                    fig.update_xaxes(type='category', title_text=x_label)
                return update_plotly_theme(fig)

            # Charts Section
            st.markdown("### Demographic & Profile Analysis")
            
            row1_col1, row1_col2 = st.columns(2)
            
            # Chart 1: Donut Chart for overall Churn
            with row1_col1:
                churn_pie = px.pie(
                    filtered_df, 
                    names='churn', 
                    title='Overall Churn Distribution',
                    color='churn',
                    color_discrete_map={0: '#38EF7D', 1: '#FF4E50'},
                    hole=0.5,
                    labels={'churn': 'Status', 'count': 'Customers'}
                )
                churn_pie.update_traces(
                    labels=['Retained', 'Churned'], 
                    textposition='inside', 
                    textinfo='percent+label',
                    textfont=dict(size=13, family='Outfit'),
                    pull=[0.03, 0.06],
                    marker=dict(
                        line=dict(color='rgba(10,10,20,0.8)', width=3)
                    ),
                    hovertemplate='<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>'
                )
                churn_pie.add_annotation(
                    text=f"<b>{churn_rate:.1f}%</b><br><span style='font-size:11px'>Churn</span>",
                    x=0.5, y=0.5, showarrow=False,
                    font=dict(size=18, color='#FF4E50', family='Outfit')
                )
                st.plotly_chart(update_plotly_theme(churn_pie), use_container_width=True)
                
            # Chart 2: Churn by Geography
            with row1_col2:
                fig_geo = create_churn_bar(filtered_df, 'country', 'Churn Rate by Country (%)', ['#4FACFE', '#FF4E50', '#38EF7D'], 'Country')
                st.plotly_chart(fig_geo, use_container_width=True)
                
            row2_col1, row2_col2 = st.columns(2)
            
            # Chart 3: Churn by Number of Products
            with row2_col1:
                fig_prod = create_churn_bar(filtered_df, 'products_number', 'Churn Rate by Number of Products (%)', ['#38EF7D', '#FFD700', '#FF8C00', '#FF4E50'], 'Number of Products', hover_suffix=" Products")
                st.plotly_chart(fig_prod, use_container_width=True)
                
            # Chart 4: Churn by Age Groups
            with row2_col2:
                # Group by age bins
                filtered_df_age = filtered_df.copy()
                filtered_df_age['age_group'] = pd.cut(
                    filtered_df_age['age'], 
                    bins=[18, 30, 40, 50, 60, 100], 
                    labels=['18-30', '30-40', '40-50', '50-60', '60+']
                )
                age_data = filtered_df_age.groupby('age_group', observed=False)['churn'].mean().reset_index()
                age_data['churn_rate'] = age_data['churn'] * 100
                
                fig_age = px.area(
                    age_data, 
                    x='age_group', 
                    y='churn_rate', 
                    title='Churn Rate by Age Group (%)',
                    markers=True,
                    color_discrete_sequence=['#00F2FE'],
                    labels={'age_group': 'Age Group', 'churn_rate': 'Churn Rate (%)'}
                )
                fig_age.update_traces(
                    line=dict(width=3.5, color='#00F2FE'),
                    marker=dict(size=10, color='#00F2FE', line=dict(color='#ffffff', width=2)),
                    fillcolor='rgba(0,242,254,0.12)',
                    hovertemplate='<b>Age Group: %{x}</b><br>Churn Rate: <b>%{y:.2f}%</b><extra></extra>'
                )
                st.plotly_chart(update_plotly_theme(fig_age), use_container_width=True)
                
            row3_col1, row3_col2 = st.columns(2)
            
            # Chart 5: Churn by Gender
            with row3_col1:
                fig_gender = create_churn_bar(filtered_df, 'gender', 'Churn Rate by Gender (%)', ['#F093FB', '#4FACFE'], 'Gender', bar_width=0.45)
                st.plotly_chart(fig_gender, use_container_width=True)
                
            # Chart 6: Active Member Status vs Churn
            with row3_col2:
                fig_active = create_churn_bar(filtered_df, 'active_member', 'Churn Rate: Active vs Inactive Members (%)', ['#FF4E50', '#38EF7D'], 'Membership Status', bar_width=0.45)
                st.plotly_chart(fig_active, use_container_width=True)

            row4_col1, row4_col2 = st.columns(2)

            # Chart 7: Churn Rate by Tenure
            with row4_col1:
                tenure_data = filtered_df.groupby('tenure')['churn'].mean().reset_index()
                tenure_data['churn_rate'] = tenure_data['churn'] * 100

                fig_tenure = px.area(
                    tenure_data,
                    x='tenure',
                    y='churn_rate',
                    title='Churn Rate by Tenure (Years)',
                    markers=True,
                    color_discrete_sequence=['#F093FB'],
                    labels={'tenure': 'Tenure (Years)', 'churn_rate': 'Churn Rate (%)'}
                )
                fig_tenure.update_traces(
                    line=dict(width=3, color='#F093FB'),
                    marker=dict(size=9, color='#F093FB', line=dict(color='#ffffff', width=2)),
                    fillcolor='rgba(240,147,251,0.12)',
                    hovertemplate='<b>Tenure: %{x} yrs</b><br>Churn Rate: <b>%{y:.2f}%</b><extra></extra>'
                )
                fig_tenure.update_xaxes(dtick=1)
                st.plotly_chart(update_plotly_theme(fig_tenure), use_container_width=True)

            # Chart 8: Credit Score Distribution — Churned vs Retained
            with row4_col2:
                cs_churned = filtered_df[filtered_df['churn'] == 1]['credit_score']
                cs_retained = filtered_df[filtered_df['churn'] == 0]['credit_score']

                fig_cs = go.Figure()
                fig_cs.add_trace(go.Box(
                    y=cs_churned,
                    name='Churned',
                    marker_color='#FF4E50',
                    line=dict(color='#FF4E50', width=2),
                    fillcolor='rgba(255,78,80,0.15)',
                    boxmean='sd',
                    hovertemplate='<b>Churned</b><br>%{y}<extra></extra>'
                ))
                fig_cs.add_trace(go.Box(
                    y=cs_retained,
                    name='Retained',
                    marker_color='#38EF7D',
                    line=dict(color='#38EF7D', width=2),
                    fillcolor='rgba(56,239,125,0.15)',
                    boxmean='sd',
                    hovertemplate='<b>Retained</b><br>%{y}<extra></extra>'
                ))
                fig_cs.update_layout(
                    title={
                        'text': '<b>Credit Score: Churned vs Retained</b>',
                        'font': {'family': 'Outfit', 'size': 16, 'color': '#ffffff'},
                        'x': 0.5, 'xanchor': 'center'
                    },
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='Inter', color='#e2e8f0', size=13),
                    yaxis=dict(
                        title='Credit Score',
                        gridcolor='rgba(255,255,255,0.06)',
                        tickfont=dict(color='#a0aec0')
                    ),
                    xaxis=dict(tickfont=dict(color='#a0aec0')),
                    legend=dict(
                        bgcolor='rgba(255,255,255,0.04)',
                        bordercolor='rgba(255,255,255,0.08)',
                        borderwidth=1,
                        font=dict(size=12)
                    ),
                    margin=dict(l=20, r=20, t=60, b=20),
                    height=380,
                    hoverlabel=dict(
                        bgcolor='rgba(10,10,20,0.92)',
                        bordercolor='rgba(0,242,254,0.5)',
                        font=dict(family='Inter', size=12)
                    )
                )
                st.plotly_chart(fig_cs, use_container_width=True)

            # ---- Feature Correlation Heatmap Section in Analytics Dashboard ----
            st.markdown("### 🔗 Feature Correlation Heatmap")
            st.markdown("The heatmap below illustrates linear correlation coefficients between customer attributes and churn status, helping identify key drivers of customer attrition.")

            # Compute Correlation Matrix
            corr_df = filtered_df.copy()
            if 'gender' in corr_df.columns:
                corr_df['gender'] = corr_df['gender'].map({'Female': 0, 'Male': 1})
            
            feature_cols = ['credit_score', 'gender', 'age', 'tenure', 'balance', 'products_number', 'credit_card', 'active_member', 'estimated_salary', 'churn']
            existing_cols = [c for c in feature_cols if c in corr_df.columns]
            corr_matrix = corr_df[existing_cols].corr()

            label_map = {
                'credit_score': 'Credit Score',
                'gender': 'Gender',
                'age': 'Age',
                'tenure': 'Tenure',
                'balance': 'Balance',
                'products_number': 'Products',
                'credit_card': 'Credit Card',
                'active_member': 'Active Member',
                'estimated_salary': 'Salary',
                'churn': 'Churn'
            }
            labels = [label_map.get(col, col) for col in existing_cols]

            col_corr_map, col_corr_info = st.columns([1.6, 1])

            with col_corr_map:
                fig_corr = px.imshow(
                    corr_matrix.values,
                    x=labels,
                    y=labels,
                    text_auto='.2f',
                    color_continuous_scale=[
                        [0.0, '#FF4E50'],
                        [0.5, 'rgba(20, 25, 45, 0.9)'],
                        [1.0, '#00F2FE']
                    ],
                    zmin=-0.5,
                    zmax=0.5,
                    aspect='auto'
                )
                fig_corr.update_traces(
                    textfont=dict(size=12, family='Outfit', color='white'),
                    hovertemplate='<b>%{x}</b> vs <b>%{y}</b><br>Correlation: <b>%{z:.3f}</b><extra></extra>'
                )
                fig_corr.update_layout(
                    title={
                        'text': '<b>Feature Correlation Heatmap</b>',
                        'font': {'family': 'Outfit', 'size': 18, 'color': '#ffffff'},
                        'x': 0.5, 'xanchor': 'center'
                    },
                    coloraxis_showscale=True,
                    coloraxis_colorbar=dict(
                        title=dict(text='Corr', font=dict(color='#a0aec0', size=12)),
                        tickfont=dict(color='#a0aec0', size=11),
                        bgcolor='rgba(255,255,255,0.04)',
                        bordercolor='rgba(255,255,255,0.1)',
                        borderwidth=1,
                        len=0.85
                    ),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='Inter', color='#e2e8f0', size=12),
                    height=420,
                    margin=dict(l=20, r=20, t=60, b=20),
                    xaxis=dict(tickfont=dict(size=11, color='#a0aec0'), tickangle=-30),
                    yaxis=dict(tickfont=dict(size=11, color='#a0aec0')),
                    hoverlabel=dict(
                        bgcolor='rgba(10,10,20,0.92)',
                        bordercolor='rgba(0,242,254,0.5)',
                        font=dict(family='Inter', size=12)
                    )
                )
                st.plotly_chart(fig_corr, use_container_width=True)

            with col_corr_info:
                st.markdown("""
                <div class="analysis-title">🔍 Key Feature Correlations</div>
                <div class="analysis-text">
                <div style="margin-bottom:16px;">
                    <div class="kpi-title">📈 Age (+0.29)</div>
                    <div style="font-size:0.92rem; color:#e2e8f0; margin-top:4px;">
                        Strongest positive correlation with churn. Older customers exhibit significantly higher attrition rates.
                    </div>
                </div>
                <div style="margin-bottom:16px;">
                    <div class="kpi-title">🛡️ Active Member (-0.16)</div>
                    <div style="font-size:0.92rem; color:#e2e8f0; margin-top:4px;">
                        Strongest negative correlation with churn. Active membership significantly reduces churn risk.
                    </div>
                </div>
                <div style="margin-bottom:16px;">
                    <div class="kpi-title">💳 Balance (+0.12)</div>
                    <div style="font-size:0.92rem; color:#e2e8f0; margin-top:4px;">
                        Positive correlation with churn. Higher balance customers churn at slightly higher rates.
                    </div>
                </div>
                <div style="margin-bottom:16px;">
                    <div class="kpi-title">👤 Gender (-0.11)</div>
                    <div style="font-size:0.92rem; color:#e2e8f0; margin-top:4px;">
                        Male customers (coded 1) show lower churn propensity compared to female customers (coded 0).
                    </div>
                </div>
                <div style="margin-bottom:16px;">
                    <div class="kpi-title">📦 Products (-0.05)</div>
                    <div style="font-size:0.92rem; color:#e2e8f0; margin-top:4px;">
                        Non-linear effect: 2 products is optimal, but holding 3 or 4 products leads to severe churn (>80%).
                    </div>
                </div>
                </div>
                """, unsafe_allow_html=True)

            # Analysis Summary Box
            st.markdown("""
            <div class="glass-card">
                <div class="analysis-title">📈 Key Analytical Takeaways</div>
                <div class="analysis-text">
                <ul>
                    <li><b>Geographic Churn:</b> Customers in <b>Germany</b> exhibit a churn rate of <b>32.4%</b>, which is roughly double the churn rate of customers in France (16.2%) and Spain (16.7%). This indicates potential issues with regional services, fees, or localized competitor pressure.</li>
                    <li><b>Product Proliferation Risk:</b> There is a massive risk associated with multiple products. While customers holding 1 or 2 products have relatively low churn rates (27.7% and 7.6% respectively), churn jumps to <b>82.7% for 3 products</b> and <b>100% for 4 products</b>. This might be due to forced cross-selling or high fees associated with multi-product packages.</li>
                    <li><b>Age Risk Profile:</b> Customer attrition increases significantly with age. The churn rate peaks between <b>50-60 years old at over 56.2%</b>, compared to just <b>7.5%</b> for customers under 30. This suggests the bank might be losing wealth-accumulating, older, long-term clients.</li>
                    <li><b>Engagement Impact:</b> Inactive members churn at a rate of <b>26.9%</b>, while active members churn at <b>14.3%</b>. Activating disengaged customers represents a major churn mitigation opportunity.</li>
                </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ----------------- TAB 2: CHURN PREDICTOR -----------------
with tab2:
    st.markdown("""
    <div class="glass-card">
        <h3 style="color:#45F0FF; font-family:'Outfit',sans-serif; margin-bottom:8px;">🤖 Predict Customer Churn Risk</h3>
        <p style="color:#cbd5e0; line-height:1.7; margin:0;">Use this tool to evaluate the churn probability of any individual customer. Select a trained machine learning model, fill in the customer's profile attributes, and run the prediction to see their attrition risk score.</p>
    </div>
    """, unsafe_allow_html=True)

    if not models_loaded:
        st.warning("Model prediction is unavailable because the model or scaler pickle files could not be loaded.")
    else:
        st.markdown("Select a trained model from the dropdown below, fill in the customer's attributes, and run the prediction to evaluate their probability of leaving the bank.")
        
        # Model selection dropdown
        selected_model = st.selectbox(
            "Select Prediction Model", 
            ["Random Forest (Recommended)", "Logistic Regression", "Decision Tree"],
            index=0
        )
        
        # Build 3 column inputs
        with st.form("churn_prediction_form"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                credit_score = st.number_input(
                    "Credit Score", 
                    min_value=300, max_value=850, value=650, step=1,
                    help="Standard credit score range (300 to 850)"
                )
                age = st.number_input(
                    "Age (Years)", 
                    min_value=18, max_value=100, value=40, step=1
                )
                tenure = st.number_input(
                    "Tenure (Years of membership)", 
                    min_value=0, max_value=20, value=5, step=1
                )
                
            with col2:
                balance = st.number_input(
                    "Account Balance ($)", 
                    min_value=0.0, max_value=250000.0, value=75000.0, step=1000.0,
                    help="Amount of money in the customer's account"
                )
                estimated_salary = st.number_input(
                    "Estimated Salary ($)", 
                    min_value=0.0, max_value=250000.0, value=100000.0, step=1000.0
                )
                products_number = st.selectbox(
                    "Number of Products", 
                    [1, 2, 3, 4], 
                    index=0,
                    help="Total bank products (accounts, loans, insurance, etc.) the customer holds"
                )
                
            with col3:
                country = st.selectbox("Country of Residence", ["France", "Germany", "Spain"], index=0)
                gender = st.selectbox("Gender", ["Female", "Male"], index=0)
                credit_card = st.selectbox("Has Credit Card?", ["No", "Yes"], index=1)
                active_member = st.selectbox("Is Active Member?", ["No", "Yes"], index=1)
            
            st.markdown("<br>", unsafe_allow_html=True)
            submit_btn = st.form_submit_button("Predict Churn Probability")
        
        # Prediction Logic
        if submit_btn:
            # Map input categories to matches used in training
            gender_val = 1 if gender == "Male" else 0
            country_germany = 1 if country == "Germany" else 0
            country_spain = 1 if country == "Spain" else 0
            credit_card_val = 1 if credit_card == "Yes" else 0
            active_member_val = 1 if active_member == "Yes" else 0
            
            # Construct feature row
            # Order matches notebook: credit_score, gender, age, tenure, balance, products_number, credit_card, active_member, estimated_salary, country_Germany, country_Spain
            input_row = np.array([[
                credit_score, gender_val, age, tenure, balance, 
                products_number, credit_card_val, active_member_val, 
                estimated_salary, country_germany, country_spain
            ]])
            
            # Preprocess features using the trained scaler
            try:
                scaled_input = scaler.transform(input_row)
                
                # Pick model
                if "Random Forest" in selected_model:
                    model = rf_model
                    model_lbl = "Random Forest"
                elif "Logistic Regression" in selected_model:
                    model = lr_model
                    model_lbl = "Logistic Regression"
                else:
                    model = dt_model
                    model_lbl = "Decision Tree"
                
                # Predict
                prob = model.predict_proba(scaled_input)[0][1]
                churn_pct = prob * 100
                prediction = model.predict(scaled_input)[0]
                
                # Plot Gauge Chart for Churn Probability (enhanced)
                bar_color = "#38EF7D" if churn_pct < 30 else ("#FFD700" if churn_pct < 70 else "#FF4E50")
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = churn_pct,
                    delta = {'reference': 20, 'valueformat': '.1f', 'suffix': '%',
                             'increasing': {'color': '#FF4E50'}, 'decreasing': {'color': '#38EF7D'}},
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {
                        'text': f"<b>Churn Risk — {model_lbl}</b>",
                        'font': {'size': 17, 'family': 'Outfit', 'color': '#ffffff'}
                    },
                    number = {
                        'suffix': "%",
                        'font': {'color': bar_color, 'size': 52, 'family': 'Outfit'},
                        'valueformat': '.1f'
                    },
                    gauge = {
                        'axis': {
                            'range': [0, 100],
                            'tickwidth': 2,
                            'tickcolor': '#a0aec0',
                            'tickfont': {'size': 12, 'color': '#a0aec0'},
                            'nticks': 6
                        },
                        'bar': {'color': bar_color, 'thickness': 0.28},
                        'bgcolor': "rgba(255, 255, 255, 0.04)",
                        'borderwidth': 2,
                        'bordercolor': "rgba(255, 255, 255, 0.1)",
                        'steps': [
                            {'range': [0, 30], 'color': 'rgba(56, 239, 125, 0.12)'},
                            {'range': [30, 70], 'color': 'rgba(255, 215, 0, 0.10)'},
                            {'range': [70, 100], 'color': 'rgba(255, 78, 80, 0.14)'}
                        ],
                        'threshold': {
                            'line': {'color': 'white', 'width': 3},
                            'thickness': 0.82,
                            'value': churn_pct
                        }
                    }
                ))
                
                fig_gauge.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    font={'color': "#ffffff", 'family': "Inter"},
                    height=340,
                    margin=dict(l=30, r=30, t=60, b=20)
                )
                
                # Display Results
                col_res1, col_res2 = st.columns([1, 1.5])
                
                with col_res1:
                    st.plotly_chart(fig_gauge, use_container_width=True)
                    
                with col_res2:
                    st.markdown("### Prediction Verdict")
                    if churn_pct >= 50.0:
                        st.markdown(f"""
                        <div class="result-banner danger">
                            ⚠️ HIGH RISK: Customer is likely to CHURN (Probability: {churn_pct:.2f}%)
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("#### 🛠️ Recommended Action Plan:")
                        recommendations = []
                        if country == "Germany":
                            recommendations.append("- **Local German Account Audit:** Customer is in Germany, which has an overall high churn. Reach out via German-based customer care representatives to resolve local issues.")
                        if products_number >= 3:
                            recommendations.append("- **Multi-Product Consolidation Fee Waiver:** The customer has 3 or more products. This configuration has a historical churn rate of >80%. Offer a consolidated waiver of product package fees.")
                        if age > 45:
                            recommendations.append("- **Retirement & Wealth Management Outreach:** Customer is in a high-risk older age group. Connect them with a dedicated relationship manager to offer customized high-yield savings options.")
                        if active_member == "No":
                            recommendations.append("- **Engagement Campaign:** Customer is inactive. Send a personalized engagement offer or reward to stimulate active card use or login activity.")
                        if not recommendations:
                            recommendations.append("- **Proactive Retention Outreach:** Schedule a feedback call and offer a loyalty rate reduction on services.")
                        
                        st.markdown("\n".join(recommendations))
                    else:
                        st.markdown(f"""
                        <div class="result-banner success">
                            ✅ LOW RISK: Customer is likely to remain RETAINED (Probability: {churn_pct:.2f}%)
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("#### 💡 Retention Strategy:")
                        st.markdown("""
                        - **Loyalty Rewards:** Maintain active relationship. Offer reward points or minor service upgrades to reinforce loyalty.
                        - **Cross-selling Caution:** If cross-selling, do not exceed 2 total bank products, as 3+ products show severe churn rates.
                        """)
                
            except Exception as ex:
                st.error(f"Error during preprocessing or prediction: {ex}")

# ----------------- TAB 3: MODEL PERFORMANCE EVALUATION -----------------
with tab3:
    st.markdown("""
    <div class="glass-card">
        <h3 style="color:#45F0FF; font-family:'Outfit',sans-serif; margin-bottom:8px;">📊 Model Performance Evaluation &amp; Comparison</h3>
        <p style="color:#cbd5e0; line-height:1.7; margin:0;">Below are the evaluation metrics for the three models calculated on the holdout test set (20% of the original data). Metrics include Accuracy, Precision, Recall, and F1-Score to comprehensively assess each model's performance.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Pre-calculated metrics from notebook
    metrics = {
        'Model': ['Logistic Regression', 'Decision Tree', 'Random Forest'],
        'Accuracy': [0.8110, 0.7840, 0.8665],
        'Precision': [0.5524, 0.4549, 0.7647],
        'Recall': [0.2010, 0.5012, 0.4631],
        'F1-Score': [0.2948, 0.4769, 0.5768]
    }
    metrics_df = pd.DataFrame(metrics)
    
    # Display comparison table
    st.dataframe(
        metrics_df.style.format({
            'Accuracy': '{:.2%}',
            'Precision': '{:.2%}',
            'Recall': '{:.2%}',
            'F1-Score': '{:.2%}'
        }),
        use_container_width=True,
        hide_index=True
    )
    
    # Plotly Metrics Comparison Bar Chart
    metrics_melted = metrics_df.melt(id_vars='Model', var_name='Metric', value_name='Score')
    fig_metrics = px.bar(
        metrics_melted, 
        x='Metric', 
        y='Score', 
        color='Model', 
        barmode='group',
        title='Model Performance Metrics Comparison',
        color_discrete_sequence=['#F093FB', '#FFB347', '#00F2FE'],
        text='Score',
        labels={'Score': 'Score (0–1)', 'Metric': 'Evaluation Metric'}
    )
    fig_metrics.update_traces(
        texttemplate='%{text:.2f}',
        textposition='outside',
        textfont=dict(size=11),
        marker_line_color='rgba(0,0,0,0.3)',
        marker_line_width=1.5,
        hovertemplate='<b>%{x}</b><br>Model: <b>%{fullData.name}</b><br>Score: <b>%{y:.4f}</b><extra></extra>'
    )
    fig_metrics.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color='#e2e8f0', size=13),
        title_font=dict(family='Outfit', size=18, color='#ffffff'),
        height=440,
        margin=dict(l=20, r=20, t=70, b=20),
        xaxis=dict(gridcolor='rgba(255,255,255,0.06)', tickfont=dict(color='#a0aec0', size=12)),
        yaxis=dict(gridcolor='rgba(255,255,255,0.06)', range=[0, 1.1], tickfont=dict(color='#a0aec0', size=12)),
        legend=dict(
            bgcolor='rgba(255,255,255,0.04)',
            bordercolor='rgba(255,255,255,0.08)',
            borderwidth=1,
            font=dict(size=12)
        ),
        hoverlabel=dict(
            bgcolor='rgba(10,10,20,0.92)',
            bordercolor='rgba(0,242,254,0.5)',
            font=dict(family='Inter', size=13)
        ),
        bargap=0.25,
        bargroupgap=0.1
    )
    st.plotly_chart(fig_metrics, use_container_width=True)
    
    # Confusion Matrices
    st.markdown("""
    <div class="glass-card">
        <h3 style="color:#45F0FF; font-family:'Outfit',sans-serif; margin-bottom:8px;">🔢 Confusion Matrices</h3>
        <p style="color:#cbd5e0; line-height:1.7; margin:0;">The confusion matrices below illustrate the True Positives, True Negatives, False Positives, and False Negatives for each model on the test set — providing a detailed breakdown of classification performance beyond simple accuracy.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # CM structures
    cm_lr = np.array([[1543, 64], [314, 79]])
    cm_dt = np.array([[1371, 236], [196, 197]])
    cm_rf = np.array([[1551, 56], [211, 182]])
    
    # Helper to plot Heatmap (enhanced)
    def plot_heatmap_cm(cm, title, colorscale):
        labels = ['No Churn (Predicted)', 'Churn (Predicted)']
        row_labels = ['No Churn (Actual)', 'Churn (Actual)']
        fig = px.imshow(
            cm, 
            text_auto=True,
            x=labels, 
            y=row_labels,
            color_continuous_scale=colorscale,
            aspect='auto',
            zmin=0
        )
        fig.update_traces(
            texttemplate='<b>%{z:,}</b>',
            textfont=dict(size=18, family='Outfit', color='white'),
            hovertemplate='<b>%{y}</b><br>%{x}<br>Count: <b>%{z:,}</b><extra></extra>'
        )
        fig.update_layout(
            title={
                'text': f'<b>{title}</b>',
                'font': {'family': 'Outfit', 'size': 16, 'color': '#ffffff'},
                'x': 0.5,
                'xanchor': 'center'
            },
            coloraxis_showscale=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', color='#e2e8f0', size=12),
            height=300,
            margin=dict(l=10, r=10, t=55, b=10),
            xaxis=dict(
                tickfont=dict(size=11, color='#a0aec0'),
                side='bottom'
            ),
            yaxis=dict(
                tickfont=dict(size=11, color='#a0aec0')
            ),
            hoverlabel=dict(
                bgcolor='rgba(10,10,20,0.92)',
                bordercolor='rgba(0,242,254,0.5)',
                font=dict(family='Inter', size=12)
            )
        )
        return fig
    
    col_cm1, col_cm2, col_cm3 = st.columns(3)
    
    with col_cm1:
        st.plotly_chart(plot_heatmap_cm(cm_lr, "Logistic Regression", "Purples"), use_container_width=True)
        
    with col_cm2:
        st.plotly_chart(plot_heatmap_cm(cm_dt, "Decision Tree", "Oranges"), use_container_width=True)
        
    with col_cm3:
        st.plotly_chart(plot_heatmap_cm(cm_rf, "Random Forest", "Blues"), use_container_width=True)

    st.markdown("""
    <div class="glass-card">
        <div class="analysis-title">🔬 Evaluation Analysis & Summary</div>
        <div class="analysis-text">
        <ul>
            <li><b>Winner: Random Forest</b> is the clear winner across almost all dimensions. It has the highest <b>Accuracy (86.65%)</b>, <b>Precision (76.47%)</b>, and <b>F1-Score (57.68%)</b>. It is the most reliable model for deployment.</li>
            <li><b>The Recall Tradeoff:</b> While the <b>Decision Tree</b> has a slightly higher <b>Recall (50.12%)</b> than Random Forest (46.31%), its <b>Precision (45.49%)</b> is extremely poor. It generates 236 False Positives, compared to only 56 for Random Forest.</li>
            <li><b>Logistic Regression Drawbacks:</b> Logistic Regression fails significantly at identifying churning customers. Its <b>Recall of 20.10%</b> means it fails to identify 80% of the customers who actually leave, making it highly ineffective for a retention campaign.</li>
        </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ----------------- TAB 4: ABOUT PROJECT -----------------
with tab4:
    st.markdown("### About the Customer Churn Project")
    
    st.markdown("""
    <div class="glass-card">
        <h4 style="color:#45F0FF; font-family:'Outfit',sans-serif; margin-bottom:10px;">1. Project Background</h4>
        <p style="color:#cbd5e0; line-height:1.7;">Customer retention is a critical metric for banking organizations. Acquiring a new customer can cost up to 5 times more than retaining an existing one. This project is dedicated to <b>predicting bank customer attrition</b> (churn) using historical profile data from 10,000 customers of a multistate bank.</p>
        <p style="color:#cbd5e0; line-height:1.7;">By employing data analysis and machine learning models, the bank's marketing and operations team can predict which customers are at risk of leaving and proactively implement retention strategies.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
        <h4 style="color:#45F0FF; font-family:'Outfit',sans-serif; margin-bottom:10px;">2. Preprocessing &amp; Feature Engineering</h4>
        <div style="color:#cbd5e0; line-height:1.7;">
        To train the model, the raw customer database underwent the following transformations:
        <ul>
            <li><b>Customer ID Exclusion:</b> <code>customer_id</code> was dropped as it carries no statistical significance for prediction.</li>
            <li><b>One-Hot Encoding:</b> The categorical feature <code>country</code> was converted to indicator variables (<code>country_Germany</code> and <code>country_Spain</code>, using France as the baseline reference category).</li>
            <li><b>Label Encoding:</b> The <code>gender</code> column was mapped to binary values (<code>Female</code> = 0, <code>Male</code> = 1).</li>
            <li><b>Feature Scaling:</b> Since metrics like Credit Score, Balance, and Salary have vastly different scales, a <code>StandardScaler</code> was fit on the training data to normalize features prior to model fit.</li>
        </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
        <h4 style="color:#45F0FF; font-family:'Outfit',sans-serif; margin-bottom:10px;">3. Strategic Recommendations for ABC Bank</h4>
        <div style="color:#cbd5e0; line-height:1.7;">
        Based on the models and analytics dashboard, we recommend the following interventions:
        <ol>
            <li><b>Localized Action for German Accounts:</b> Churn in Germany stands at 32.4%. We recommend conducting service audits, customer experience interviews, and pricing reviews for accounts in Germany.</li>
            <li><b>Multi-Product Package Review:</b> The bank should evaluate fee structures for customers holding 3 or 4 products. It is likely that these customers are overcharged or experiencing high pricing friction, causing massive attrition (&gt;80%).</li>
            <li><b>Active Membership Incentives:</b> Create campaigns (e.g. cashback on card usage, high-yield product trials) targeted at inactive users, since active status drops churn by nearly 50%.</li>
            <li><b>VIP Channels for Older Customers:</b> Customers aged 45-60 control significant wealth but have high churn rates. Create specialized retirement savings or high-yield investment services to secure these accounts.</li>
        </ol>
        </div>
    </div>
    """, unsafe_allow_html=True)
