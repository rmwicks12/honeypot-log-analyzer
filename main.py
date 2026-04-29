import mysql.connector
import time
import requests

# 1. Connect to MySQL Workbench
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="rithwik@8", # <-- Change this!
        database="honeypot_db"
    )
    cursor = db.cursor()
    print("✅ Successfully connected to the Honeypot Database!")
except mysql.connector.Error as err:
    print(f"❌ Connection Failed: {err}")
    exit()

# 2. The Tarpit Function (Time Wasting)
def handle_incoming_connection(ip_address):
    print(f"\nIncoming ping from IP: {ip_address}...")
    
    # Check if this attacker is already in our database
    cursor.execute("SELECT threat_score FROM attackers WHERE ip_address = %s", (ip_address,))
    result = cursor.fetchone()

    if result:
        # Attacker found! Engage the Tarpit.
        threat_score = result[0]
        print(f"⚠️ KNOWN THREAT DETECTED. Threat Level: {threat_score}/5")
        
        delay_time = threat_score * 3 # e.g., Level 5 threat waits 15 seconds
        print(f"Engaging Tarpit. Stalling connection for {delay_time} seconds...")
        time.sleep(delay_time)
        print("Tarpit released. Connection dropped.")
        
    else:
        # New attacker. Log them into the database with a base threat level of 1
        print("New IP detected. Logging into database...")
        cursor.execute("INSERT INTO attackers (ip_address, threat_score) VALUES (%s, 1)", (ip_address,))
        db.commit()
        print("IP Logged successfully.")

# 3. Simulate some attacks to test the logic
if __name__ == "__main__":
    print("Starting Honeypot Listener Simulator...\n")
    
    # Simulating a brand new attack
    handle_incoming_connection("192.168.1.50")
    
    # Let's manually bump their threat score in the DB to test the Tarpit
    cursor.execute("UPDATE attackers SET threat_score = 4 WHERE ip_address = '192.168.1.50'")
    db.commit()
    print("\n[Simulating the same bot returning after trying to hack an admin account...]")
    
    # Simulating the same IP attacking again
    handle_incoming_connection("192.168.1.50")