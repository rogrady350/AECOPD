import pandas as pd
import os

#Config
INPUT_PATH = "data/simulated_patient_day1.csv"
OUTPUT_PATH = "data/filtered_jump_points.csv"

#Constants
PATIENT_ID = 1
LABEL = 0 #0: no AECOPD, 1:AECOPD
THRESHOLD = 0.5 #50% change

#load orginal data
df = pd.read_csv(INPUT_PATH) #load CSV into a DataFrame. holds all original  readings
columns_to_check = df.columns[1:] #skip timestamp (1st column)

filtered_rows = [] #array to hold filtered data

#loop through each attribute column
for col in columns_to_check:
    for i in range(len(df)-1):
        curr_val = df.at[i, col]
        next_val = df.at[i+1, col]

        #skip if either value is 0 to avoid division by zero
        if curr_val == 0 or next_val == 0:
            continue

        #calculate relative change
        change = abs(curr_val - next_val) / abs(curr_val)

        if change > THRESHOLD:
            filtered_rows.append({
                "patient_id": PATIENT_ID,
                "label": LABEL,
                "timestamp": df.at[i, "timestamp"],
                "event_type": col,
                "event_value": curr_val
            })

#create output DataFrame
filtered_df = pd.DataFrame(filtered_rows)

#save to csv
filtered_df.to_csv(OUTPUT_PATH, index=False) #holds only jump points
print(f"Saved filtered jump points to {OUTPUT_PATH}")