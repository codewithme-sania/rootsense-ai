
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="RootSense AI",
    page_icon="🌱",
    layout="wide"
)

# ---------------- CUSTOM DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background-color: #f4f8f4;
}
.block-container {
    padding-top: 1.5rem;
}
.hero {
    background: linear-gradient(120deg,#103d2a,#16834b);
    padding: 30px;
    border-radius: 18px;
    color: white;
}
.hero h1 {
    color: white;
    font-size: 42px;
}
.hero p {
    color: #e0f3e7;
}
.metric {
    background: white;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #dce9df;
}
.metric h2 {
    color: #16834b;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🌱 RootSense AI")
st.sidebar.caption("AG-02 | Underground Soil Intelligence")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard Overview",
        "Live Soil Monitoring",
        "Root Intelligence",
        "AI Insights",
        "Alerts & Recommendations",
        "Data Analytics",
        "Sensor Management"
    ]
)

crop = st.sidebar.selectbox(
    "Select Crop",
    ["Tomato", "Maize", "Wheat", "Groundnut", "Chilli"]
)

field = st.sidebar.text_input("Field Name", "Demo Field A")

variation = st.sidebar.slider(
    "Simulation variation",
    0, 15, 5
)

# ---------------- SENSOR DATA ----------------
rng = np.random.default_rng()

depths = [10, 20, 30, 40]

data = pd.DataFrame({
    "Depth (cm)": depths,
    "Moisture (%)": [
        38 + rng.normal(0, variation),
        32 + rng.normal(0, variation),
        26 + rng.normal(0, variation),
        22 + rng.normal(0, variation)
    ],
    "Temperature (°C)": [
        28 + rng.normal(0, variation/8),
        26 + rng.normal(0, variation/8),
        24 + rng.normal(0, variation/8),
        23 + rng.normal(0, variation/8)
    ],
    "Compaction Index": [
        22 + rng.normal(0, variation),
        30 + rng.normal(0, variation),
        43 + rng.normal(0, variation),
        51 + rng.normal(0, variation)
    ],
    "Root Zone Signal": [
        80 + rng.normal(0, variation),
        85 + rng.normal(0, variation),
        70 + rng.normal(0, variation),
        55 + rng.normal(0, variation)
    ]
})

data["Moisture (%)"] = data["Moisture (%)"].clip(5, 65)
data["Compaction Index"] = data["Compaction Index"].clip(0, 100)
data["Root Zone Signal"] = data["Root Zone Signal"].clip(0, 100)

avg_moisture = data["Moisture (%)"].mean()
avg_temp = data["Temperature (°C)"].mean()
avg_compaction = data["Compaction Index"].mean()
avg_root = data["Root Zone Signal"].mean()

# Demonstration health indicator, not a validated agronomic score
health = np.clip(
    100
    - abs(avg_moisture - 30) * 2
    - max(avg_compaction - 25, 0) * 0.5
    - abs(avg_temp - 25) * 3
    + (avg_root - 70) * 0.15,
    0, 100
)

