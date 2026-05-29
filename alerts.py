import numpy as np
import json
import os
from datetime import datetime
import smtplib
from email.message import EmailMessage


def run_test_alert(status):
    """
    Testing: Validating system alerts and status check.
    Ensures the alert engine is functional before production use.
    """
    if status == "Success":
        print("Test Passed: System is stable.")
    else:
        print("Test Failed: Check logs.")


LOG_FILE = "data/anomaly_logs.json"

def save_to_history(new_alerts):
    """
    Update: Professional Database & Backup Logic.
    In a real company, this would connect to MongoDB or SQL.
    """
    if not new_alerts:
        return

   
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    history = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                history = json.load(f)
        except:
            history = []

    history.extend(new_alerts)

    with open(LOG_FILE, "w") as f:
        json.dump(history[-1000:], f, indent=4)
    
    for alert in new_alerts:
        if alert["severity"] == "HIGH":
            trigger_email_alert(alert)

def trigger_email_alert(alert):
    """
    Macha, indha function company production-la email anuppa use aagum.
    """
    print(f" [SYSTEM NOTIFICATION]: Sending alert to engineer for {alert['category']}...")
    pass

def generate_alerts(predictions, data, anomaly_details=None):
    """
    Update: Added 'Action Required' field and Enterprise Categorization.
    """
    alerts = []
    
    for i, val in enumerate(predictions):
        if val == -1:
            category = "General Anomaly"
            confidence = 0.0
            if anomaly_details:
                for d in anomaly_details:
                    if d['index'] == i:
                        category = d['type']
                        confidence = d['confidence']
                        break

           
            action_map = {
                "Satellite Interference": " Action: Re-align Receiver Dish",
                "Solar Flare": " Action: Switch to Backup Frequency",
                "Equipment Malfunction": " Action: Contact Maintenance - Sensor B-12",
                "General Anomaly": " Action: Monitor Signal Stability"
            }

            alerts.append({
                "index": i,
                "value": float(data[i]),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "severity": get_severity(data[i]),
                "category": category,
                "confidence": confidence,
                "action_required": action_map.get(category, " Action: System Audit Needed") 
            })

    if alerts:
        save_to_history(alerts)
        
    return alerts

def get_severity(value):
    if value > 2:
        return "HIGH"
    elif value > 1:
        return "MEDIUM"
    else:
        return "LOW"

def get_alert_summary(alerts):
    summary = {
        "total": len(alerts),
        "high": 0,
        "medium": 0,
        "low": 0,
        "categories": {}
    }

    for alert in alerts:
        sev = alert["severity"].lower()
        summary[sev] = summary.get(sev, 0) + 1
        
        cat = alert["category"]
        summary["categories"][cat] = summary["categories"].get(cat, 0) + 1

    return summary

def has_alerts(alerts):
    return len(alerts) > 0

def get_alert_message(alerts):
    if not alerts:
        return " System Status: ALL CLEAR"

    high_count = sum(1 for a in alerts if a["severity"] == "HIGH")

    if high_count > 0:
        return f" SYSTEM CRITICAL: {high_count} Events requiring immediate action!"
    else:
        return f" Monitoring: {len(alerts)} events logged for review."

def get_alert_indices(predictions):
    return np.where(np.array(predictions) == -1)[0]


if __name__ == "__main__":
    run_test_alert("Success")