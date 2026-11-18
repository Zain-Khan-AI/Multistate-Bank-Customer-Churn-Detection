import os
import glob
import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

GITHUB_URL = "https://github.com/Zain-Khan-AI"
LINKEDIN_URL = "https://www.linkedin.com/in/m-zainkhan/"

GITHUB_SVG = """
<svg height="16" width="16" viewBox="0 0 16 16" fill="currentColor" style="vertical-align: -2px; margin-right: 6px;">
  <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
</svg>
"""

LINKEDIN_SVG = """
<svg height="16" width="16" viewBox="0 0 24 24" fill="currentColor" style="vertical-align: -2px; margin-right: 6px;">
  <path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/>
</svg>
"""


# ==============================================================================
# 1. PAGE CONFIGURATION & FINTECH SAAS DESIGN SYSTEM
# ==============================================================================
st.set_page_config(
    page_title="Bank Churn Intelligence",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
@import url('https://googleapis.com');

:root {
    --bg-primary: #060913;
    --bg-secondary: #0D1324;
    --bg-card: rgba(17, 25, 45, 0.75);
    --border-subtle: rgba(148, 163, 184, 0.15);
    --border-glow: rgba(56, 189, 248, 0.45);
    --text-main: #F8FAFC;
    --text-muted: #94A3B8;
    --accent-cyan: #38BDF8;
    --accent-indigo: #818CF8;
    --accent-emerald: #10B981;
    --accent-amber: #F59E0B;
    --accent-rose: #F43F5E;
}

.creator-actions {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.6rem;
}

.social-pill {
    display: inline-flex;
    align-items: center;
    padding: 0.45rem 0.9rem;
    border-radius: 10px;
    font-size: 0.82rem;
    font-weight: 600;
    text-decoration: none !important;
    transition: all 0.2s ease;
    border: 1px solid rgba(148, 163, 184, 0.22);
    background: rgba(15, 23, 42, 0.85);
    color: #F8FAFC !important;
}

.social-pill:hover {
    transform: translateY(-2px);
    border-color: #38BDF8;
    box-shadow: 0 6px 18px rgba(56, 189, 248, 0.2);
    color: #38BDF8 !important;
}

.gen-by-pill {
    display: inline-flex;
    align-items: center;
    padding: 0.45rem 0.95rem;
    border-radius: 10px;
    font-size: 0.82rem;
    font-weight: 700;
    text-decoration: none !important;
    background: linear-gradient(135deg, rgba(56, 189, 248, 0.16), rgba(129, 140, 248, 0.18));
    border: 1px solid rgba(56, 189, 248, 0.4);
    color: #E0F2FE !important;
    transition: all 0.2s ease;
}

.gen-by-pill:hover {
    transform: translateY(-2px);
    background: linear-gradient(135deg, rgba(56, 189, 248, 0.28), rgba(129, 140, 248, 0.3));
    color: #FFFFFF !important;
}


html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: var(--bg-primary);
    color: var(--text-main);
}

.stApp {
    background:
        radial-gradient(circle at 12% 8%, rgba(56, 189, 248, 0.09), transparent 35%),
        radial-gradient(circle at 88% 12%, rgba(129, 140, 248, 0.09), transparent 38%),
        linear-gradient(180deg, #060913 0%, #090E1C 100%);
}

section[data-testid="stSidebar"] {
    background-color: #090E1C;
    border-right: 1px solid var(--border-subtle);
}

/* Hero Banner */
.product-header {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.92) 0%, rgba(30, 41, 59, 0.68) 100%);
    border: 1px solid var(--border-subtle);
    border-left: 4px solid var(--accent-cyan);
    border-radius: 16px;
    padding: 1.4rem 1.8rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.35);
}

.product-badge {
    display: inline-block;
    background: rgba(56, 189, 248, 0.14);
    color: var(--accent-cyan);
    border: 1px solid rgba(56, 189, 248, 0.35);
    padding: 0.22rem 0.75rem;
    border-radius: 999px;
    font-size: 0.74rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.product-title {
    font-size: 1.85rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin: 0;
    color: #FFFFFF;
}

.product-sub {
    color: var(--text-muted);
    font-size: 0.95rem;
    margin-top: 0.3rem;
}

/* KPI Cards */
.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 14px;
    padding: 1.15rem 1.3rem;
    backdrop-filter: blur(12px);
    transition: transform 0.2s ease, border-color 0.2s ease;
}

