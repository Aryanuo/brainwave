from flask import Flask, request, jsonify
from flask_cors import CORS 
from datetime import datetime
import joblib
import os
import pandas as pd
import sys
import threading

from agent import get_threat_report

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "model")))
from model import compute_risk_score, clean_dataset, SIMULATION_FEATURES

app = Flask(__name__)
CORS(app) 

BASE_MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "model"))
RF_PATH = os.path.join(BASE_MODEL_PATH, "rf_model.pkl")
ISO_PATH = os.path.join(BASE_MODEL_PATH, "iso_model.pkl")
PREPROCESSOR_PATH = os.path.join(BASE_MODEL_PATH, "preprocessor.pkl")

try:
    rf_model = joblib.load(RF_PATH)
    iso_model = joblib.load(ISO_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    print("All model artifacts loaded successfully.")
except Exception as e:
    print(f"Error loading models: {e}")

traffic_data_store = []

def run_ai_agent_async(log_entry):
   
    try:
        agent_data = get_threat_report(
            failed_logins=log_entry.get('failed_logins', 0),
            request_rate=int(log_entry.get('Total Fwd Packets', 0)),
            data_size=int(log_entry.get('Total Length of Fwd Packets', 0)),
            blocking=False 
        )
        log_entry['ai_report'] = agent_data
    except Exception as e:
        log_entry['ai_report'] = {"status": "ERROR", "message": str(e)}

@app.route("/logs", methods=["POST"])
def receive_logs():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        # 1. Prediction logic
        df_input = pd.DataFrame([data])
        available_cols = [c for c in SIMULATION_FEATURES if c in df_input.columns]
        df_input = clean_dataset(df_input[available_cols])
        
        results = compute_risk_score(rf_model, iso_model, preprocessor, df_input)
        prediction_result = results[0]
        
        
        data["received_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data.update(prediction_result)
        
        # TRIGGER BACKGROUND THREAD FOR THREATS
        if prediction_result['risk_label'] in ['High-Risk', 'Watchlist']:
            # Start thread so the API can return immediately
            thread = threading.Thread(target=run_ai_agent_async, args=(data,))
            thread.daemon = True
            thread.start()
        else:
            data['ai_report'] = {"status": "SKIPPED", "message": "Benign traffic"}

        # Store and Respond Instantly
        traffic_data_store.append(data)
        return jsonify({
            "message": "Log processed successfully",
            "analysis": prediction_result
        }), 201

    except Exception as e:
        print(f"Prediction Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/logs", methods=["GET"])
def get_logs():
    return jsonify(traffic_data_store), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
