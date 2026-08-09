from scapy.all import sniff, IP
import numpy as np
import csv
import time

# --- CONFIGURATION ---
# Increased threshold from 3.0 to 5.0 to drastically reduce false positives
THRESHOLD = 5.0  

# A list to hold our normal packet sizes
normal_traffic = []

# Limit memory to 100 packets to keep the program running fast and efficiently
MAX_PACKETS = 100

# Create a fresh log file and write the headers (columns) for the dashboard
with open("traffic_log.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Time", "Source_IP", "Size", "Z_Score", "Is_Anomaly"])

def intelligent_anomaly_detector(packet):
    # Check if the packet has an IP address
    if IP in packet:
        packet_size = len(packet)
        source_ip = packet[IP].src
        current_time = time.strftime("%H:%M:%S")

        # Phase 1: Build the baseline
        if len(normal_traffic) < MAX_PACKETS:
            normal_traffic.append(packet_size)
            print(f"Learning... collected {len(normal_traffic)}/{MAX_PACKETS} packets")
        
        # Phase 2: Detect Anomalies and Log Data
        else:
            mean = np.mean(normal_traffic)
            std_dev = np.std(normal_traffic)

            # Prevent dividing by zero if all packets are exactly the same size
            if std_dev > 0:
                # Calculate the Z-score deviation
                z_score = (packet_size - mean) / std_dev
                
                # Determine threat level using the new higher threshold
                is_anomaly = "YES" if z_score > THRESHOLD else "NO"

                # Log the live data to our CSV file for Streamlit
                with open("traffic_log.csv", "a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([current_time, source_ip, packet_size, z_score, is_anomaly])

                # Memory management & Console Output
                if z_score > THRESHOLD:
                    print(f"🚨 Anomaly logged from {source_ip}! Size: {packet_size} bytes (Z-Score: {z_score:.2f})")
                else:
                    # Remove the oldest packet and add the new safe packet to keep baseline updated
                    normal_traffic.pop(0)
                    normal_traffic.append(packet_size)
                    print("Traffic normal. Moving forward...")

# --- THE IGNITION ---
print(f"Starting Engine with Anomaly Threshold Z > {THRESHOLD}...")
print("Press Ctrl + C to stop the program at any time.")

# store=0 prevents Scapy from keeping all packets in RAM
sniff(prn=intelligent_anomaly_detector, store=0)