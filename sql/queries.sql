USE marine_fleet_db;

-- 1. Total catch by species
SELECT fs.common_name, SUM(cr.quantity_kg) AS total_catch_kg
FROM fish_species fs
LEFT JOIN catch_records cr ON cr.species_id = fs.id
GROUP BY fs.id, fs.common_name
ORDER BY total_catch_kg DESC;

-- 2. Catch and estimated revenue by month
SELECT DATE_FORMAT(recorded_at, '%Y-%m') AS month,
       SUM(quantity_kg) AS catch_kg, SUM(market_value) AS estimated_value
FROM catch_records
GROUP BY DATE_FORMAT(recorded_at, '%Y-%m')
ORDER BY month;

-- 3. Boats with the number of trips and total recorded catch
SELECT b.registration_number, b.boat_name, COUNT(DISTINCT ft.id) AS trip_count,
       COALESCE(SUM(cr.quantity_kg), 0) AS total_catch_kg
FROM boats b
LEFT JOIN fishing_trips ft ON ft.boat_id = b.id
LEFT JOIN catch_records cr ON cr.trip_id = ft.id
GROUP BY b.id, b.registration_number, b.boat_name
ORDER BY total_catch_kg DESC;

-- 4. Open safety alerts with vessel, captain and zone information
SELECT sa.id, sa.alert_type, sa.severity, sa.status, sa.message,
       b.boat_name, f.full_name AS captain, mz.zone_name, sa.created_at
FROM safety_alerts sa
JOIN fishing_trips ft ON ft.id = sa.trip_id
JOIN boats b ON b.id = ft.boat_id
JOIN fishermen f ON f.id = ft.captain_id
LEFT JOIN marine_zones mz ON mz.id = sa.zone_id
WHERE sa.status <> 'resolved'
ORDER BY FIELD(sa.severity, 'critical','high','medium','low'), sa.created_at DESC;

-- 5. Trips that have a location recorded inside an active restricted/protected zone.
-- This is a simple circular-radius approximation, not a legal boundary test.
SELECT ft.id AS trip_id, b.boat_name, mz.zone_name, mz.zone_type, ft.departure_time
FROM fishing_trips ft
JOIN boats b ON b.id = ft.boat_id
JOIN marine_zones mz ON mz.active = TRUE AND mz.zone_type IN ('restricted','protected')
WHERE ft.recorded_lat IS NOT NULL AND ft.recorded_lng IS NOT NULL
  AND 6371 * 2 * ASIN(SQRT(
    POWER(SIN(RADIANS(CAST(ft.recorded_lat AS DECIMAL(10,7)) - CAST(mz.center_lat AS DECIMAL(10,7))) / 2), 2)
    + COS(RADIANS(CAST(ft.recorded_lat AS DECIMAL(10,7))))
    * COS(RADIANS(CAST(mz.center_lat AS DECIMAL(10,7))) )
    * POWER(SIN(RADIANS(CAST(ft.recorded_lng AS DECIMAL(10,7)) - CAST(mz.center_lng AS DECIMAL(10,7))) / 2), 2)
  )) <= mz.radius_km;

-- 6. Species never recorded in a catch (relational division-style NOT EXISTS query)
SELECT fs.common_name
FROM fish_species fs
WHERE NOT EXISTS (SELECT 1 FROM catch_records cr WHERE cr.species_id = fs.id);

-- 7. Trips with catch totals greater than the average trip catch
WITH trip_totals AS (
  SELECT ft.id AS trip_id, b.boat_name, COALESCE(SUM(cr.quantity_kg), 0) AS catch_kg
  FROM fishing_trips ft JOIN boats b ON b.id = ft.boat_id
  LEFT JOIN catch_records cr ON cr.trip_id = ft.id
  GROUP BY ft.id, b.boat_name
)
SELECT * FROM trip_totals
WHERE catch_kg > (SELECT AVG(catch_kg) FROM trip_totals)
ORDER BY catch_kg DESC;

-- 8. Seasonal restrictions that overlap a trip date
SELECT ft.id AS trip_id, b.boat_name, fr.restriction_name, mz.zone_name,
       ft.departure_time, fr.start_date, fr.end_date
FROM fishing_trips ft
JOIN boats b ON b.id = ft.boat_id
JOIN marine_zones mz ON mz.active = TRUE
JOIN fishing_restrictions fr ON fr.zone_id = mz.id
WHERE DATE(ft.departure_time) BETWEEN fr.start_date AND fr.end_date;

-- 9. Boat utilization: count trips by operational status
SELECT b.boat_name, b.status AS boat_status,
       SUM(ft.status = 'returned') AS returned_trips,
       SUM(ft.status = 'at_sea') AS trips_at_sea,
       SUM(ft.status = 'flagged') AS flagged_trips
FROM boats b LEFT JOIN fishing_trips ft ON ft.boat_id = b.id
GROUP BY b.id, b.boat_name, b.status;

-- 10. Weather records requiring attention
SELECT wr.*, ft.boat_id, b.boat_name
FROM weather_records wr JOIN fishing_trips ft ON ft.id = wr.trip_id
JOIN boats b ON b.id = ft.boat_id
WHERE wr.advisory_level IN ('warning','danger')
ORDER BY wr.observed_at DESC;
