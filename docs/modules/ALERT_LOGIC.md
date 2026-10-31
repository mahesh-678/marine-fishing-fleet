# Safety Alert Logic

## Purpose

The prototype creates review alerts when a recorded trip coordinate falls within a configured restricted/protected zone radius or when the trip date overlaps a configured restriction period.

## Inputs

- Trip departure date/time and optional recorded latitude/longitude (`fishing_trips`).
- Active zone center coordinates, zone type and radius (`marine_zones`).
- Restriction date ranges associated with zones (`fishing_restrictions`).

## Coordinate distance

The Flask application uses the Haversine formula with an Earth-radius approximation of 6,371 km to calculate the great-circle distance between the trip coordinate and the zone center. The coordinate is considered inside the configured circle when:

```text
distance_km <= zone.radius_km
```

## Alert rules implemented in `evaluate_trip()`

1. If either trip coordinate is missing, the function returns without performing zone checks.
2. It examines active marine zones.
3. If the point is inside a zone whose type is `restricted` or `protected`, it creates a `restricted_zone` alert with `high` severity unless one already exists for the same trip, zone and alert type. The trip is marked `flagged`.
4. If the point is inside a zone and the trip departure date falls between a restriction's start and end dates (inclusive), it creates a `seasonal_ban` alert with `high` severity unless one already exists for the same trip, zone and alert type. The trip is marked `flagged`.
5. The application commits the trip and any generated alerts together in the trip-creation handler.

The date-overlap check is performed for restrictions associated with an active zone; it is not limited to restricted/protected zone types.

## Alert lifecycle

`safety_alerts.status` supports `open`, `reviewing` and `resolved`. The `/alerts` page allows authenticated users to view alerts and filter by status. Admin/organizer users can update status. When an alert is resolved, `resolved_at` is set to the current application time; moving it to another status clears that timestamp.

## Alert types in the schema

`restricted_zone`, `seasonal_ban`, `weather` and `manual_review` are allowed enum values. The current automatic `evaluate_trip()` logic creates the first two types. Weather alerts in the seed data are illustrative records; this function does not currently generate alerts from `weather_records` automatically.

## Safety limitation

This is a classroom demonstration based on circular radii and sample zone data. It is not an official geofence, legal compliance assessment, navigation aid or emergency-warning system. Official boundaries, verified GPS, uncertainty handling and regulatory review would be required before any real-world use.
