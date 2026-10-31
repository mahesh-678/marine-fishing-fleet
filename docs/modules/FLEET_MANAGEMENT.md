# Fleet Management

## Purpose

The fleet module maintains fisherman/boat owner records and the boats registered to them.

## Fishermen records

The `fishermen` table stores a person's name, village, optional phone number and optional unique license number. The Flask application provides create, edit and delete actions through `/fishermen` and its related POST routes. A fisherman cannot be deleted through the application while that person is referenced as a boat owner or trip captain.

## Boat records

The `boats` table stores registration number, boat name, owner, boat type, carrying capacity and operational status. `owner_id` references `fishermen.id`. The application allows a boat to be registered, its status to be changed among `active`, `maintenance` and `inactive`, and deletion when it has no associated fishing trips.

## Integrity rules

- Boat registration numbers must be unique.
- A boat must reference an existing fisherman.
- Boat capacity must be positive in the Flask registration handler.
- Boats with existing trips are protected from deletion by the application.

## Application pages

- `/fishermen` — list and manage fishermen/owners.
- `/boats` — list and manage boats.

Both routes require an authenticated `admin` or `organizer` role according to the `admin_required` decorator.