.kpi-card:hover {
    transform: translateY(-2px);
    border-color: var(--border-glow);
}

.kpi-label {
    color: var(--text-muted);
    font-size: 0.76rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.kpi-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.6rem;
    font-weight: 700;
    color: #FFFFFF;
    margin: 0.25rem 0;
}

.kpi-delta {
    font-size: 0.8rem;
    font-weight: 500;
}

/* Verdict Banners */
.verdict-high {
    background: linear-gradient(135deg, rgba(244, 63, 94, 0.18), rgba(15, 23, 42, 0.92));
    border: 1px solid rgba(244, 63, 94, 0.55);
    border-radius: 16px;
    padding: 1.35rem;
    margin-bottom: 1rem;
}

.verdict-low {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.18), rgba(15, 23, 42, 0.92));
    border: 1px solid rgba(16, 185, 129, 0.55);
    border-radius: 16px;
    padding: 1.35rem;
    margin-bottom: 1rem;
}

.action-pill {
    background: rgba(30, 41, 59, 0.85);
    border-left: 3px solid var(--accent-cyan);
    padding: 0.75rem 1rem;
    border-radius: 8px;
    margin-bottom: 0.6rem;
    font-size: 0.9rem;
}

.js-plotly-plot .plotly .main-svg {
    background: transparent !important;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ==============================================================================
# 2. PATHS, MODEL REGISTRY & EXACT FEATURE SCHEMA
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "Bank Customer Churn Prediction.csv")
MODELS_DIR = os.path.join(BASE_DIR, "bank customer churn models")

EXACT_FEATURE_COLUMNS = [
    "credit_score",
    "gender",
    "age",
    "tenure",
    "balance",
    "products_number",
    "credit_card",
    "active_member",
    "estimated_salary",
    "country_Germany",
    "country_Spain",
    "Balance_Salary_Ratio",
    "Tenure_Age_Ratio",
    "Is_Zero_Balance",
    "Active_With_Card",
]

MODEL_SPECS = {
    "Voting Ensemble (Best #1)": {
        "keywords": ["voting"],
        "rank": "#1 Best Overall (Default)",
        "badge": "🥇 Champion",
        "desc": "Soft-voting ensemble combining top gradient boosted & bagged trees for maximum F1 and generalization.",
        "metrics": {"Accuracy": 0.8690, "Precision": 0.7280, "Recall": 0.6412, "F1 Score": 0.6819, "ROC-AUC": 0.874},
    },
    "XGBoost Classifier (#2)": {
        "keywords": ["xgb", "xgboost"],
        "rank": "#2 Runner-Up",
        "badge": "🥈 2nd Best",
        "desc": "250-tree regularized XGBoost (max_depth=4, lr=0.04, subsample=0.8) tuned for non-linear churn signals.",
        "metrics": {"Accuracy": 0.8645, "Precision": 0.7110, "Recall": 0.6361, "F1 Score": 0.6715, "ROC-AUC": 0.869},
    },
    "Gradient Boosting (#3)": {
        "keywords": ["gradient"],
        "rank": "#3 Contender",
        "badge": "🥉 3rd Best",
        "desc": "250-estimator Scikit-Learn Gradient Boosting Classifier with calibrated binomial log-loss.",
        "metrics": {"Accuracy": 0.8610, "Precision": 0.7042, "Recall": 0.6234, "F1 Score": 0.6613, "ROC-AUC": 0.865},
    },
    "Random Forest (#4)": {
        "keywords": ["random", "forest"],
        "rank": "#4 Baseline Ensemble",
        "badge": "4th Rank",
        "desc": "250-tree Random Forest Classifier providing low-variance bagging benchmarks.",
        "metrics": {"Accuracy": 0.8565, "Precision": 0.6925, "Recall": 0.6107, "F1 Score": 0.6490, "ROC-AUC": 0.858},
    },
}


@st.cache_data(show_spinner=False)
def load_dataset():
    if not os.path.exists(DATA_PATH):
        return None
    df = pd.read_csv(DATA_PATH)
    if "customer_id" in df.columns:
        df = df.drop(columns=["customer_id"])

    df["Churn_Label"] = df["churn"].map({0: "Retained (0)", 1: "Churned (1)"})
    df["Active_Label"] = df["active_member"].map({0: "Inactive", 1: "Active"})
    df["Card_Label"] = df["credit_card"].map({0: "No Card", 1: "Has Card"})
    df["Balance_Type"] = np.where(df["balance"] == 0, "Zero Balance ($0)", "Positive Balance (>$0)")

    bins = [18, 30, 40, 50, 60, 100]
    labels = ["18-29", "30-39", "40-49", "50-59", "60+"]
    df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels, right=False)
    return df


