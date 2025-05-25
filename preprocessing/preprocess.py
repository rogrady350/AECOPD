#create simulated patient data CSV file
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

#Config (used research paper data)
num_secs = 60 #simulate 1 min of data
samples_per_sec = 5 #data sampled at 5Hz
tot_samples = num_secs * samples_per_sec
start_time = datetime(2025, 1, 1, 8, 0, 0) #Jan 1, 2025, 8:00:00

#generate timestamps
timestamps = []

#loop over number of samples
for i in range(tot_samples):
    time_offset = timedelta(seconds = i/samples_per_sec) #time per sample
    timestamp = start_time + time_offset
    timestamps.append(timestamp) #add to list

#simulate signals and jump points
#base: central/ave value of signal, noise: random variation, jump_magnitude: simulate a jump point (big sudden change)
def simulate_signal(base=50, noise=3, jump_magnitude=20):
    signal = np.random.normal(base, noise, tot_samples) #create realistic-looking waveforms

    #add 3 artificial jumps. choose 3 random starting indices away from edges
    jump_indices = np.random.choice(range(100, tot_samples - 100), size=3, replace=False)

    #loop through each selected index
    for index in jump_indices:
        jump_direction = np.random.choice([-1, 1]) #choose direction
        jump_value = jump_direction * jump_magnitude #total jump change
        signal[index : index+10] += jump_value #simulate sustained change, add jump to next 10 values

    return signal

#sample data
data = pd.DataFrame({
    "timestamp": timestamps,
    "flow": simulate_signal(30),                   #standard flow of air into lungs. norm: 30-40 
    "pressure": simulate_signal(10),               #air pressure delivered by ventilator. norm: ~10cmH20
    "spo2": simulate_signal(95, noise=0.5),        #blood oxygen saturation. norm: 94-100%
    "resrate": simulate_signal(16, noise=0.5),     #respiratory rate (breaths/min). norm: 12-20
    "tidalvolume": simulate_signal(450, noise=10), #volume of air exhaled/breath. norm ~450 mL/breath
    "minutevent": simulate_signal(8, noise=0.3),   #tot vol of air/min. norm: ~6-10 L/min
    "leak": simulate_signal(2, noise=0.2)          #air leakage from ventilator mask/system. norm: small(~0-3)
})

#save to CSV
os.makedirs("data", exist_ok=True) #create dir if it doesnt exist
csv_path = "data/simulated_patient_day1.csv"
data.to_csv(csv_path, index=False)
print(f"saved simulated data to {csv_path}")