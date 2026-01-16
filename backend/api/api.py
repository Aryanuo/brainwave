from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

traffic_data_store = []

@app.route('/logs', methods=['POST'])
def receive_logs():
    data = request.get_json()
    
    required_fields = ["ip", "timestamp", "username", "status", "label"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    try:
        data['received_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        traffic_data_store.append(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({
        "message": "Log received successfully",
        "total_records": len(traffic_data_store)
    }), 201

@app.route('/logs', methods=['GET'])
def get_logs():
    return jsonify(traffic_data_store), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)