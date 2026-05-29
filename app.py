import sys
import os
import time
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit.components.v1 as components
import smtplib
from email.mime.text import MIMEText
from datetime import datetime


st.set_page_config(page_title="CosmicPulse AI", layout="wide", page_icon="🛰️")


def send_auto_email(alert_id, magnitude, timestamp):
    sender_email = "pprabas577@gmail.com"             # 
    receiver_email = "nagaduraipirabanchan@gmail.com" 
    
   
    password = "xbke xwru ttcb panh" 

    subject = f" CRITICAL SIGNAL DETECTED: {alert_id}"
    body = f"""
    CosmicPulse AI - Automated Security Alert
    ----------------------------------------
    Incident ID: {alert_id}
    Time: {timestamp}
    Magnitude: {magnitude}
    Status: Critical Anomaly Triggered
    
    This is an automated notification from your CosmicPulse Dashboard.
    """
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
    except Exception as e:
        print(f"Email Error: {e}")

st.markdown("""
<style>
    .stApp { background-color: #000000; color: white; }
    div.block-container { 
        background: rgba(10, 10, 10, 0.9); 
        border-radius: 15px; 
        padding: 2rem; 
        border: 1px solid rgba(255, 20, 147, 0.3); 
    }
    .incident-card { 
        background: rgba(255, 20, 147, 0.15); 
        border-left: 5px solid #FF1493; 
        padding: 12px; 
        border-radius: 8px; 
        margin-bottom: 8px; 
    }
    .critical-banner {
        background-color: #FF0000;
        color: white;
        padding: 20px;
        text-align: center;
        font-weight: bold;
        font-size: 24px;
        border-radius: 10px;
        animation: blinker 1s linear infinite;
        margin-bottom: 20px;
    }
    @keyframes blinker { 50% { opacity: 0; } }
</style>
""", unsafe_allow_html=True)


def trigger_voice():
    js = "<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('Critical signal detected'));</script>"
    components.html(js, height=0)


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from utils.data_loader import load_real_data
    from utils.signal_processing import process_signal
    from models.anomaly_model import run_anomaly_detection
except:
    def load_real_data(): return np.random.randn(500)
    def process_signal(s): return {"cleaned": s + 2}
    def run_anomaly_detection(s, contamination): return None, np.array([1 if x < 1.5 else -1 for x in s]), [{"index": 50}]


if 'incidents' not in st.session_state:
    st.session_state.incidents = []


with st.sidebar:
    st.title("CosmicPulse AI: Control Center")
    st.markdown("---")
    st.markdown("### History Analysis")
    selected_date = st.date_input("Filter Alerts by Date", datetime.now())
    
    st.markdown("### Reports")
    if st.session_state.incidents:
        df_incidents = pd.DataFrame(st.session_state.incidents)
        csv = df_incidents.to_csv(index=False).encode('utf-8')
        st.download_button(label="Download CSV Report", data=csv, file_name="CosmicPulse_Report.csv", mime='text/csv')
    
    st.markdown("---")
    sensitivity = st.slider("Sensitivity", 0.01, 0.20, 0.05)
    mute_alerts = st.toggle("Mute Audio Alerts", value=False)

    st.show_alerts = st.checkbox("Show Active Alerts", value=True)
    st.anomaly_plot = st.checkbox("Show Anomaly Plot", value=True)
    st.clean_signal = st.checkbox("Show Cleaned Signal", value=True)
    

st.title("CosmicPulse AI")
st.subheader(" Intelligent Detection & Visualization of Radio Signals")
st.markdown("---")

alert_banner_area = st.empty()
step1_metrics = st.empty()       
step2_anomaly = st.empty()       
step3_live_clean = st.empty()    
step4_wave_3d = st.empty()       
step5_map = st.empty()           
step6_alerts = st.empty()        