@st.cache_resource(show_spinner=False)
def load_ml_artifacts():
    artifacts = {
        "models": {},
        "scaler": None,
        "threshold": 0.50,
        "features": EXACT_FEATURE_COLUMNS,
        "loaded_files": [],
        "errors": [],
    }

    if not os.path.exists(MODELS_DIR):
        artifacts["errors"].append(f"Directory not found: {MODELS_DIR}")
        return artifacts

    joblib_files = glob.glob(os.path.join(MODELS_DIR, "*.joblib"))
    if not joblib_files:
        artifacts["errors"].append(f"No .joblib files found inside {MODELS_DIR}")
        return artifacts

    for filepath in joblib_files:
        fname = os.path.basename(filepath).lower()
        try:
            obj = joblib.load(filepath)
        except Exception as exc:
            artifacts["errors"].append(f"Failed loading {os.path.basename(filepath)}: {exc}")
            continue

        # 1. Detect Scaler
        if "scaler" in fname or hasattr(obj, "scale_"):
            artifacts["scaler"] = obj
            artifacts["loaded_files"].append(f"Scaler: {os.path.basename(filepath)}")
            if hasattr(obj, "feature_names_in_"):
                artifacts["features"] = list(obj.feature_names_in_)
            continue

        # 2. Detect Threshold / Metadata Dict
        if isinstance(obj, dict):
            if "threshold" in obj:
                artifacts["threshold"] = float(obj["threshold"])
            if "feature_columns" in obj:
                artifacts["features"] = list(obj["feature_columns"])
            artifacts["loaded_files"].append(
                f"Config: {os.path.basename(filepath)} (threshold={artifacts['threshold']:.3f})"
            )
            continue

        if "threshold" in fname and np.ndim(obj) == 0:
            artifacts["threshold"] = float(obj)
            artifacts["loaded_files"].append(f"Threshold: {os.path.basename(filepath)}")
            continue

        if ("feature" in fname or "column" in fname) and isinstance(obj, (list, tuple, np.ndarray)):
            artifacts["features"] = list(obj)
            artifacts["loaded_files"].append(f"Features: {os.path.basename(filepath)}")
            continue

        # 3. Match Trained Classifiers
        for display_name, spec in MODEL_SPECS.items():
            if any(keyword in fname for keyword in spec["keywords"]):
                artifacts["models"][display_name] = obj
                artifacts["loaded_files"].append(
                    f"Model: {os.path.basename(filepath)} -> {display_name}"
                )
                break

    if artifacts["scaler"] is None:
        artifacts["errors"].append("StandardScaler artifact was not detected.")

    return artifacts


def build_feature_vector(
    credit_score, country, gender, age, tenure, balance,
    products_number, credit_card, active_member, estimated_salary, feature_cols
):
    balance_salary_ratio = balance / (estimated_salary + 1.0)
    tenure_age_ratio = tenure / (age + 1.0)
    is_zero_balance = 1 if balance == 0 else 0
    active_with_card = 1 if (active_member == 1 and credit_card == 1) else 0

    feature_map = {
        "credit_score": float(credit_score),
        "gender": 1 if gender == "Male" else 0,
        "age": float(age),
        "tenure": float(tenure),
        "balance": float(balance),
        "products_number": int(products_number),
        "credit_card": int(credit_card),
        "active_member": int(active_member),
        "estimated_salary": float(estimated_salary),
        "country_Germany": 1 if country == "Germany" else 0,
        "country_Spain": 1 if country == "Spain" else 0,
        "Balance_Salary_Ratio": float(balance_salary_ratio),
        "Tenure_Age_Ratio": float(tenure_age_ratio),
        "Is_Zero_Balance": int(is_zero_balance),
        "Active_With_Card": int(active_with_card),
    }
    ordered_row = {column: feature_map.get(column, 0) for column in feature_cols}
    return pd.DataFrame([ordered_row]), feature_map


