# Fishing Trip Management

## Purpose

A fishing trip links a boat to a fisherman acting as captain and records the planned or actual trip details.

## Stored information

The `fishing_trips` table includes:

- `boat_id` and `captain_id` foreign keys;
- departure and optional return date/time;
- departure port;
- optional recorded latitude and longitude;
- status (`planned`, `at_sea`, `returned` or `flagged`);
- notes and creation timestamp.

## Workflow in the application

1. An authenticated admin/organizer opens `/trips`.
2. The form selects an active boat and a fisherman as captain.
3. Departure time and port are required; coordinates are optional.
4. The application creates the trip and evaluates the supplied coordinates against active configured zones and date restrictions.
5. Any generated alerts are saved with the trip; the trip may be marked `flagged`.
6. An admin/organizer can update trip status. When status is changed to `returned`, the application sets `return_time` if it is not already populated.

## Validation and integrity

- The selected boat and captain must exist because of foreign keys.
- `return_time` must be null or no earlier than `departure_time`.
- A trip coordinate is only evaluated when both latitude and longitude are supplied.

## Scope note

The application currently records a coordinate on the trip. It does not ingest a continuous live GPS track or provide real-time vessel tracking.
