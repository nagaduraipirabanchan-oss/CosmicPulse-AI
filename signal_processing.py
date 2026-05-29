import numpy as np
from scipy.signal import savgol_filter, butter, filtfilt

def butter_lowpass_filter(data, cutoff=0.3, fs=1.0, order=5):
    """
    Advanced Noise Reduction: Removes high-frequency jitter.
    """
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

def clean_signal(signal):
    """
    Optimized Signal Cleaning using Savitzky-Golay and Butterworth filtering.
    """
    signal = np.array(signal)
    
    if len(signal) < 11:
        return signal

    signal = butter_lowpass_filter(signal)

    
    window = min(len(signal) // 3 * 2 + 1, 31)
    if window % 2 == 0: window += 1 
    
    if window < 5:
        return signal

   
    return savgol_filter(signal, window_length=window, polyorder=3)

def normalize_signal(signal):
    signal = np.array(signal)

    min_val = np.min(signal)
    max_val = np.max(signal)

    if max_val - min_val == 0:
        return signal

    return (signal - min_val) / (max_val - min_val)

def compute_fft(signal):
    signal = np.array(signal)
    
    
    signal = signal - np.mean(signal)

    fft = np.fft.fft(signal)
    freq = np.fft.fftfreq(len(signal))

    return freq, np.abs(fft)

def process_signal(signal):
    """
    Advanced Signal Pipeline: Clean -> Normalize -> Frequency Domain Analysis
    """
    cleaned = clean_signal(signal)
    normalized = normalize_signal(cleaned)
    freq, fft_values = compute_fft(normalized)

    return {
        "cleaned": cleaned,
        "normalized": normalized,
        "freq": freq,
        "fft": fft_values
    }