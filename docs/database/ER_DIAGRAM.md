# Entity–Relationship Diagram

This document describes the relational structure defined in `sql/schema.sql`. The diagram is written in Mermaid and can be rendered by GitHub.

## ER diagram

```mermaid
erDiagram
    USERS {
        int id PK
        varchar username UK
        varchar password_hash
        enum role
        timestamp created_at
    }
    FISHERMEN {
        int id PK
        varchar full_name
        varchar phone
        varchar village
        varchar license_number UK
        timestamp created_at
    }
    BOATS {
        int id PK
        varchar registration_number UK
        varchar boat_name
        int owner_id FK
        varchar boat_type
        decimal capacity_kg
        enum status
    }
    MARINE_ZONES {
        int id PK
        varchar zone_name UK
        enum zone_type
        decimal center_lat
        decimal center_lng
        decimal radius_km
        boolean active
    }
    FISHING_RESTRICTIONS {
        int id PK
        int zone_id FK
        varchar restriction_name
        date start_date
        date end_date
    }
    FISHING_TRIPS {
        int id PK
        int boat_id FK
        int captain_id FK
        datetime departure_time
        datetime return_time
        varchar departure_port
        decimal recorded_lat
        decimal recorded_lng
        enum status
    }
    FISH_SPECIES {
        int id PK
        varchar common_name UK
        varchar scientific_name
        varchar conservation_status
    }
    CATCH_RECORDS {
        int id PK
        int trip_id FK
        int species_id FK
        decimal quantity_kg
        datetime recorded_at
        decimal market_value
    }
    WEATHER_RECORDS {
        int id PK
        int trip_id FK
        datetime observed_at
        varchar condition_text
        decimal wind_speed_kmh
        decimal wave_height_m
        enum advisory_level
    }
    SAFETY_ALERTS {
        int id PK
        int trip_id FK
        int zone_id FK
        enum alert_type
        enum severity
        varchar status
        datetime resolved_at
    }

    FISHERMEN ||--o{ BOATS : owns
    FISHERMEN ||--o{ FISHING_TRIPS : captains
    BOATS ||--o{ FISHING_TRIPS : used_for
    MARINE_ZONES ||--o{ FISHING_RESTRICTIONS : has
    FISHING_TRIPS ||--o{ CATCH_RECORDS : produces
    FISH_SPECIES ||--o{ CATCH_RECORDS : identifies
    FISHING_TRIPS ||--o{ WEATHER_RECORDS : records
    FISHING_TRIPS ||--o{ SAFETY_ALERTS : may_generate
    MARINE_ZONES o|--o{ SAFETY_ALERTS : associated_with
```

`USERS` is an independent authentication entity. The other relationships are enforced through foreign keys in the schema.

## Relationship summary

| Parent | Child | Cardinality | Foreign key |
|---|---|---|---|
| `fishermen` | `boats` | One-to-many | `boats.owner_id` |
| `fishermen` | `fishing_trips` | One-to-many (captain) | `fishing_trips.captain_id` |
| `boats` | `fishing_trips` | One-to-many | `fishing_trips.boat_id` |
| `marine_zones` | `fishing_restrictions` | One-to-many | `fishing_restrictions.zone_id` |
| `fishing_trips` | `catch_records` | One-to-many | `catch_records.trip_id` |
| `fish_species` | `catch_records` | One-to-many | `catch_records.species_id` |
| `fishing_trips` | `weather_records` | One-to-many | `weather_records.trip_id` |
| `fishing_trips` | `safety_alerts` | One-to-many | `safety_alerts.trip_id` |
| `marine_zones` | `safety_alerts` | One-to-many, optional on alert | `safety_alerts.zone_id` |

## Notes

- Every table uses a surrogate integer primary key.
- Boat ownership and trip assignments are linked to fishermen; a fisherman can own boats and can also captain trips.
- Catch rows connect a trip to a fish species and store quantity and estimated value.
- An alert must refer to a trip. Its zone reference is optional and becomes `NULL` if the referenced zone is deleted (`ON DELETE SET NULL`).
- The SQL schema restricts deletion of fishermen, boats, zones and species when dependent records exist. Catch, weather and alert rows are configured to cascade when their parent trip is deleted.
- `users` is not linked to operational records in the current schema.
