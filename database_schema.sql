-- Create and use the database
CREATE DATABASE honeypot_db;
USE honeypot_db;

-- Table to track unique attackers and their dynamic threat level
CREATE TABLE attackers (
    ip_address VARCHAR(45) PRIMARY KEY,
    threat_score INT DEFAULT 1,
    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table to log every individual attack and its geographical location
CREATE TABLE threat_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    ip_address VARCHAR(45),
    location_city VARCHAR(100),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    attack_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ip_address) REFERENCES attackers(ip_address)
);

-- Table to store high-priority alerts triggered by our traps
CREATE TABLE active_alerts (
    alert_id INT AUTO_INCREMENT PRIMARY KEY,
    alert_type VARCHAR(50),
    description TEXT,
    alert_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- The fake, enticing table
CREATE TABLE blr_office_admins (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    password_hash VARCHAR(255),
    access_level VARCHAR(20)
);

-- Insert a fake record to make it look legitimate if scanned
INSERT INTO blr_office_admins (username, password_hash, access_level) 
VALUES ('sys_admin', 'e10adc3949ba59abbe56e057f20f883e', 'SUPERUSER');
DELIMITER //

CREATE TRIGGER trap_rogue_admin_insert
AFTER INSERT ON blr_office_admins
FOR EACH ROW
BEGIN
    -- The moment a bot tries to add a new admin, log a CRITICAL alert
    INSERT INTO active_alerts (alert_type, description)
    VALUES ('CRITICAL BREACH', CONCAT('Unauthorized INSERT attempted on admin table. Attempted username: ', NEW.username));
END; //

DELIMITER ;
-- This wipes the history so you can start fresh
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE threat_logs;
SET FOREIGN_KEY_CHECKS = 1;

