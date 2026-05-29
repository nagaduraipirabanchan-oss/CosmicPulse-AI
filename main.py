from utils.data_loader import load_data
from utils.signal_processing import clean_signal, normalize_signal
from models.lstm_model import train_lstm, detect_lstm_anomalies

data = load_data("data/sample_signal.csv")

signal = data["signal"].values

cleaned = clean_signal(signal)
normalized = normalize_signal(cleaned)

normalized = normalized.reshape(-1, 1)


model = train_lstm(normalized)


anomalies = detect_lstm_anomalies(model, normalized)


result = [0]*10 + anomalies.tolist()

data['anomaly'] = result


data.to_csv("data/output.csv", index=False)

print("LSTM Detection Done ")