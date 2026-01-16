from flask import Flask, request, jsonify
from datetime import datetime
import joblib
import os

from preprocessing import preprocess_log

app = Flask(__name__)
MODEL_PATH = os.path.join("model", "trained_model.pkl")
model = joblib.load(MODEL_PATH)

traffic_data_store = []


@app.route("/logs", methods=["POST"])
def receive_logs():
    data = request.get_json()

    required_fields = ["ip", "timestamp", "username", "status"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        data["received_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        features = preprocess_log(data)
        prediction = model.predict(features)[0]

        data["prediction"] = int(prediction)

        traffic_data_store.append(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "message": "Log processed successfully",
        "prediction": int(prediction),
        "total_records": len(traffic_data_store)
    }), 201


@app.route("/logs", methods=["GET"])
def get_logs():
    return jsonify(traffic_data_store), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
