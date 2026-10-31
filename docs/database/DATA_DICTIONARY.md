# Data Dictionary

The following definitions are based on the `CREATE TABLE` statements in `sql/schema.sql`. MySQL types and nullability are shown as declared in that file.

## `users`

| Column | Type | Rules / meaning |
|---|---|---|
| `id` | `INT` | Primary key, auto-increment |
| `username` | `VARCHAR(80)` | Required, unique login name |
| `password_hash` | `VARCHAR(255)` | Required password hash; plaintext passwords should not be stored |
| `role` | `ENUM('admin','organizer','viewer')` | Required; default `organizer` |
| `created_at` | `TIMESTAMP` | Defaults to current timestamp |

## `fishermen`

| Column | Type | Rules / meaning |
|---|---|---|
| `id` | `INT` | Primary key, auto-increment |
| `full_name` | `VARCHAR(120)` | Required name |
| `phone` | `VARCHAR(25)` | Optional contact number |
| `village` | `VARCHAR(100)` | Required village |
| `license_number` | `VARCHAR(60)` | Optional, unique when supplied |
| `created_at` | `TIMESTAMP` | Defaults to current timestamp |

## `boats`

| Column | Type | Rules / meaning |
|---|---|---|
| `id` | `INT` | Primary key, auto-increment |
| `registration_number` | `VARCHAR(40)` | Required, unique vessel registration |
| `boat_name` | `VARCHAR(100)` | Required display name |
| `owner_id` | `INT` | Required FK to `fishermen.id` |
| `boat_type` | `VARCHAR(60)` | Required vessel category |
| `capacity_kg` | `DECIMAL(10,2)` | Required; default 0 in SQL schema |
| `status` | `ENUM('active','maintenance','inactive')` | Required; default `active` |

## `marine_zones`

| Column | Type | Rules / meaning |
|---|---|---|
| `id` | `INT` | Primary key, auto-increment |
| `zone_name` | `VARCHAR(120)` | Required, unique |
| `zone_type` | `ENUM('permitted','restricted','protected')` | Required zone category |
| `description` | `TEXT` | Optional explanation |
| `center_lat` | `DECIMAL(10,7)` | Required center latitude |
| `center_lng` | `DECIMAL(10,7)` | Required center longitude |
| `radius_km` | `DECIMAL(8,2)` | Required; default 1 km |
| `active` | `BOOLEAN` | Required; default true |

## `fishing_restrictions`

| Column | Type | Rules / meaning |
|---|---|---|
| `id` | `INT` | Primary key, auto-increment |
| `zone_id` | `INT` | Required FK to `marine_zones.id` |
| `restriction_name` | `VARCHAR(150)` | Required restriction label |
| `start_date` | `DATE` | Required first date |
| `end_date` | `DATE` | Required last date; CHECK requires end >= start |
| `notes` | `TEXT` | Optional notes |

## `fishing_trips`

| Column | Type | Rules / meaning |
|---|---|---|
| `id` | `INT` | Primary key, auto-increment |
| `boat_id` | `INT` | Required FK to `boats.id` |
| `captain_id` | `INT` | Required FK to `fishermen.id` |
| `departure_time` | `DATETIME` | Required departure date/time |
| `return_time` | `DATETIME` | Optional return date/time; cannot precede departure |
| `departure_port` | `VARCHAR(120)` | Required departure location label |
| `recorded_lat` | `DECIMAL(10,7)` | Optional recorded latitude |
| `recorded_lng` | `DECIMAL(10,7)` | Optional recorded longitude |
| `status` | `ENUM('planned','at_sea','returned','flagged')` | Required; default `planned` |
| `notes` | `TEXT` | Optional trip notes |
| `created_at` | `TIMESTAMP` | Defaults to current timestamp |

## `fish_species`

| Column | Type | Rules / meaning |
|---|---|---|
| `id` | `INT` | Primary key, auto-increment |
| `common_name` | `VARCHAR(100)` | Required, unique species name |
| `scientific_name` | `VARCHAR(150)` | Optional scientific name |
| `conservation_status` | `VARCHAR(60)` | Defaults to `Not assessed` |
| `breeding_season_notes` | `TEXT` | Optional notes |

## `catch_records`

| Column | Type | Rules / meaning |
|---|---|---|
| `id` | `INT` | Primary key, auto-increment |
| `trip_id` | `INT` | Required FK to `fishing_trips.id` |
| `species_id` | `INT` | Required FK to `fish_species.id` |
| `quantity_kg` | `DECIMAL(10,2)` | Required; CHECK requires > 0 |
| `recorded_at` | `DATETIME` | Required; defaults to current timestamp |
| `market_value` | `DECIMAL(12,2)` | Required; default 0; CHECK requires >= 0 |
| `notes` | `TEXT` | Optional notes |

## `weather_records`

| Column | Type | Rules / meaning |
|---|---|---|
| `id` | `INT` | Primary key, auto-increment |
| `trip_id` | `INT` | Required FK to `fishing_trips.id` |
| `observed_at` | `DATETIME` | Required; defaults to current timestamp |
| `condition_text` | `VARCHAR(80)` | Required weather description |
| `wind_speed_kmh` | `DECIMAL(6,2)` | Defaults to 0 |
| `wave_height_m` | `DECIMAL(5,2)` | Defaults to 0 |
| `advisory_level` | `ENUM('normal','caution','warning','danger')` | Required; default `normal` |
| `notes` | `TEXT` | Optional notes |

## `safety_alerts`

| Column | Type | Rules / meaning |
|---|---|---|
| `id` | `INT` | Primary key, auto-increment |
| `trip_id` | `INT` | Required FK to `fishing_trips.id` |
| `zone_id` | `INT` | Optional FK to `marine_zones.id` |
| `alert_type` | `ENUM('restricted_zone','seasonal_ban','weather','manual_review')` | Required category |
| `severity` | `ENUM('low','medium','high','critical')` | Required; default `medium` |
| `message` | `VARCHAR(500)` | Required alert explanation |
| `status` | `ENUM('open','reviewing','resolved')` | Required; default `open` |
| `created_at` | `TIMESTAMP` | Defaults to current timestamp |
| `resolved_at` | `DATETIME` | Optional resolution time |
