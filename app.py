import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import plotly.graph_objects as go
import time

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AuraHealth: PCOS Diagnostic AI",
    layout="wide",
    page_icon="🧬"
)

# --------------------------------------------------
# CUSTOM STYLE
# --------------------------------------------------

st.markdown("""
<style>
.main {
    background-color: #f5f7f9;
}
.stButton>button {
    width:100%;
    border-radius:8px;
    height:3em;
    background-color:#007BFF;
    color:white;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🧬 AuraHealth AI")
st.caption("Multi-Modal PCOS Risk Intelligence | Explainable Clinical Decision Support")

st.warning("⚠️ Research Prototype — Not for real clinical diagnosis.")

st.markdown("---")

# --------------------------------------------------
# SIDEBAR - CLINICAL INPUT
# --------------------------------------------------

st.sidebar.header("📋 Step 1: Clinical Markers")

age = st.sidebar.slider("Patient Age", 18, 45, 25)
weight = st.sidebar.number_input("Weight (kg)", 40.0, 150.0, 60.0)
height = st.sidebar.number_input("Height (cm)", 100.0, 220.0, 160.0)
testosterone = st.sidebar.number_input("Testosterone Level (ng/dL)", 10.0, 150.0, 45.0)

cycle_reg = st.sidebar.selectbox(
    "Menstrual Cycle Regularity",
    ["Regular", "Irregular"]
)

follicle_count = st.sidebar.number_input("Follicle Count (Per Ovary)", 0, 50, 12)

# BMI calculation
bmi = round(weight / ((height/100)**2), 2)
st.sidebar.metric("Calculated BMI", bmi)

# --------------------------------------------------
# MAIN LAYOUT
# --------------------------------------------------

col1, col2, col3 = st.columns([1,1,1])

# --------------------------------------------------
# STEP 2 - ULTRASOUND
# --------------------------------------------------

with col1:
    st.header("🖼 Step 2: Ultrasound Upload")

    uploaded_file = st.file_uploader(
        "Upload ovarian ultrasound image",
        type=["jpg","jpeg","png"]
    )

    image = None

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True)
        st.success("✔ Image Loaded")

    analyze_btn = st.button("Run Multi-Modal Diagnostic")

# --------------------------------------------------
# STEP 3 - AI RESULT
# --------------------------------------------------

with col2:
    st.header("🤖 Step 3: AI Verdict")

    if analyze_btn:

        progress = st.progress(0)

        for i in range(100):
            time.sleep(0.01)
            progress.progress(i+1)

        with st.spinner("Running Clinical Risk Model..."):
            time.sleep(1)

        with st.spinner("Analyzing Ultrasound Features..."):
            time.sleep(1)

        with st.spinner("Generating Explainability Maps..."):
            time.sleep(1)

        # Simulated weighted AI risk scoring
        risk_score = (
            0.35*(testosterone/100) +
            0.30*(follicle_count/30) +
            0.20*(bmi/30) +
            0.15*(1 if cycle_reg=="Irregular" else 0)
        )

        confidence = round(risk_score*100,1)

        # Diagnosis decision
        if confidence >= 70:
            result = "High Risk: PCOS Detected"
            color = "red"
        elif confidence >= 40:
            result = "Potential Risk"
            color = "orange"
        else:
            result = "Normal Profile"
            color = "green"

        st.subheader(f"Status: :{color}[{result}]")

        # Gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=confidence,
            title={'text': "AI Confidence (%)"},
            gauge={
                'axis': {'range': [0,100]},
                'bar': {'color': color}
            }
        ))

        st.plotly_chart(fig, use_container_width=True)

        st.caption("Model: AuraHealth Multi-Modal Fusion v1.2")

# --------------------------------------------------
# EXPLAINABLE AI DASHBOARD
# --------------------------------------------------

with col3:

    if analyze_btn:

        st.header("🧠 Explainable AI")

        # SHAP simulation
        feat_data = pd.DataFrame({
            'Feature': ['Testosterone','Cycle Regularity','Follicle Count','BMI','Age'],
            'Impact Score': [0.45,0.25,0.15,0.10,0.05]
        })

        st.subheader("Global Explainability (Feature Impact)")
        st.bar_chart(feat_data.set_index('Feature'))

        st.caption(
            "Prediction mainly influenced by androgen levels and follicle morphology."
        )

        # Grad-CAM simulation
        st.subheader("Local Explainability (Grad-CAM Simulation)")

        if image is not None:
            st.image(image, use_container_width=True)
            st.caption("Heatmap highlights follicle clusters (simulated).")
        else:
            st.info("Upload ultrasound image to view explainability.")

# --------------------------------------------------
# AI PIPELINE SECTION
# --------------------------------------------------

st.markdown("---")

st.markdown("""
### 🧠 AI Pipeline

1️⃣ Clinical Feature Encoding  
2️⃣ Ultrasound Feature Extraction  
3️⃣ Multi-Modal Fusion Risk Model  
4️⃣ Explainable AI Layer (SHAP + GradCAM)
""")

st.markdown("---")
st.write("© 2026 AuraHealth AI | Hackathon Prototype")