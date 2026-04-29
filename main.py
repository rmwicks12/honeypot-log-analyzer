import mysql.connector
import time
import random
import requests

# 1. Connect to MySQL Workbench
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="rithwik@8", 
        database="honeypot_db"
    )
    cursor = db.cursor()
    print("✅ Successfully connected to the Honeypot Database!")
except mysql.connector.Error as err:
    print(f"❌ Connection Failed: {err}")
    exit()

# 2. Geolocation Tracker Function
def get_geolocation(ip_address):
    """Fetches the physical location of an IP address using a public API."""
    try:
        # We use a public IP for testing. If it's a local network IP (like 192.168.x.x), 
        # the API will fail, so we simulate a real-world scenario here.
        test_ip = "8.8.8.8" if ip_address.startswith("192.") else ip_address
        
        response = requests.get(f"http://ip-api.com/json/{test_ip}")
        data = response.json()
        
        if data.get("status") == "success":
            return data["city"], data["lat"], data["lon"]
    except Exception as e:
        print(f"⚠️ Could not fetch location: {e}")
    
    return "Unknown", 0.0, 0.0

# 3. The Core Honeypot Logic (Tarpit + Logging)
def handle_incoming_connection(ip_address):
    print(f"\n--- Incoming ping from IP: {ip_address} ---")
    
    # Check if attacker is known
    cursor.execute("SELECT threat_score FROM attackers WHERE ip_address = %s", (ip_address,))
    result = cursor.fetchone()

    if result:
        threat_score = result[0]
        print(f"⚠️ KNOWN THREAT DETECTED. Threat Level: {threat_score}/5")
        
        # Tarpit logic
        delay_time = threat_score * 3 
        print(f"Engaging Tarpit. Stalling connection for {delay_time} seconds...")
        time.sleep(delay_time)
        print("Tarpit released.")
    else:
        print("New IP detected. Registering in database...")
        cursor.execute("INSERT INTO attackers (ip_address, threat_score) VALUES (%s, 1)", (ip_address,))
        db.commit()

    # 4. Fetch Location and Log the Attack
    city, lat, lon = get_geolocation(ip_address)
    print(f"Tracking origin: {city} (Lat: {lat}, Lon: {lon})")
    
    cursor.execute("""
        INSERT INTO threat_logs (ip_address, location_city, latitude, longitude) 
        VALUES (%s, %s, %s, %s)
    """, (ip_address, city, lat, lon))
    db.commit()
    print("✅ Attack logged successfully.")

# 5. Simulate the attacks
# (Keep all your existing database connection and handle_incoming_connection logic above this line)

if __name__ == "__main__":
    import random # Make sure this is imported at the top of your file!
    
    print("🚀 Starting Live Honeypot Attack Simulator...\n")
    print("Press CTRL+C in the terminal to stop the simulation.\n")
    
    # A list of real global IPs to make the heatmap look awesome
    global_ips = [
        "103.82.14.23",   # India
        "46.17.40.0",     # Russia
        "114.114.114.114",# China
        "8.8.8.8",        # USA (Google)
        "187.190.38.140", # Mexico
        "177.54.148.10",  # Brazil
        "2.17.214.0",     # France
        "197.210.29.255", # Nigeria
        "139.130.4.5"     # Australia
    ]
    
    try:
        # Run 15 simulated attacks in a row
        for i in range(15): 
            target_ip = random.choice(global_ips)
            handle_incoming_connection(target_ip)
            
            # Wait 3 seconds before the next bot attacks
            time.sleep(3) 
            
    except KeyboardInterrupt:
        print("\n🛑 Simulation manually stopped.")