while True:
    s_raw = load_real_data()
    processed = process_signal(s_raw)
    c_live = processed["cleaned"]
    
    model, predictions, details = run_anomaly_detection(c_live, contamination=sensitivity)
    anom_idx = np.where(predictions == -1)[0]
    
    current_time_str = datetime.now().strftime('%H:%M:%S')
    current_date_str = datetime.now().strftime('%Y-%m-%d')
    
    
    if len(anom_idx) > 0:
        alert_banner_area.markdown('<div class="critical-banner">⚠️ CRITICAL SIGNAL DETECTED - NOTIFICATIONS DISPATCHED ⚠️</div>', unsafe_allow_html=True)
        if not mute_alerts:
            trigger_voice()
        
        for d in details[:1]: 
            uid = f"INC-{datetime.now().strftime('%M%S')}-{d['index']}"
            if not any(inc['id'] == uid for inc in st.session_state.incidents):
                val_str = f"{c_live[d['index']]:.2f}"
                st.session_state.incidents.insert(0, {"id": uid, "date": current_date_str, "time": current_time_str, "val": val_str, "status": "OPEN"})
                
               
                send_auto_email(uid, val_str, current_time_str)
    else:
        alert_banner_area.empty()

  
    with step1_metrics.container():
        st.markdown("###  Signal Overview")
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Points Processed", len(s_raw))
        k2.metric("Detected Anomalies", len(anom_idx), delta=f"{len(anom_idx)} Active")
        k3.metric("Peak Amplitude", f"{max(c_live):.2f}")
        k4.metric("Noise Floor (σ)", f"{np.std(c_live):.4f}")

  
    with step2_anomaly.container():
        st.markdown("###  Anomaly Detection Analysis")
        fig_anom = go.Figure()
        fig_anom.add_trace(go.Scatter(y=c_live, mode='lines', line=dict(color='#FF69B4', width=1.5), name="Signal"))
        fig_anom.add_trace(go.Scatter(x=anom_idx, y=c_live[anom_idx], mode='markers', marker=dict(color='white', size=8), name="Anomaly"))
        fig_anom.update_layout(template="plotly_dark", height=250, margin=dict(l=10,r=10,t=10,b=10))
        st.plotly_chart(fig_anom, use_container_width=True, key=f"anom_{time.time()}")

    
    with step3_live_clean.container():
        st.markdown("###  Live Signal & Noise Filtering")
        st.caption("Raw Data Input")
        st.line_chart(s_raw, height=100) 
        st.caption("Filtered/Cleaned Output")
        st.line_chart(c_live, height=100, color="#FF69B4") 

    
    with step4_wave_3d.container():
        st.markdown("###  3D Radio Wave Visualization")
        wave_buffer = c_live[:100]
        z_data = np.array([np.roll(wave_buffer, i) for i in range(20)]) 
        fig_3d = go.Figure(data=[go.Surface(z=z_data, colorscale='RdPu', showscale=False)]) 
        fig_3d.update_layout(template="plotly_dark", height=350, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig_3d, use_container_width=True, key=f"3d_{time.time()}")

    
    with step5_map.container():
        st.markdown("###  Live Burst Tracking Map")
        if len(anom_idx) > 0:
            map_df = pd.DataFrame({
                'lat': [11.0168, 11.1085, 11.2989, 11.4102, 11.3410],
                'lon': [76.9558, 77.3411, 77.7177, 76.6991, 76.9324],
                'intensity': [30 + (len(anom_idx)*30)] * 5
            })
        else:
            map_df = pd.DataFrame({'lat': [11.0168], 'lon': [76.9558], 'intensity': [5]})
        st.map(map_df, size='big', color="#FF1493") 

    
    with step6_alerts.container():
        st.markdown(f"###  System Alerts ({current_time_str})")
        filtered = [inc for inc in st.session_state.incidents if inc['date'] == selected_date.strftime('%Y-%m-%d')]
        if not filtered:
            st.info("Monitoring for anomalies...")
        else:
            for alert in filtered[:4]:
                st.markdown(f'<div class="incident-card"><b>CRITICAL ALERT</b> | {alert["time"]} | ID: {alert["id"]} | Mag: {alert["val"]}</div>', unsafe_allow_html=True)

    time.sleep(0.5)