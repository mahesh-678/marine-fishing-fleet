USE marine_fleet_db;
DELIMITER $$

-- Demonstration stored procedure: summary of catch for a date range.
DROP PROCEDURE IF EXISTS sp_catch_summary$$
CREATE PROCEDURE sp_catch_summary(IN p_start DATE, IN p_end DATE)
BEGIN
  SELECT fs.common_name, SUM(cr.quantity_kg) AS total_kg,
         SUM(cr.market_value) AS estimated_value
  FROM catch_records cr
  JOIN fish_species fs ON fs.id = cr.species_id
  WHERE DATE(cr.recorded_at) BETWEEN p_start AND p_end
  GROUP BY fs.id, fs.common_name
  ORDER BY total_kg DESC;
END$$

-- Demonstration trigger: reject non-positive catch quantities.
DROP TRIGGER IF EXISTS trg_catch_positive_quantity$$
CREATE TRIGGER trg_catch_positive_quantity
BEFORE INSERT ON catch_records
FOR EACH ROW
BEGIN
  IF NEW.quantity_kg <= 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Catch quantity must be greater than zero';
  END IF;
END$$

DELIMITER ;

-- Example call after loading sample data:
-- CALL sp_catch_summary('2026-10-01', '2026-10-31');
