# Database Normalisation

This note analyses the schema in `sql/schema.sql`. It explains how the project separates operational concepts into related tables to reduce duplication and update anomalies.

## 1. Main functional dependencies

The following dependencies describe the intended identifiers in the current schema:

| Relation | Functional dependency | Reason |
|---|---|---|
| `users` | `id → username, password_hash, role, created_at` | One account row is identified by its user ID. `username` is also unique. |
| `fishermen` | `id → full_name, phone, village, license_number, created_at` | Each fisherman row has its own ID; a non-NULL license number is unique. |
| `boats` | `id → registration_number, boat_name, owner_id, boat_type, capacity_kg, status` | Each boat has an ID and a unique registration number. |
| `marine_zones` | `id → zone_name, zone_type, description, center_lat, center_lng, radius_km, active` | Each zone has an ID and a unique name. |
| `fishing_trips` | `id → boat_id, captain_id, departure_time, return_time, departure_port, recorded_lat, recorded_lng, status, notes` | Each trip is identified by its ID. |
| `fish_species` | `id → common_name, scientific_name, conservation_status, breeding_season_notes` | Each species has an ID and unique common name. |
| `catch_records` | `id → trip_id, species_id, quantity_kg, recorded_at, market_value, notes` | Each catch record has its own ID. |

Equivalent dependencies apply to `fishing_restrictions`, `weather_records` and `safety_alerts`: their primary key determines the remaining attributes in each row.

## 2. First Normal Form (1NF)

The schema uses individual columns for individual values. For example, a catch record stores one `trip_id`, one `species_id`, one `quantity_kg` and one `market_value`. Multiple catches are represented as multiple rows in `catch_records`, rather than repeating columns such as `species_1`, `species_2` and `species_3`.

This is consistent with 1NF's requirement for atomic column values and the absence of repeating groups.

## 3. Second Normal Form (2NF)

Every table in the current schema has a single-column primary key (`id`). Therefore, there cannot be a partial dependency of a non-key attribute on only part of a composite primary key. The schema satisfies the usual 2NF condition, assuming the stated keys and dependencies.

## 4. Third Normal Form (3NF)

Descriptive information is separated into its own relations and referenced by foreign keys:

- Fisherman details are stored in `fishermen`; `boats` stores `owner_id` instead of repeating the owner's name, phone and village for every boat.
- Boat and captain details are stored in their respective parent tables; `fishing_trips` stores `boat_id` and `captain_id`.
- Species descriptions are stored once in `fish_species`; `catch_records` stores `species_id`.
- Marine-zone details are stored in `marine_zones`; date-based restriction rows refer to a zone through `zone_id`.
- Catch, weather and alert records are separate child relations linked to trips.

This reduces repeated descriptive data and helps avoid update, insertion and deletion anomalies.

## 5. BCNF consideration

The declared primary keys and unique constraints make the listed identifiers candidate keys for their relations. Under the functional dependencies documented above, each non-trivial determinant is a candidate key, which is consistent with BCNF. If additional business rules introduce dependencies (for example, if a registration number is not globally unique in a future deployment), the design should be reviewed again.

## 6. Anomalies reduced by the design

| Potential anomaly | Design choice |
|---|---|
| Updating a fisherman's phone number in every boat row | Store contact details once in `fishermen`. |
| Repeating species names for every catch | Store species once in `fish_species` and reference it by ID. |
| Repeating boat details in every trip | Store boat details in `boats` and use `boat_id` in `fishing_trips`. |
| Losing a trip's catch context when reporting | Link catch rows to trips using `trip_id`. |
| Inconsistent zone descriptions across restrictions | Store zone attributes in `marine_zones` and restrictions separately. |

## 7. Referential integrity

Foreign keys enforce valid parent references. The schema uses `ON DELETE RESTRICT` for boat owners, trip boats/captains, restriction zones and catch species; it uses `ON DELETE CASCADE` for trip-owned catch, weather and alert records; and `ON DELETE SET NULL` for an alert's optional zone reference.

See `ER_DIAGRAM.md` and `DATABASE_CONSTRAINTS.md` for the relationship and constraint details.
