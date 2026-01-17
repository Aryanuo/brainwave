import streamlit as st
import pandas as pd
import requests
import time
import plotly.express as px

from api_client import start_workflow, poll_execution_once

BACKEND_LOG_API = "http://localhost:5000/logs"

st.set_page_config(
    page_title="Real-Time Cyber Threat Detection Dashboard",
    layout="wide"
)

with st.sidebar:
    st.header("Settings")
    auto_refresh = st.toggle("🔄 Live Update", value=True)
    refresh_interval = st.slider("Refresh interval (seconds)", 2, 10, 5)

st.title("🛡️ Real-Time Cyber Threat Detection Dashboard")

if "execution_id" not in st.session_state:
    st.session_state.execution_id = None

try:
    response = requests.get(BACKEND_LOG_API, timeout=5)
    logs = response.json()
except Exception:
    logs = [
        {"received_at": "00:25:20", "attack_type": "BENIGN", "threat_score": 0.099, "risk_label": "Benign"},
        {"received_at": "00:25:27", "attack_type": "UDP Flood", "threat_score": 0.404, "risk_label": "Watchlist"},
        {"received_at": "00:25:34", "attack_type": "BENIGN", "threat_score": 0.1, "risk_label": "Benign"}
    ]

df = pd.DataFrame(logs)

# --- KEY FIX: HANDLE EMPTY DATA AND COLUMN NAMES ---
if not df.empty:
    
    latest = df.iloc[-1]
    current_score = latest.get("threat_score", 0)
    current_label = latest.get("risk_label", "Unknown")

    if current_score >= 0.7:
        st.error(f"🚨 THREAT DETECTED | {latest.get('attack_type')} | Score: {current_score:.3f}")
    elif current_score >= 0.4:
        st.warning(f"⚠️ ATTACK | Potential Anomaly | Score: {current_score:.3f}")
    else:
        st.success(f"✅ System Normal | Score: {current_score:.3f}")

    st.subheader("📜 Live Network Logs")
    cols_to_show = [c for c in ["received_at", "attack_type", "threat_score", "risk_label"] if c in df.columns]
    
    st.dataframe(
        df[cols_to_show][::-1],
        use_container_width=True,
        height=250,
        column_config={
            "received_at": "Timestamp",
            "attack_type": "Detection",
            "threat_score": st.column_config.NumberColumn("Risk Score", format="%.3f"),
            "risk_label": "Status"
        }
    )

    # --- CHARTS ---
    st.subheader("📊 Threat Analytics")
    c1, c2 = st.columns([2, 1])

    with c1:
        st.write("📈 Threat Score Trend")
        line_fig = px.line(df, x="received_at", y="threat_score", markers=True, 
                           labels={"threat_score": "Score", "received_at": "Time"})
        line_fig.update_layout(height=350, template="plotly_dark")
        st.plotly_chart(line_fig, use_container_width=True)

    with c2:
        st.write("🧠 Distribution")
        pie_data = df["attack_type"].value_counts().reset_index()
        pie_data.columns = ["type", "count"]
        pie_fig = px.pie(pie_data, names="type", values="count", hole=0.4)
        pie_fig.update_layout(height=350, template="plotly_dark")
        st.plotly_chart(pie_fig, use_container_width=True)
else:
    st.info("📡 Waiting for data from Backend API...")

# --- ON-DEMAND SECTION ---
st.divider()
st.subheader("🤖 AI Orchestration (On-Demand)")
c1, c2, c3 = st.columns(3)
with c1:
    f_logins = st.number_input("Failed Logins", value=21)
with c2:
    r_rate = st.number_input("Request Rate", value=40)
with c3:
    d_size = st.number_input("Data Size", value=909)

if st.button("Analyze via On-Demand"):
    start = start_workflow(f_logins, r_rate, d_size)
    if "executionID" in start:
        st.session_state.execution_id = start["executionID"]
        st.info(f"Workflow started: {st.session_state.execution_id}")

# --- POLLING ---
if st.session_state.execution_id:
    result = poll_execution_once(st.session_state.execution_id)
    status = result.get("status", "").upper()

    if status == "COMPLETED":
        st.success("✅ On-Demand analysis completed")
        st.json(result.get("output", {}))
        st.session_state.execution_id = None
    elif status in ["EXECUTING", "STARTED", "PENDING"]:
        st.warning(f"⏳ On-Demand running ({status})...")
        time.sleep(2)
        st.rerun()
    else:
        st.error(f"❌ Execution Status: {status}")
        st.session_state.execution_id = None

# --- AUTO REFRESH ---
if auto_refresh and not st.session_state.execution_id:
    time.sleep(0.5)
    st.rerun()
