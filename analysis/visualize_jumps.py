#display graphs of data

#plot patient ventilator data
import pandas as pd
import matplotlib.pyplot as plt

#LOAD DATA
#Files
input_csv = "data/simulated_patient_day1.csv"
jump_csv = "data/filtered_jump_points.csv"

#load original (full) time-series data
df_full = pd.read_csv(input_csv)
df_full["timestamp"] = pd.to_datetime(df_full["timestamp"]) #convert to datetime from text for sorting


#load jump point data
df_jumps = pd.read_csv(jump_csv)
df_jumps["timestamp"] = pd.to_datetime(df_jumps["timestamp"]) #convert to datetime

#USER INPUT
#Available signal columns
available_signals = ["flow", "spo2", "pressure", "leak", "resrate", "tidalvolume", "minutevent"]
print("Available signals:", ", ".join(available_signals))

#Prompt user
user_input = input("Enter signals to plot (comma-separated): ")
raw_signals = user_input.split(",") #split input string into list
signals = []                        #list to store signals

#loop through each entered signal
for signal in raw_signals:
    cleaned_signal = signal.strip() #remove extra spaces

    #add valid signals
    if cleaned_signal in available_signals:
        signals.append(cleaned_signal)

    #handle no valid entries
    if len(signals) == 0:
        print("No valid signals entered. Exiting")
        exit()


#SHARED GLOBAL DATA
timestamps = df_full["timestamp"] #timestamp column from original data CSV (x-axis)

#dictionary of signal values (excluding timestamp)
signal_values_dict = {}
for column in df_full.columns:
    if column!= "timestamp":
        signal_values_dict[column] = df_full[column]

#dictionary of jump points by signal
jump_point_dict = {}
unique_signals = df_jumps["event_type"].unique()

#for each signal, filter to show only rows with jumps
for sig in unique_signals:
    sig_jumps =df_jumps[df_jumps["event_type"] == sig]
    jump_point_dict[sig] = {
        "timestamps": sig_jumps["timestamp"],
        "values": sig_jumps["event_value"]
    }

#CREATE SUBPLOTS
num_signals = len(signals) #number of signals in list of signals

#fig: full canvas, axs: list of subplots for each signal. 1 row per signal, 12x3*num_signals, aligned by timestamp
fig, axs = plt.subplots(nrows=num_signals, figsize=(12, 3*num_signals), sharex=True)

#set axs as a list if only 1 signal for consistency
if num_signals == 1:
    axs = [axs]

#loop through each signal and plot values
for i in range(num_signals):
    signal_name = signals[i]
    signal_values = signal_values_dict[signal_name]

    #plot the full signal line
    axs[i].plot(timestamps, signal_values, label=f"{signal_name} signal", linewidth=1.5) #draw smooth line through points

    #overlay jump points, if available
    jump_data = jump_point_dict.get(signal_name)
    if jump_data:
        axs[i]. scatter(jump_data["timestamps"], jump_data["values"],
                        color='red', label='Jump Points', zorder=5)
    
    #format subplot
    axs[i].set_ylabel(signal_name.capitalize())
    axs[i].legend()   #display legend
    axs[i].grid(True) #add gridlines

#FINAL PLOT FORMATTING
plt.xlabel("Timestamp")
plt.suptitle("Ventilator Signals with Jump Points")
plt.tight_layout()      #auto adjust spacing
plt.xticks(rotation=45) #rotate x-axis labels to prevent crowding
plt.show()              #display