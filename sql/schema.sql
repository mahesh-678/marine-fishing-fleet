CREATE DATABASE IF NOT EXISTS marine_fleet_db
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE marine_fleet_db;

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(80) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  role ENUM('admin','organizer','viewer') NOT NULL DEFAULT 'organizer',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS fishermen (
  id INT AUTO_INCREMENT PRIMARY KEY,
  full_name VARCHAR(120) NOT NULL,
  phone VARCHAR(25),
  village VARCHAR(100) NOT NULL,
  license_number VARCHAR(60) UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS boats (
  id INT AUTO_INCREMENT PRIMARY KEY,
  registration_number VARCHAR(40) NOT NULL UNIQUE,
  boat_name VARCHAR(100) NOT NULL,
  owner_id INT NOT NULL,
  boat_type VARCHAR(60) NOT NULL,
  capacity_kg DECIMAL(10,2) NOT NULL DEFAULT 0,
  status ENUM('active','maintenance','inactive') NOT NULL DEFAULT 'active',
  FOREIGN KEY (owner_id) REFERENCES fishermen(id) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS marine_zones (
  id INT AUTO_INCREMENT PRIMARY KEY,
  zone_name VARCHAR(120) NOT NULL UNIQUE,
  zone_type ENUM('permitted','restricted','protected') NOT NULL,
  description TEXT,
  center_lat DECIMAL(10,7) NOT NULL,
  center_lng DECIMAL(10,7) NOT NULL,
  radius_km DECIMAL(8,2) NOT NULL DEFAULT 1,
  active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS fishing_restrictions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  zone_id INT NOT NULL,
  restriction_name VARCHAR(150) NOT NULL,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  notes TEXT,
  FOREIGN KEY (zone_id) REFERENCES marine_zones(id) ON UPDATE CASCADE ON DELETE RESTRICT,
  CHECK (end_date >= start_date)
);

CREATE TABLE IF NOT EXISTS fishing_trips (
  id INT AUTO_INCREMENT PRIMARY KEY,
  boat_id INT NOT NULL,
  captain_id INT NOT NULL,
  departure_time DATETIME NOT NULL,
  return_time DATETIME NULL,
  departure_port VARCHAR(120) NOT NULL,
  recorded_lat DECIMAL(10,7),
  recorded_lng DECIMAL(10,7),
  status ENUM('planned','at_sea','returned','flagged') NOT NULL DEFAULT 'planned',
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (boat_id) REFERENCES boats(id) ON UPDATE CASCADE ON DELETE RESTRICT,
  FOREIGN KEY (captain_id) REFERENCES fishermen(id) ON UPDATE CASCADE ON DELETE RESTRICT,
  CHECK (return_time IS NULL OR return_time >= departure_time)
);

CREATE TABLE IF NOT EXISTS fish_species (
  id INT AUTO_INCREMENT PRIMARY KEY,
  common_name VARCHAR(100) NOT NULL UNIQUE,
  scientific_name VARCHAR(150),
  conservation_status VARCHAR(60) DEFAULT 'Not assessed',
  breeding_season_notes TEXT
);

CREATE TABLE IF NOT EXISTS catch_records (
  id INT AUTO_INCREMENT PRIMARY KEY,
  trip_id INT NOT NULL,
  species_id INT NOT NULL,
  quantity_kg DECIMAL(10,2) NOT NULL,
  recorded_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  market_value DECIMAL(12,2) NOT NULL DEFAULT 0,
  notes TEXT,
  FOREIGN KEY (trip_id) REFERENCES fishing_trips(id) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (species_id) REFERENCES fish_species(id) ON UPDATE CASCADE ON DELETE RESTRICT,
  CHECK (quantity_kg > 0),
  CHECK (market_value >= 0)
);

CREATE TABLE IF NOT EXISTS weather_records (
  id INT AUTO_INCREMENT PRIMARY KEY,
  trip_id INT NOT NULL,
  observed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  condition_text VARCHAR(80) NOT NULL,
  wind_speed_kmh DECIMAL(6,2) DEFAULT 0,
  wave_height_m DECIMAL(5,2) DEFAULT 0,
  advisory_level ENUM('normal','caution','warning','danger') NOT NULL DEFAULT 'normal',
  notes TEXT,
  FOREIGN KEY (trip_id) REFERENCES fishing_trips(id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS safety_alerts (
  id INT AUTO_INCREMENT PRIMARY KEY,
  trip_id INT NOT NULL,
  zone_id INT NULL,
  alert_type ENUM('restricted_zone','seasonal_ban','weather','manual_review') NOT NULL,
  severity ENUM('low','medium','high','critical') NOT NULL DEFAULT 'medium',
  message VARCHAR(500) NOT NULL,
  status ENUM('open','reviewing','resolved') NOT NULL DEFAULT 'open',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  resolved_at DATETIME NULL,
  FOREIGN KEY (trip_id) REFERENCES fishing_trips(id) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (zone_id) REFERENCES marine_zones(id) ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE INDEX idx_trip_departure ON fishing_trips(departure_time);
CREATE INDEX idx_trip_status ON fishing_trips(status);
CREATE INDEX idx_catch_recorded_at ON catch_records(recorded_at);
CREATE INDEX idx_alert_status ON safety_alerts(status);
CREATE INDEX idx_restriction_dates ON fishing_restrictions(start_date, end_date);
