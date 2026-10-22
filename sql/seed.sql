USE marine_fleet_db;

INSERT IGNORE INTO fishermen (id, full_name, phone, village, license_number) VALUES
(1,'Arun Kumar','9876501001','Rameswaram','TN-FISH-1001'),
(2,'Selvam Raj','9876501002','Mandapam','TN-FISH-1002'),
(3,'Meena Devi','9876501003','Pamban','TN-FISH-1003'),
(4,'Karthik M','9876501004','Nagapattinam','TN-FISH-1004'),
(5,'Ravi Shankar','9876501005','Thoothukudi','TN-FISH-1005');

INSERT IGNORE INTO boats (id, registration_number, boat_name, owner_id, boat_type, capacity_kg, status) VALUES
(1,'TN-RMM-001','Kadal Vendan',1,'Mechanized trawler',1800,'active'),
(2,'TN-MDM-014','Blue Pearl',2,'Motorized boat',850,'active'),
(3,'TN-PMB-022','Amman Thunai',3,'Traditional craft',350,'active'),
(4,'TN-NGP-009','Sea Star',4,'Motorized boat',700,'maintenance'),
(5,'TN-TTK-031','Ocean Friend',5,'Mechanized trawler',1500,'active');

INSERT IGNORE INTO marine_zones (id, zone_name, zone_type, description, center_lat, center_lng, radius_km, active) VALUES
(1,'Rameswaram Coastal Fishing Area','permitted','Example permitted zone for demonstration only.',9.2876,79.3129,12,TRUE),
(2,'Gulf of Mannar Protected Zone','protected','Illustrative protected-zone marker. Confirm official boundaries before operational use.',9.1000,79.2500,8,TRUE),
(3,'Training Restricted Zone','restricted','Synthetic restricted zone used to demonstrate alerts; not an official boundary.',9.3500,79.4500,5,TRUE),
(4,'Nagapattinam Demonstration Zone','permitted','Example permitted zone for dashboard demonstrations.',10.7650,79.8420,10,TRUE);

INSERT IGNORE INTO fishing_restrictions (id, zone_id, restriction_name, start_date, end_date, notes) VALUES
(1,2,'Protected-area review period','2026-04-01','2026-06-30','Sample dates only. Replace with current official restrictions.'),
(2,3,'Demonstration seasonal restriction','2026-10-01','2026-10-31','Synthetic restriction for testing the application.');

INSERT IGNORE INTO fish_species (id, common_name, scientific_name, conservation_status, breeding_season_notes) VALUES
(1,'Indian mackerel','Rastrelliger kanagurta','Not assessed','Use official fisheries guidance for seasonal rules.'),
(2,'Sardine','Sardinella longiceps','Not assessed','Use official fisheries guidance for seasonal rules.'),
(3,'Indian squid','Uroteuthis duvaucelii','Not assessed','Use official fisheries guidance for seasonal rules.'),
(4,'Seer fish','Scomberomorus commerson','Not assessed','Use official fisheries guidance for seasonal rules.'),
(5,'Prawn','Penaeus spp.','Not assessed','Species-specific restrictions may apply.');

INSERT IGNORE INTO fishing_trips (id, boat_id, captain_id, departure_time, return_time, departure_port, recorded_lat, recorded_lng, status, notes) VALUES
(1,1,1,'2026-10-10 05:30:00','2026-10-10 14:15:00','Rameswaram Harbour',9.2876,79.3129,'returned','Sample trip record.'),
(2,2,2,'2026-10-12 04:45:00','2026-10-12 12:20:00','Mandapam Port',9.2750,79.1250,'returned','Sample trip record.'),
(3,3,3,'2026-10-15 06:00:00',NULL,'Pamban Harbour',9.2800,79.2050,'at_sea','Sample active trip.'),
(4,5,5,'2026-10-18 05:10:00','2026-10-18 13:40:00','Thoothukudi Port',8.7642,78.1348,'returned','Sample trip record.');

INSERT IGNORE INTO catch_records (id, trip_id, species_id, quantity_kg, recorded_at, market_value, notes) VALUES
(1,1,1,120,'2026-10-10 11:00:00',24000,'Sample catch record.'),
(2,1,3,28,'2026-10-10 11:20:00',11200,'Sample catch record.'),
(3,2,2,95,'2026-10-12 10:30:00',14250,'Sample catch record.'),
(4,3,4,22,'2026-10-15 09:45:00',17600,'Sample catch record.'),
(5,4,5,45,'2026-10-18 10:00:00',22500,'Sample catch record.'),
(6,4,1,105,'2026-10-18 10:20:00',21000,'Sample catch record.');

INSERT IGNORE INTO weather_records (id, trip_id, observed_at, condition_text, wind_speed_kmh, wave_height_m, advisory_level, notes) VALUES
(1,1,'2026-10-10 07:00:00','Partly cloudy',12,0.8,'normal','Sample weather record.'),
(2,2,'2026-10-12 08:00:00','Wind increasing',24,1.5,'caution','Sample weather record.'),
(3,3,'2026-10-15 08:00:00','Rough sea',38,2.8,'warning','Sample weather record.'),
(4,4,'2026-10-18 07:30:00','Clear',10,0.6,'normal','Sample weather record.');

INSERT IGNORE INTO safety_alerts (id, trip_id, zone_id, alert_type, severity, message, status, created_at) VALUES
(1,3,2,'restricted_zone','high','Sample alert: trip location requires a manual review against authoritative zone boundaries.','open','2026-10-15 08:10:00'),
(2,3,NULL,'weather','high','Sample alert: weather record has a warning advisory. Confirm local marine forecast before departure or continuing at sea.','open','2026-10-15 08:15:00');
