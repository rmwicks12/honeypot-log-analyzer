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
        # --- ASIA (India, China, Japan, SE Asia, Middle East) ---
        "103.82.14.23", "114.114.114.114", "210.1.224.1", "202.175.4.1", "121.121.121.121",
        "182.253.0.1", "124.120.0.1", "175.45.176.1", "203.119.0.1", "211.24.0.1",
        "1.1.1.1", "101.0.86.43", "111.13.101.208", "125.212.217.214", "218.100.0.1",
        "58.147.128.0", "222.124.0.1", "119.2.0.1", "210.212.0.1", "122.160.0.1",
        "94.200.0.1", "2.50.0.1", "82.194.64.1", "212.118.142.1", "178.250.240.1",
        "89.211.0.1", "213.132.0.1", "87.101.0.1", "193.188.128.1", "212.100.128.1",
        # --- EUROPE (UK, France, Germany, Russia, Nordics, Balkans) ---
        "2.17.214.0", "91.198.174.192", "163.1.0.1", "212.58.244.0", "81.169.145.0",
        "213.133.107.0", "194.25.0.1", "62.149.128.0", "195.234.0.1", "77.88.55.77",
        "5.9.0.1", "31.13.64.1", "37.9.64.1", "46.16.160.1", "62.210.0.1",
        "80.239.128.1", "88.198.0.1", "95.142.160.1", "109.163.224.1", "141.101.64.1",
        "176.9.0.1", "185.10.200.1", "188.165.0.1", "193.0.0.1", "195.154.0.1",
        "212.227.0.1", "217.160.0.1", "82.165.0.1", "85.214.0.1", "94.23.0.1",
        "178.63.0.1", "5.135.0.1", "46.105.0.1", "149.202.0.1", "51.254.0.1",
        "185.5.160.1", "91.121.0.1", "37.59.0.1", "164.132.0.1", "54.36.0.1",
        # --- NORTH AMERICA (USA, Canada, Mexico) ---
        "8.8.8.8", "172.217.1.1", "204.79.197.200", "23.212.0.0", "45.57.0.1",
        "142.250.0.0", "192.206.151.131", "187.190.38.140", "201.147.0.1", "66.249.64.0",
        "64.233.160.0", "66.102.0.0", "72.14.192.0", "74.125.0.0", "104.16.0.0",
        "107.154.0.1", "108.177.0.0", "151.101.1.67", "162.158.0.0", "192.0.78.0",
        "198.41.128.0", "199.27.128.0", "204.15.20.0", "205.251.192.0", "206.190.32.0",
        "207.126.144.0", "208.67.222.222", "209.85.128.0", "216.58.192.0", "216.239.32.0",
        "4.2.2.1", "9.9.9.9", "12.1.1.1", "63.245.208.0", "65.52.0.0",
        "69.171.224.0", "157.240.0.0", "173.194.0.0", "172.253.0.0", "157.55.0.0",
        # --- SOUTH AMERICA (Brazil, Argentina, Chile, Colombia, Peru) ---
        "177.54.148.10", "200.16.88.1", "190.111.0.1", "200.40.0.1", "201.217.0.1",
        "186.215.0.1", "191.241.0.1", "200.1.0.1", "181.30.0.1", "200.10.0.1",
        "200.1.121.1", "201.235.0.1", "186.0.0.1", "190.0.0.1", "200.0.0.1",
        "201.0.0.1", "187.0.0.1", "189.0.0.1", "179.0.0.1", "177.0.0.1",
        # --- AFRICA (Nigeria, South Africa, Egypt, Kenya, Ghana, Morocco) ---
        "197.210.29.255", "196.25.1.1", "41.222.0.1", "154.0.0.1", "197.156.0.1",
        "102.129.0.1", "105.235.0.1", "41.74.0.1", "197.254.0.1", "154.160.0.1",
        "41.190.0.1", "102.64.0.1", "156.192.0.1", "196.20.0.1", "197.1.0.1",
        "213.150.0.1", "41.21.0.1", "105.0.0.1", "160.154.0.1", "196.0.0.1",
        # --- OCEANIA (Australia, NZ, Fiji, PNG) ---
        "139.130.4.5", "202.89.0.1", "122.56.0.1", "27.106.0.1", "101.167.0.1",
        "1.0.0.1", "14.202.0.1", "43.245.160.1", "120.144.0.1", "203.0.0.1",
        # --- RANDOM DIVERSE ADDITIONS ---
        "45.33.32.156", "104.24.0.1", "141.101.112.1", "108.162.192.1", "190.93.240.1",
        "198.41.212.1", "162.158.0.1", "172.64.0.1", "104.16.128.1", "172.67.0.1",
        "104.18.0.1", "104.26.0.1", "104.22.0.1", "172.66.0.1", "104.20.0.1",
        "104.28.0.1", "104.21.0.1", "104.17.0.1", "104.19.0.1", "104.25.0.1",
        "104.27.0.1", "104.23.0.1", "104.16.0.1", "104.29.0.1", "172.70.0.1",
        "172.71.0.1", "141.101.64.1", "197.234.240.1", "108.162.192.1", "162.158.0.1"
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