def style_fig(fig, height=370):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.45)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#E2E8F0", size=12),
        height=height,
        margin=dict(l=20, r=20, t=48, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(gridcolor="rgba(148, 163, 184, 0.12)", zeroline=False)
    return fig

# ==============================================================================
# 3. LOAD RESOURCES
# ==============================================================================
df = load_dataset()
artifacts = load_ml_artifacts()


# ==============================================================================
# 4. SIDEBAR PRODUCT NAVIGATION
# ==============================================================================
with st.sidebar:
    st.markdown("## 🏦 RetainIQ")
    st.caption("Enterprise Bank Churn Intelligence")
    st.markdown("---")
    page = st.radio(
        "WORKSPACE",
        [
            "🎯 Churn Prediction Studio",
            "📊 Full Notebook Analytics",
            "🏆 Model Leaderboard",
        ],
    )
    st.markdown("---")
    st.markdown("### ⚙️ Engine Status")
    loaded_count = len(artifacts["models"])
    st.markdown(f"Models Online: {loaded_count} / 4")
    st.markdown(f"Decision Threshold: {artifacts['threshold']:.2f}")
    st.markdown("Default Engine: Voting Ensemble")
    if artifacts["errors"]:
        with st.expander("⚠️ Artifact Warnings"):
            for err in artifacts["errors"]:
                st.warning(err)
    st.markdown("---")
    st.caption("Dataset: Bank Customer Churn Prediction (10,000 Records)")
    st.markdown(
    f"""
    <div class="creator-actions">
        <a href="{GITHUB_URL}" target="_blank" class="social-pill">
            {GITHUB_SVG} GitHub
        </a>
        <a href="{LINKEDIN_URL}" target="_blank" class="social-pill">
            {LINKEDIN_SVG} LinkedIn
        </a>
        <a href="{LINKEDIN_URL}" target="_blank" class="gen-by-pill">
            ✨ Generated by Zain Khan
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)



# ==============================================================================
# 5. TOP HERO HEADER
# ==============================================================================
st.markdown(
    """
    <div class="product-header">
        <span class="product-badge">ML Production Suite • v2.0</span>
        <h1 class="product-title">Bank Customer Churn Prediction &amp; Analytics</h1>
        <div class="product-sub">Real-time customer attrition scoring powered by Voting Ensemble, XGBoost, Random Forest &amp; Gradient Boosting.</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==============================================================================
# VIEW 1: CHURN PREDICTION STUDIO
# ==============================================================================
if page == "🎯 Churn Prediction Studio":
    if not artifacts["models"]:
        st.error(
            f"No trained .joblib models found in {MODELS_DIR}. "
            "Please verify the folder path and model filenames."
        )
        st.stop()

    col_left, col_right = st.columns([1.15, 1.0], gap="large")
    with col_left:
        st.markdown("### 1. Configure Model & Customer Profile")
        available_models = [m for m in MODEL_SPECS if m in artifacts["models"]]
        default_idx = available_models.index("Voting Ensemble (Champion)") if "Voting Ensemble (Champion)" in available_models else 0
        selected_model_name = st.selectbox(
            "Select Inference Model",
            options=available_models,
            index=default_idx,
        )
        spec = MODEL_SPECS[selected_model_name]
        st.info(f"{spec['badge']} — {spec['rank']}: {spec['desc']}")

        with st.form("prediction_form"):
            c1, c2, c3 = st.columns(3)
            with c1:
                country = st.selectbox("Country", ["France", "Germany", "Spain"])
                gender = st.selectbox("Gender", ["Female", "Male"])
                age = st.slider("Age (Years)", 18, 92, 42)
            with c2:
                credit_score = st.number_input("Credit Score", min_value=350, max_value=850, value=619, step=5)
                tenure = st.slider("Tenure (Years)", 0, 10, 3)
                products_number = st.selectbox("Number of Products", [1, 2, 3, 4], index=0)
            with c3:
                balance = st.number_input("Account Balance ($)", min_value=0.0, max_value=300000.0, value=85000.0, step=1000.0)
                estimated_salary = st.number_input("Estimated Salary ($)", min_value=10.0, max_value=250000.0, value=100000.0, step=1000.0)
                active_member = st.selectbox(
                    "Active Member",
                    [1, 0],
                    format_func=lambda value: "Yes (Active)" if value == 1 else "No (Inactive)",
                )
                credit_card = st.checkbox("Customer holds a Bank Credit Card", value=True)

            submitted = st.form_submit_button(
                "🚀 Run Churn Risk Assessment",
                use_container_width=True,
                type="primary",
            )

    with col_right:
        st.markdown("### 2. Live Risk Verdict & Retention Playbook")

        X_input, _ = build_feature_vector(
            credit_score=credit_score,
            country=country,
            gender=gender,
            age=age,
            tenure=tenure,
            balance=balance,
            products_number=products_number,
            credit_card=1 if credit_card else 0,
            active_member=active_member,
            estimated_salary=estimated_salary,
            feature_cols=artifacts["features"],
        )

        if artifacts["scaler"] is not None:
            X_model = artifacts["scaler"].transform(X_input)
        else:
            X_model = X_input.values

        active_model = artifacts["models"][selected_model_name]
        threshold = artifacts["threshold"]

        if hasattr(active_model, "predict_proba"):
            prob = float(active_model.predict_proba(X_model)[0][1])
        else:
            prob = float(active_model.predict(X_model)[0])

        is_churn = prob >= threshold
        gauge_color = "#F43F5E" if is_churn else "#10B981"

        fig_gauge = go.Figure(
            go.Indicator(
                mode="gauge+number+delta",
                value=prob * 100,
                number={"suffix": "%", "font": {"size": 42, "family": "JetBrains Mono"}},
                delta={
                    "reference": threshold * 100,
                    "increasing": {"color": "#F43F5E"},
                    "decreasing": {"color": "#10B981"},
                },
                title={
                    "text": f"Churn Probability (Threshold: {threshold * 100:.1f}%)",
                    "font": {"size": 14, "color": "#94A3B8"},
                },
                gauge={
                    "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#475569"},
                    "bar": {"color": gauge_color},
                    "bgcolor": "rgba(15, 23, 42, 0.6)",
                    "borderwidth": 1,
                    "bordercolor": "rgba(148, 163, 184, 0.2)",
                    "steps": [
                        {"range": [0, threshold * 100], "color": "rgba(16, 185, 129, 0.14)"},
                        {"range": [threshold * 100, 100], "color": "rgba(244, 63, 94, 0.14)"},
                    ],
                    "threshold": {
                        "line": {"color": "#F59E0B", "width": 3},
                        "thickness": 0.8,
                        "value": threshold * 100,
                    },
                },
            )
        )
        style_fig(fig_gauge, height=265)
        st.plotly_chart(fig_gauge, use_container_width=True)

        if is_churn:
            st.markdown(
                f"""
                <div class="verdict-high">
                    <strong>⚠️ HIGH CHURN RISK DETECTED ({prob * 100:.1f}%)</strong><br>
                    Predicted class: EXIT (1) — exceeds the calibrated threshold of {threshold * 100:.1f}%.<br>
                    Immediate retention outreach is recommended.
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="verdict-low">
                    <strong>✅ LOW CHURN RISK — RETAINED ({prob * 100:.1f}%)</strong><br>
                    Predicted class: STAY (0) — safely below the calibrated threshold of {threshold * 100:.1f}%.
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("#### Multi-Model Consensus Check")
        consensus_cols = st.columns(len(available_models))
        for idx, model_name in enumerate(available_models):
            model = artifacts["models"][model_name]
            model_prob = (
                float(model.predict_proba(X_model)[0][1])
                if hasattr(model, "predict_proba")
                else float(model.predict(X_model)[0])
            )
            short_label = model_name.replace(" (Champion)", "").replace(" Classifier", "")
            consensus_cols[idx].metric(
                label=short_label,
                value=f"{model_prob * 100:.1f}%",
                delta="Churn" if model_prob >= threshold else "Retain",
                delta_color="inverse",
            )

        st.markdown("#### Recommended Retention Actions")
        actions = []
        if active_member == 0:
            actions.append("🔔 Re-engagement campaign: inactive members require a targeted outreach plan.")
        if products_number >= 3:
            actions.append("📦 Product review: assign a relationship manager to audit fees and product value.")
        elif products_number == 1:
            actions.append("🎯 Cross-sell bundle: offer a relevant zero-fee savings or card bundle.")
        if age >= 45:
            actions.append("🛡️ Senior advisory: provide tailored retirement or fixed-deposit consultation.")
        if country == "Germany" and balance > 0:
            actions.append("🇩🇪 Germany high-balance retention: offer preferential interest tiers.")
        if not actions:
            actions.append("🌟 Loyalty maintenance: enroll the customer in automated cashback or tier upgrades.")

        for action in actions:
            st.markdown(f'<div class="action-pill">{action}</div>', unsafe_allow_html=True)

# ==============================================================================
# VIEW 2: FULL NOTEBOOK ANALYTICS
# ==============================================================================
elif page == "📊 Full Notebook Analytics":
    if df is None:
        st.error(f"Dataset not found at {DATA_PATH}.")
        st.stop()

    with st.expander("🔍 Global Portfolio Filters", expanded=False):
        f1, f2, f3 = st.columns(3)
        sel_countries = f1.multiselect("Country", options=df["country"].unique(), default=list(df["country"].unique()))
        sel_genders = f2.multiselect("Gender", options=df["gender"].unique(), default=list(df["gender"].unique()))
        age_range = f3.slider("Age Range", int(df["age"].min()), int(df["age"].max()), (18, 92))

    fdf = df[
        (df["country"].isin(sel_countries))
        & (df["gender"].isin(sel_genders))
        & (df["age"].between(age_range[0], age_range[1]))
    ]

    if fdf.empty:
        st.warning("No records match your active filters. Please adjust the filter selection.")
        st.stop()

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.markdown(f'<div class="kpi-card"><div class="kpi-label">Total Customers</div><div class="kpi-val">{len(fdf):,}</div><div class="kpi-delta">Dataset Records</div></div>', unsafe_allow_html=True)
    k2.markdown(f'<div class="kpi-card"><div class="kpi-label">Churn Rate</div><div class="kpi-val">{fdf["churn"].mean() * 100:.2f}%</div><div class="kpi-delta">{int(fdf["churn"].sum()):,} Exited</div></div>', unsafe_allow_html=True)
    k3.markdown(f'<div class="kpi-card"><div class="kpi-label">Mean Balance</div><div class="kpi-val">${fdf["balance"].mean():,.0f}</div><div class="kpi-delta">Portfolio Average</div></div>', unsafe_allow_html=True)
    k4.markdown(f'<div class="kpi-card"><div class="kpi-label">Average Age</div><div class="kpi-val">{fdf["age"].mean():.1f} yrs</div><div class="kpi-delta">Median: {fdf["age"].median():.0f} yrs</div></div>', unsafe_allow_html=True)
    k5.markdown(f'<div class="kpi-card"><div class="kpi-label">Active Members</div><div class="kpi-val">{fdf["active_member"].mean() * 100:.1f}%</div><div class="kpi-delta">Engaged Base</div></div>', unsafe_allow_html=True)

    eda_group = st.segmented_control(
        "Select Notebook Visualization Section",
        [
            "1. Target & Demographics",
            "2. Feature Distributions",
            "3. Churn Drivers & Violin Plots",
            "4. Age Trends & Correlations",
        ],
        default="1. Target & Demographics",
    )

    if eda_group == "1. Target & Demographics":
        c1, c2, c3 = st.columns(3)
        with c1:
            churn_df = fdf["Churn_Label"].value_counts().reset_index()
            churn_df.columns = ["Churn", "Count"]
            fig = px.bar(churn_df, x="Churn", y="Count", color="Churn", text="Count", title="1. Churn Distribution", color_discrete_map={"Retained (0)": "#10B981", "Churned (1)": "#F43F5E"})
            st.plotly_chart(style_fig(fig), use_container_width=True)
        with c2:
            country_df = fdf["country"].value_counts().reset_index()
            country_df.columns = ["Country", "Count"]
            fig = px.bar(country_df, x="Country", y="Count", color="Country", text="Count", title="2. Country Distribution", color_discrete_sequence=["#38BDF8", "#818CF8", "#F59E0B"])
            st.plotly_chart(style_fig(fig), use_container_width=True)
        with c3:
            gender_df = fdf["gender"].value_counts().reset_index()
            gender_df.columns = ["Gender", "Count"]
            fig = px.bar(gender_df, x="Gender", y="Count", color="Gender", text="Count", title="3. Gender Distribution", color_discrete_sequence=["#EC4899", "#3B82F6"])
            st.plotly_chart(style_fig(fig), use_container_width=True)

        c4, c5 = st.columns(2)
        with c4:
            fig = px.histogram(fdf, x="country", color="Churn_Label", barmode="group", text_auto=True, title="4. Churn Distribution by Country", color_discrete_map={"Retained (0)": "#10B981", "Churned (1)": "#F43F5E"})
            st.plotly_chart(style_fig(fig), use_container_width=True)
        with c5:
            fig = px.histogram(fdf, x="gender", color="Churn_Label", barmode="group", text_auto=True, title="5. Churn Distribution by Gender", color_discrete_map={"Retained (0)": "#10B981", "Churned (1)": "#F43F5E"})
            st.plotly_chart(style_fig(fig), use_container_width=True)

    elif eda_group == "2. Feature Distributions":
        c1, c2, c3 = st.columns(3)
        with c1:
            st.plotly_chart(style_fig(px.histogram(fdf, x="age", nbins=30, title="6. Age Distribution", color_discrete_sequence=["#38BDF8"])), use_container_width=True)
        with c2:
            st.plotly_chart(style_fig(px.histogram(fdf, x="credit_score", nbins=30, title="7. Credit Score Distribution", color_discrete_sequence=["#F43F5E"])), use_container_width=True)
        with c3:
            st.plotly_chart(style_fig(px.histogram(fdf, x="balance", nbins=30, title="8. Balance Distribution", color_discrete_sequence=["#10B981"])), use_container_width=True)

        c4, c5, c6 = st.columns(3)
        with c4:
            tenure_df = fdf["tenure"].value_counts().sort_index().reset_index()
            tenure_df.columns = ["Tenure", "Count"]
            st.plotly_chart(style_fig(px.bar(tenure_df, x="Tenure", y="Count", title="9. Tenure Distribution (Years)", color_discrete_sequence=["#818CF8"])), use_container_width=True)
        with c5:
            product_df = fdf["products_number"].value_counts().sort_index().reset_index()
            product_df.columns = ["Products", "Count"]
            st.plotly_chart(style_fig(px.bar(product_df, x="Products", y="Count", text="Count", title="10. Number of Products Distribution", color_discrete_sequence=["#F59E0B"])), use_container_width=True)
        with c6:
            active_df = fdf["Active_Label"].value_counts().reset_index()
            active_df.columns = ["Active Status", "Count"]
            st.plotly_chart(style_fig(px.bar(active_df, x="Active Status", y="Count", color="Active Status", text="Count", title="11. Active Member Distribution", color_discrete_sequence=["#06B6D4", "#64748B"])), use_container_width=True)

    elif eda_group == "3. Churn Drivers & Violin Plots":
        c1, c2, c3 = st.columns(3)
        for column, title, target in [
            (c1, "12. Age Distribution by Churn", "age"),
            (c2, "13. Credit Score Distribution by Churn", "credit_score"),
            (c3, "14. Balance Distribution by Churn", "balance"),
        ]:
            fig = px.violin(fdf, x="Churn_Label", y=target, color="Churn_Label", box=True, title=title, color_discrete_map={"Retained (0)": "#10B981", "Churned (1)": "#F43F5E"})
            with column:
                st.plotly_chart(style_fig(fig), use_container_width=True)

        c4, c5, c6 = st.columns(3)
        with c4:
            fig = px.histogram(fdf, x="products_number", color="Churn_Label", barmode="group", text_auto=True, title="15. Churn by Number of Products", color_discrete_map={"Retained (0)": "#10B981", "Churned (1)": "#F43F5E"})
            st.plotly_chart(style_fig(fig), use_container_width=True)
        with c5:
            fig = px.histogram(fdf, x="Active_Label", color="Churn_Label", barmode="group", text_auto=True, title="16. Churn by Active Member Status", color_discrete_map={"Retained (0)": "#10B981", "Churned (1)": "#F43F5E"})
            st.plotly_chart(style_fig(fig), use_container_width=True)
        with c6:
            balance_df = fdf.groupby("Balance_Type")["churn"].mean().mul(100).reset_index()
            balance_df.columns = ["Balance Segment", "Churn Rate (%)"]
            fig = px.bar(balance_df, x="Balance Segment", y="Churn Rate (%)", color="Balance Segment", text=balance_df["Churn Rate (%)"].round(2).astype(str) + "%", title="17. Zero vs. Positive Balance Churn Rate", color_discrete_sequence=["#38BDF8", "#F43F5E"])
            st.plotly_chart(style_fig(fig), use_container_width=True)

    elif eda_group == "4. Age Trends & Correlations":
        c1, c2 = st.columns(2)
        with c1:
            age_line = fdf.groupby("age", observed=True)["churn"].mean().mul(100).reset_index()
            fig = px.line(age_line, x="age", y="churn", markers=True, title="18. Churn Rate (%) Trend Across Age", labels={"age": "Age", "churn": "Churn Rate (%)"}, color_discrete_sequence=["#F43F5E"])
            st.plotly_chart(style_fig(fig, height=400), use_container_width=True)
        with c2:
            age_group_df = fdf.groupby("age_group", observed=False)["churn"].mean().mul(100).reset_index()
            age_group_df.columns = ["Age Group", "Churn Rate (%)"]
            fig = px.bar(age_group_df, x="Age Group", y="Churn Rate (%)", color="Churn Rate (%)", text=age_group_df["Churn Rate (%)"].round(1).astype(str) + "%", title="19. Churn Rate (%) by Age Group", color_continuous_scale="OrRd")
            st.plotly_chart(style_fig(fig, height=400), use_container_width=True)

        numerical_columns = ["credit_score", "age", "tenure", "balance", "products_number", "credit_card", "active_member", "estimated_salary", "churn"]
        correlation = fdf[numerical_columns].corr().round(2)
        fig = px.imshow(correlation, text_auto=True, aspect="auto", color_continuous_scale="RdBu_r", zmin=-1, zmax=1, title="20. Correlation Heatmap of Numerical Features")
        st.plotly_chart(style_fig(fig, height=530), use_container_width=True)


# ==============================================================================
# VIEW 3: MODEL LEADERBOARD
# ==============================================================================
elif page == "🏆 Model Leaderboard":
    st.markdown("### Model Hierarchy & Hold-Out Evaluation Benchmarks")
    st.caption("Voting Ensemble is deployed as the default engine; the leaderboard reflects notebook benchmark metrics.")

    rows = []
    for name, info in MODEL_SPECS.items():
        rows.append({
            "Rank": info["badge"],
            "Model Name": name,
            "Artifact Status": "✅ Online" if name in artifacts["models"] else "⚠️ Missing",
            "Accuracy": info["metrics"]["Accuracy"],
            "Precision": info["metrics"]["Precision"],
            "Recall": info["metrics"]["Recall"],
            "F1 Score": info["metrics"]["F1 Score"],
            "ROC-AUC": info["metrics"]["ROC-AUC"],
        })

    benchmark_df = pd.DataFrame(rows)
    st.dataframe(
        benchmark_df.style.format({
            "Accuracy": "{:.2%}",
            "Precision": "{:.2%}",
            "Recall": "{:.2%}",
            "F1 Score": "{:.4f}",
            "ROC-AUC": "{:.3f}",
        }).highlight_max(subset=["Accuracy", "Precision", "Recall", "F1 Score", "ROC-AUC"], color="#065F46"),
        use_container_width=True,
        hide_index=True,
    )

    melted = benchmark_df.melt(
        id_vars=["Model Name", "Rank"],
        value_vars=["Accuracy", "Precision", "Recall", "F1 Score", "ROC-AUC"],
        var_name="Metric",
        value_name="Score",
    )
    benchmark_fig = px.bar(
        melted,
        x="Metric",
        y="Score",
        color="Model Name",
        barmode="group",
        text=melted["Score"].round(3),
        title="Model Performance Comparison Across All Metrics",
        color_discrete_sequence=["#38BDF8", "#818CF8", "#10B981", "#F59E0B"],
    )
    benchmark_fig.update_yaxes(range=[0, 1.05])
    st.plotly_chart(style_fig(benchmark_fig, height=450), use_container_width=True)

    importance_candidates = ["XGBoost Classifier (#2)", "Gradient Boosting (#3)", "Random Forest (#4)"]
    available_importance = [
        name for name in importance_candidates
        if name in artifacts["models"] and hasattr(artifacts["models"][name], "feature_importances_")
    ]
    if available_importance:
        st.markdown("### Learned Feature Importances")
        chosen_model = st.selectbox("Inspect Feature Importances From:", available_importance)
        importance_df = pd.DataFrame({
            "Feature": artifacts["features"],
            "Importance": artifacts["models"][chosen_model].feature_importances_,
        }).sort_values(by="Importance", ascending=True)
        importance_fig = px.bar(
            importance_df,
            x="Importance",
            y="Feature",
            orientation="h",
            title=f"Feature Importance Ranking — {chosen_model}",
            color="Importance",
            color_continuous_scale="Tealgrn",
        )
        st.plotly_chart(style_fig(importance_fig, height=480), use_container_width=True)