from sklearn.ensemble import IsolationForest
import numpy as np

def train_model(data, contamination=0.05):
    data = np.array(data).reshape(-1, 1)
    model = IsolationForest(
        contamination=contamination,
        random_state=42,
        n_estimators=150,      
        max_samples='auto'
    )
    model.fit(data)
    return model

def classify_anomaly(signal_value, mean_val, std_val):
    """
    Context-based labeling using Z-Score logic.
    """
    z_score = (signal_value - mean_val) / (std_val + 1e-6)
    if z_score > 3.0: 
        return "Solar Flare (Extreme Peak)"
    elif z_score > 2.0:
        return "Satellite Interference"
    elif z_score < -2.5:
        return "Signal Dropout / Deep Space Void"
    elif abs(z_score) > 1.5:
        return "Equipment Malfunction (Unstable Pulse)"
    else:
        return "Atmospheric Noise"

def detect_anomalies(model, data):
    data_reshaped = np.array(data).reshape(-1, 1)
    mean_val = np.mean(data)
    std_val = np.std(data)
    
    predictions = model.predict(data_reshaped)
    scores = model.decision_function(data_reshaped)
    
    
    predictions = np.array(predictions)
    smoothed = predictions.copy()
    for i in range(1, len(predictions) - 1):
        if predictions[i] == -1:
            if predictions[i-1] != -1 and predictions[i+1] != -1:
                smoothed[i] = 1
    predictions = smoothed

    anomaly_details = []
    for i in range(len(predictions)):
        if predictions[i] == -1:
           
            if abs(scores[i]) < 0.02: 
                predictions[i] = 1 
                continue
            
            a_type = classify_anomaly(data[i], mean_val, std_val)
            conf_val = min(max(abs(scores[i]) * 200, 75.0), 99.9)
            
            anomaly_details.append({
                "index": i,
                "type": a_type,
                "confidence": round(conf_val, 2)
            })
            
    return predictions, anomaly_details

def run_anomaly_detection(data, contamination=0.05):
    """
    CRITICAL FIX: Returns 3 values to match app.py expectation.
    """
    model = train_model(data, contamination)
    predictions, details = detect_anomalies(model, data) 
    
    
    return model, predictions, details