# ---------------- HEADER ----------------
st.markdown(f"""
<div class="hero">
    <h1>🌱 RootSense AI</h1>
    <h3>Underground Soil Intelligence & Root Monitoring System</h3>
    <p>AG-02 Hackathon Challenge | Smart Agriculture Monitoring</p>
    <p>Field: {field} | Crop: {crop}</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------------- DASHBOARD OVERVIEW ----------------
if page == "Dashboard Overview":

    st.title("Dashboard Overview")

    st.caption(
        "Underground soil monitoring and intelligent root-zone analysis"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Soil Health Index", f"{health:.0f}/100")

    with c2:
        st.metric("Average Moisture", f"{avg_moisture:.1f}%")

    with c3:
        st.metric("Soil Temperature", f"{avg_temp:.1f} °C")

    with c4:
        st.metric("Compaction Index", f"{avg_compaction:.1f}")

    st.subheader("Underground Moisture Distribution")

    fig = px.line(
        data,
        x="Moisture (%)",
        y="Depth (cm)",
        markers=True,
        title="Soil Moisture at Different Depths"
    )

    fig.update_yaxes(autorange="reversed")

    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Soil Temperature")

        fig = px.bar(
            data,
            x="Depth (cm)",
            y="Temperature (°C)",
            color="Temperature (°C)"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Soil Compaction")

        fig = px.bar(
            data,
            x="Depth (cm)",
            y="Compaction Index",
            color="Compaction Index"
        )

        st.plotly_chart(fig, use_container_width=True)

# ---------------- LIVE MONITORING ----------------
elif page == "Live Soil Monitoring":

    st.title("📡 Live Soil Monitoring")

    st.info("Current prototype uses simulated sensor readings.")

    st.dataframe(data, use_container_width=True)

    selected = st.selectbox("Select Depth", depths)

    reading = data[data["Depth (cm)"] == selected].iloc[0]

    a, b, c = st.columns(3)

    a.metric("Moisture", f"{reading['Moisture (%)']:.1f}%")
    b.metric("Temperature", f"{reading['Temperature (°C)']:.1f} °C")
    c.metric("Compaction", f"{reading['Compaction Index']:.1f}")

# ---------------- ROOT INTELLIGENCE ----------------
elif page == "Root Intelligence":

    st.title("🌿 Root Zone Intelligence")

    st.write(
        "Analyze underground root-zone conditions at multiple soil depths."
    )

    fig = px.bar(
        data,
        x="Depth (cm)",
        y="Root Zone Signal",
        color="Root Zone Signal",
        title="Root-Zone Signal by Depth"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.metric("Average Root-Zone Signal", f"{avg_root:.1f}/100")

    st.warning(
        "Root-zone signal is a demonstration proxy, not a direct measurement "
        "of root growth. Actual root development requires validated sensing."
    )

# ---------------- AI INSIGHTS ----------------
elif page == "AI Insights":

    st.title("🤖 AI Soil Intelligence")

    st.write("Automated observations based on sensor readings.")

    if avg_moisture < 20:
        st.error("Low soil moisture detected. Check irrigation.")
    elif avg_moisture > 45:
        st.warning("High moisture detected. Check soil drainage.")
    else:
        st.success("Moisture is within the prototype's target range.")

    if avg_compaction > 45:
        st.error("High relative compaction detected.")
    else:
        st.success("No high-compaction alert from the current readings.")

    if avg_temp > 32:
        st.error("High root-zone temperature detected.")
    else:
        st.success("No high-temperature alert from current readings.")

    st.subheader("Soil Health Indicator")

    st.progress(int(health))

    st.write(f"Current prototype indicator: {health:.1f}/100")

# ---------------- ALERTS ----------------
elif page == "Alerts & Recommendations":

    st.title("🚨 Alerts & Recommendations")

    if avg_moisture < 20:
        st.error("LOW MOISTURE: Inspect irrigation and deeper soil layers.")

    if avg_moisture > 45:
        st.warning("HIGH MOISTURE: Inspect drainage.")

    if avg_compaction > 45:
        st.error("COMPACTION: Investigate soil resistance.")

    if avg_temp > 32:
        st.error("TEMPERATURE: Inspect heat stress conditions.")

    st.subheader("Recommended Actions")

    st.write("1. Monitor moisture at different depths.")
    st.write("2. Check water distribution around the root zone.")
    st.write("3. Validate compaction using a calibrated penetrometer.")
    st.write("4. Compare sensor readings over multiple days.")
    st.write("5. Inspect root development using an appropriate root observation method.")

# ---------------- ANALYTICS ----------------
elif page == "Data Analytics":

    st.title("📊 Soil Data Analytics")

    fig = px.line(
        data,
        x="Depth (cm)",
        y=["Moisture (%)", "Temperature (°C)"],
        markers=True,
        title="Soil Condition Analysis"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Sensor Data")

    st.dataframe(data, use_container_width=True)

    csv = data.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Soil Data CSV",
        csv,
        "rootsense_data.csv",
        "text/csv"
    )

# ---------------- SENSOR MANAGEMENT ----------------
elif page == "Sensor Management":

    st.title("🔌 Sensor Management")

    st.write("Prototype sensor network overview")

    sensors = pd.DataFrame({
        "Sensor": [
            "Soil Moisture Sensor",
            "Temperature Sensor",
            "Compaction Sensor",
            "Root-Zone Monitoring"
        ],
        "Measurement": [
            "Moisture percentage",
            "Temperature",
            "Relative soil resistance",
            "Root-zone proxy"
        ],
        "Status": [
            "Simulation",
            "Simulation",
            "Simulation",
            "Simulation"
        ]
    })

    st.dataframe(sensors, use_container_width=True)

    st.warning(
        "Hardware is not connected yet. These are simulated readings, "
        "not live ESP32 measurements."
    )

# ---------------- FOOTER ----------------
st.markdown("---")

st.markdown("""
<center>
<h4>🌱 RootSense AI</h4>
<p>Underground Soil Intelligence & Root Monitoring System</p>
<p>AG-02 | Smart Agriculture Hackathon Prototype</p>
</center>
""", unsafe_allow_html=True)
