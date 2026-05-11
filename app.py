from flask import Flask, render_template, jsonify, request
import datetime

app = Flask(__name__)

# In-memory database for demo purposes
plc_state = {
    "status": "RUN",  # Can be RUN, STOP, or ERROR
    "speed": 1500,
    "temperature": 45.5,
    "last_update": datetime.datetime.now().strftime("%H:%M:%S")
}

security_alerts = []

@app.route('/')
def index():
    return render_template('index.html')

# API Endpoint to get the current PLC Status
@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify(plc_state)

# API Endpoint to get all security alerts
@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    # Return last 50 alerts, newest first
    return jsonify(sorted(security_alerts, key=lambda x: x['timestamp'], reverse=True)[:50])

# API Endpoint for student scripts to push alerts/events
@app.route('/api/report', methods=['POST'])
def report_alert():
    data = request.json
    
    if not data or 'message' not in data:
        return jsonify({"error": "Invalid payload, requires 'message'"}), 400

    alert = {
        "id": len(security_alerts) + 1,
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
        "severity": data.get('severity', 'LOW'),  # HIGH, MEDIUM, LOW
        "source": data.get('source', 'Unknown Script'),
        "message": data['message']
    }
    
    security_alerts.append(alert)
    return jsonify({"success": True, "alert": alert}), 201

# API Endpoint to update simulated PLC status
@app.route('/api/update_plc', methods=['POST'])
def update_plc():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    if 'status' in data:
        plc_state['status'] = data['status'].upper()
    if 'speed' in data:
        plc_state['speed'] = data['speed']
    if 'temperature' in data:
        plc_state['temperature'] = data['temperature']
        
    plc_state['last_update'] = datetime.datetime.now().strftime("%H:%M:%S")
    
    # Auto-generate alert if status goes to STOP
    if plc_state['status'] == "STOP":
        security_alerts.append({
            "id": len(security_alerts) + 1,
            "timestamp": plc_state['last_update'],
            "severity": "HIGH",
            "source": "PLC State Monitor",
            "message": "CRITICAL: PLC Status changed to STOP!"
        })

    return jsonify({"success": True, "state": plc_state})

if __name__ == '__main__':
    # Run on all interfaces so other students can send data to it
    app.run(host='0.0.0.0', port=5000, debug=True)
