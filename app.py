from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app) # Allows our HTML file to request data from this API

# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="rithwik@8", 
        database="honeypot_db"
    )

@app.route('/api/threats', methods=['GET'])
def get_threats():
    """Fetches all logged attacks from MySQL and sends them as JSON."""
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True) # Returns data as clean dictionaries
        
        # Grab the latest 100 attacks
        cursor.execute("SELECT ip_address, location_city, latitude, longitude FROM threat_logs ORDER BY attack_time DESC LIMIT 100")
        threats = cursor.fetchall()
        
        db.close()
        return jsonify(threats)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Honeypot API Server on http://localhost:5000/api/threats")
    app.run(debug=True, port=5000)