import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense


def predict_signal(data):
    """
    Design: Process signal for anomalies.
    This acts as the interface between raw data and the LSTM model.
    """
   
    predictions = data * 1.2  
    return predictions

def create_sequences(data, seq_length=10):
    sequences = []
    for i in range(len(data) - seq_length):
        sequences.append(data[i:i+seq_length])
    return np.array(sequences)

def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(50, return_sequences=False, input_shape=input_shape))
    model.add(Dense(1))
    
    model.compile(optimizer='adam', loss='mse')
    return model

def train_lstm(data):
    sequences = create_sequences(data)
    
    X = sequences[:, :-1]
    y = sequences[:, -1]
    
    model = build_lstm_model((X.shape[1], 1))
    model.fit(X, y, epochs=5, batch_size=32)
    
    return model

def detect_lstm_anomalies(model, data):
    sequences = create_sequences(data)
    
    X = sequences[:, :-1]
    y_true = sequences[:, -1]
    
    y_pred = model.predict(X)
    
    error = np.abs(y_pred.flatten() - y_true.flatten())
    
    threshold = np.mean(error) + 2*np.std(error)
    
    anomalies = error > threshold
    
    return anomalies