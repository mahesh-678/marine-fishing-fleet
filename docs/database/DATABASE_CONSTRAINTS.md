# Database Constraints and Referential Integrity

This document records the constraints declared in `sql/schema.sql`.

## Primary keys

Every table has an auto-incrementing integer primary key named `id`: `users`, `fishermen`, `boats`, `marine_zones`, `fishing_restrictions`, `fishing_trips`, `fish_species`, `catch_records`, `weather_records` and `safety_alerts`.

## Unique constraints

| Table | Column | Purpose |
|---|---|---|
| `users` | `username` | Prevent duplicate login names |
| `fishermen` | `license_number` | Prevent duplicate license numbers when populated |
| `boats` | `registration_number` | Prevent duplicate vessel registrations |
| `marine_zones` | `zone_name` | Prevent duplicate zone names |
| `fish_species` | `common_name` | Prevent duplicate common species names |

## Foreign keys and delete behaviour

| Child table.column | Parent table.column | Update behaviour | Delete behaviour |
|---|---|---|---|
| `boats.owner_id` | `fishermen.id` | CASCADE | RESTRICT |
| `fishing_restrictions.zone_id` | `marine_zones.id` | CASCADE | RESTRICT |
| `fishing_trips.boat_id` | `boats.id` | CASCADE | RESTRICT |
| `fishing_trips.captain_id` | `fishermen.id` | CASCADE | RESTRICT |
| `catch_records.trip_id` | `fishing_trips.id` | CASCADE | CASCADE |
| `catch_records.species_id` | `fish_species.id` | CASCADE | RESTRICT |
| `weather_records.trip_id` | `fishing_trips.id` | CASCADE | CASCADE |
| `safety_alerts.trip_id` | `fishing_trips.id` | CASCADE | CASCADE |
| `safety_alerts.zone_id` | `marine_zones.id` | CASCADE | SET NULL |

## CHECK constraints

| Table | Rule | Purpose |
|---|---|---|
| `fishing_restrictions` | `end_date >= start_date` | Restriction end cannot precede its start |
| `fishing_trips` | `return_time IS NULL OR return_time >= departure_time` | Return cannot precede departure |
| `catch_records` | `quantity_kg > 0` | A recorded catch must have positive quantity |
| `catch_records` | `market_value >= 0` | Estimated value cannot be negative |

MySQL CHECK enforcement depends on server version; the project targets MySQL 8.0+. The Flask catch form also checks positive quantity and non-negative market value.

## Enumerated status values

The schema restricts values for roles, boat status, zone type, trip status, weather advisory, alert type, alert severity and alert status using MySQL `ENUM` columns. See `docs/database/DATA_DICTIONARY.md` for the exact values.

## Indexes

The schema explicitly creates indexes for trip departure time, trip status, catch record timestamp, alert status and restriction date range. Details are in `INDEXING_AND_OPTIMIZATION.md`.
