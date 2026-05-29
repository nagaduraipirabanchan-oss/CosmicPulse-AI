import pandas as pd
import numpy as np
import time


def load_pulsar_data(file_path):
    """
    Requirement: Process the pulsar CSV dataset.
    This acts as the primary data entry point for the system.
    """
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error in base loading: {e}")
        return None

def load_data(file_path):
    try:
      
        data = load_pulsar_data(file_path)
        
       
        if data is None or data.empty:
            print(" Error: CSV file is empty.")
            return None
            
       
        data = data.select_dtypes(include=['float64', 'int64'])
        
      
        if data.isnull().values.any():
            print(" Warning: Missing values detected. Applying interpolation...")
            data = data.interpolate(method='linear').fillna(method='bfill')
            
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def get_signal(data):
    if data is None or data.empty:
        return np.array([])
    if 'target' in data.columns:
        data = data.drop(columns=['target'])
    
    
    signal = data.mean(axis=1).values
    return signal

def load_real_data():
    """
    Update: Real-time stream simulation logic.
    Instead of loading everything at once, it simulates a live pulse.
    """
    file_path = "data/pulsar.csv"
    data = load_data(file_path)

    if data is None or data.empty:
        raise ValueError(" Pulsar dataset missing or invalid")

    full_signal = get_signal(data)
    
   
    return full_signal