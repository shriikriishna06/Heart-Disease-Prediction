import time
import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="Heart Risk Check",
    page_icon="🫀",
    layout="centered",
)

@st.cache_resource
def load_artifacts():
    model = joblib.load("LogReg_heart.pkl")
    scaler = joblib.load("scaler.pkl")
    columns = joblib.load("columns.pkl")
    return model, scaler, columns


model, scaler, expected_columns = load_artifacts()

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap');

    :root {
        --ink: #14202B;
        --muted: #6B7785;
        --line: #E3E8EE;
        --bg: #F6F8FA;
        --accent: #0F766E;
        --accent-dark: #0B5C56;
        --risk: #B42318;
        --risk-bg: #FEF3F2;
        --safe: #067647;
        --safe-bg: #ECFDF3;
    }

    html, body, [class*="css"], .stApp {
        font-family: 'DM Sans', sans-serif;
        color: var(--ink);
    }
    .stApp { background: var(--bg); }

    #MainMenu, footer, header { visibility: hidden; }

    .block-container {
        max-width: 720px;
        padding-top: 3rem;
        padding-bottom: 4rem;
    }

    .app-title {
        font-size: 2.1rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin: 0 0 0.35rem 0;
    }
    .app-sub {
        color: var(--muted);
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    .group-title {
        font-size: 1.05rem;
        font-weight: 700;
        margin: 1.6rem 0 0.2rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--line);
    }

    [data-testid="stForm"] {
        background: #FFFFFF;
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 1.2rem 1.8rem 1.8rem 1.8rem;
        box-shadow: 0 1px 2px rgba(20, 32, 43, 0.04);
    }

    label, [data-testid="stWidgetLabel"] p {
        font-size: 0.88rem !important;
        color: var(--muted) !important;
        font-weight: 500 !important;
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        border-radius: 8px;
        border-color: var(--line);
        background: #FBFCFD;
    }

    div[data-testid="stSlider"] [role="slider"] { background-color: var(--accent); }

    .stButton > button, [data-testid="stFormSubmitButton"] > button {
        width: 100%;
        background: var(--accent);
        color: #fff;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        font-weight: 700;
        font-size: 1rem;
        margin-top: 1.4rem;
        transition: background 0.15s ease;
    }
    .stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover {
        background: var(--accent-dark);
        color: #fff;
    }

    .result {
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        margin-top: 1.6rem;
        border: 1px solid;
    }
    .result.high { background: var(--risk-bg); border-color: #F9C7C2; }
    .result.low  { background: var(--safe-bg); border-color: #B7E4C7; }
    .result h3 { margin: 0 0 0.3rem 0; font-size: 1.35rem; }
    .result.high h3 { color: var(--risk); }
    .result.low  h3 { color: var(--safe); }
    .result p { margin: 0; color: var(--ink); font-size: 0.95rem; }

    .bar-wrap {
        background: rgba(20, 32, 43, 0.08);
        border-radius: 99px;
        height: 8px;
        margin: 1rem 0 0.4rem 0;
        overflow: hidden;
    }
    .bar { height: 100%; border-radius: 99px; }
    .result.high .bar { background: var(--risk); }
    .result.low  .bar { background: var(--safe); }
    .bar-label { font-size: 0.82rem; color: var(--muted); }

    .loader-wrap {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.85rem;
        padding: 2rem 0;
    }
    .loader {
        width: 30px;
        height: 30px;
        border: 3px solid #D3E6E4;
        border-top-color: var(--accent);
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
    }
    .loader-text { color: var(--muted); font-size: 0.95rem; }
    @keyframes spin { to { transform: rotate(360deg); } }

    .disclaimer {
        color: var(--muted);
        font-size: 0.8rem;
        margin-top: 1.6rem;
        line-height: 1.5;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="app-title">Heart risk check</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-sub">Enter your details below to estimate your risk of heart disease.</div>',
    unsafe_allow_html=True,
)

with st.form("risk_form"):

    st.markdown('<div class="group-title">About you</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        age = st.slider("Age", 18, 100, 40)
    with c2:
        sex = st.selectbox("Sex", ["M", "F"], format_func=lambda x: {"M": "Male", "F": "Female"}[x])

    st.markdown('<div class="group-title">Vitals and blood work</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        resting_bp = st.number_input("Resting blood pressure (mm Hg)", 80, 200, 120)
        fasting_bs = st.selectbox(
            "Fasting blood sugar above 120 mg/dL",
            [0, 1],
            format_func=lambda x: "Yes" if x == 1 else "No",
        )
    with c2:
        cholesterol = st.number_input("Cholesterol (mg/dL)", 100, 600, 200)
        max_hr = st.slider("Max heart rate", 60, 220, 150)

    st.markdown('<div class="group-title">Heart tests and symptoms</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        chest_pain = st.selectbox(
            "Chest pain type",
            ["ATA", "NAP", "TA", "ASY"],
            format_func=lambda x: {
                "ATA": "Atypical angina",
                "NAP": "Non-anginal pain",
                "TA": "Typical angina",
                "ASY": "No symptoms",
            }[x],
        )
        resting_ecg = st.selectbox(
            "Resting ECG",
            ["Normal", "ST", "LVH"],
            format_func=lambda x: {
                "Normal": "Normal",
                "ST": "ST-T wave abnormality",
                "LVH": "Left ventricular hypertrophy",
            }[x],
        )
        st_slope = st.selectbox("ST slope", ["Up", "Flat", "Down"])
    with c2:
        exercise_angina = st.selectbox(
            "Chest pain during exercise",
            ["N", "Y"],
            format_func=lambda x: "Yes" if x == "Y" else "No",
        )
        oldpeak = st.slider("Oldpeak (ST depression)", 0.0, 6.0, 1.0, step=0.1)

    submitted = st.form_submit_button("Check my risk")

if submitted:
    loader = st.empty()
    loader.markdown(
        '<div class="loader-wrap"><div class="loader"></div>'
        '<div class="loader-text">Analysing your details...</div></div>',
        unsafe_allow_html=True,
    )
    time.sleep(1.2)

    raw_input = {
        "Age": age,
        "RestingBP": resting_bp,
        "Cholesterol": cholesterol,
        "FastingBS": fasting_bs,
        "MaxHR": max_hr,
        "Oldpeak": oldpeak,
        "Sex_" + sex: 1,
        "ChestPainType_" + chest_pain: 1,
        "RestingECG_" + resting_ecg: 1,
        "ExerciseAngina_" + exercise_angina: 1,
        "ST_Slope_" + st_slope: 1,
    }

    input_df = pd.DataFrame([raw_input])

    for col in expected_columns:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[expected_columns]

    scaled_input = scaler.transform(input_df)
    prediction = model.predict(scaled_input)[0]

    try:
        risk_pct = float(model.predict_proba(scaled_input)[0][1]) * 100
    except Exception:
        risk_pct = None

    loader.empty()

    if prediction == 1:
        css, title = "high", "Higher risk of heart disease"
        msg = "Your inputs resemble patients who were diagnosed with heart disease. Consider booking a check-up with a doctor."
    else:
        css, title = "low", "Lower risk of heart disease"
        msg = "Your inputs resemble patients without heart disease. Keep up healthy habits and regular check-ups."

    bar_html = ""
    if risk_pct is not None:
        bar_html = f"""
        <div class="bar-wrap"><div class="bar" style="width:{risk_pct:.0f}%"></div></div>
        <div class="bar-label">Model-estimated risk score: {risk_pct:.0f}%</div>
        """

    st.markdown(
        f"""
        <div class="result {css}">
            <h3>{title}</h3>
            <p>{msg}</p>
            {bar_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    '<div class="disclaimer" style="text-align:center;">This is a machine-learning estimate for learning purposes, '
    "not a medical diagnosis.</div>",
    unsafe_allow_html=True,
)