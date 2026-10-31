# Data Integrity and Validation

## Relational integrity

Foreign keys connect boats to fishermen, trips to boats and captains, restrictions to zones, catches to trips and species, weather observations to trips, and alerts to trips and optional zones. These constraints prevent orphaned references.

## Uniqueness

The schema makes usernames, boat registration numbers, zone names and species common names unique. Fisherman license numbers are also unique when populated.

## Domain validation

- Boat status, trip status, zone type, weather advisory and alert status use enumerated values.
- Trip return time cannot precede departure time.
- Restriction end date cannot precede its start date.
- Catch quantity must be positive.
- Catch market value cannot be negative.
- The zone form validates latitude/longitude ranges and requires a positive radius.

## Application-level checks

The Flask handlers validate required fisherman fields, positive boat capacity, catch quantity and market value. The trip evaluator skips geospatial checks if either coordinate is missing. The application prevents deletion of fishermen referenced by boats/trips and boats that already have trips.

## Operational recommendations

- Validate and normalize imported records before loading them.
- Keep dates and timestamps consistent, including timezone assumptions.
- Avoid using sample zone coordinates or restrictions as authoritative data.
- Back up before bulk edits or seed reloads.
- Review rejected inserts and application errors instead of silently ignoring them.
