import streamlit as st
import pandas as pd
import time

# --- UI Configuration ---
st.set_page_config(
    page_title="Intelligent Network Anomaly Detector", 
    page_icon="🛡️", 
    layout="wide"
)

st.title("🛡️ Real-Time Network Traffic Anomaly Dashboard")
st.markdown("Monitoring live packet sizes and statistical deviations (Z-Scores).")

# --- Dynamic Placeholders ---
metrics_placeholder = st.empty()
chart_placeholder = st.empty()
table_placeholder = st.empty()

def fetch_live_data():
    """Reads the latest data from the CSV file."""
    try:
        df = pd.read_csv("traffic_log.csv")
        return df
    except Exception:
        return pd.DataFrame(columns=["Time", "Source_IP", "Size", "Z_Score", "Is_Anomaly"])

# --- Main Dashboard Loop ---
while True:
    df = fetch_live_data()
    
    if not df.empty:
        # Isolate anomalous traffic
        anomalies_df = df[df["Is_Anomaly"] == "YES"]
        
        # 1. Update Top Metrics
        with metrics_placeholder.container():
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Packets Analyzed", len(df))
            col2.metric("Anomalies Detected", len(anomalies_df))
            
            threat_level = "🚨 HIGH" if len(anomalies_df) > 0 else "✅ LOW (Normal)"
            col3.metric("Current Threat Level", threat_level)
            
        # 2. Update Live Charts
        with chart_placeholder.container():
            st.subheader("Live Packet Size Trend")
            recent_data = df.tail(50).reset_index()
            st.line_chart(recent_data, x="Time", y="Size", color="#1f77b4")
            
        # 3. Update Anomaly Log Table
        with table_placeholder.container():
            st.subheader("Recent Security Alerts (Anomalies)")
            if not anomalies_df.empty:
                st.dataframe(
                    anomalies_df.tail(10).style.highlight_max(axis=0, color="#ff4c4c"),
                    use_container_width=True
                )
            else:
                st.success("No anomalies detected yet. Baseline is stable.")
    else:
        st.warning("Waiting for data... Please ensure your Scapy sniffer script is running.")

    # Refresh the dashboard every 2 seconds
    time.sleep(2)