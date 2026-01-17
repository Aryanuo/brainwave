import random 
import requests
import time

# Importing your generation functions
from attack import (
    generateNormal, 
    generateAnomaly, 
    generateBruteForce, 
    generateDos, 
    generateUdp
)

API_URL = "http://localhost:5000/logs"   

def run_main():
    print("🚀 Starting Network Traffic Simulation...")
    
    while True:
        choice = random.randint(1, 100)

        # 1. Generate the simulated record and assign a manual label for tracking
        if (1 <= choice <= 70):
            record = generateNormal()
            sim_type = "Benign"
        elif (71 <= choice <= 80):
            record = generateBruteForce()
            sim_type = "Brute Force"
        elif (81 <= choice <= 88):
            record = generateDos()
            sim_type = "DoS"
        elif (89 <= choice <= 95):
            record = generateUdp()
            sim_type = "UDP Flood"
        else:
            record = generateAnomaly()
            sim_type = "Anomaly"

        # --- PREPARE DATA FOR API ---
        try:
            record["Simulated Type"] = sim_type 

            # 2. Send the record to the API
            response = requests.post(API_URL, json=record, timeout=10)
            
            print(f"\n[SENT] Simulated Type: {sim_type}")
            print(f"Log Data: {record}")
            
            if response.status_code == 201:
                api_data = response.json()
                analysis = api_data.get("analysis", {})
                
                print(f"-> ML Prediction: {analysis.get('attack_type')} ({analysis.get('risk_label')})")
                
                if "executionID" in str(analysis.get('ai_report')):
                    print(f"-> AI Agent: Started Investigation (ID: {analysis['ai_report']['executionID']})")
            else:
                print(f"API Error ({response.status_code}):", response.text)

        except Exception as e:
            print("API not reachable. Ensure api.py is running on port 5000.")

        time.sleep(0.01) 

if __name__ == "__main__":
    run_main()
