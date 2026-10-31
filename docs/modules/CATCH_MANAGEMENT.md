# Catch and Species Management

## Purpose

The catch module records the species and quantity associated with a fishing trip, along with an estimated market value.

## Related tables

- `fish_species` stores common name, optional scientific name, conservation status and breeding-season notes.
- `catch_records` stores the trip, species, quantity in kilograms, record timestamp, estimated market value and notes.

Each catch record references one trip and one species. A trip can have multiple catch records, and a species can appear in multiple catch records.

## Application workflow

The `/catches` page is available to authenticated admin/organizer users. The form selects an existing trip and species, then records quantity and market value. The handler rejects a quantity less than or equal to zero and a negative market value before saving.

## Database validation

The schema declares `CHECK (quantity_kg > 0)` and `CHECK (market_value >= 0)`. The SQL routines file also defines a `BEFORE INSERT` trigger named `trg_catch_positive_quantity` to reject non-positive quantities when that script has been installed.

## Reporting

Catch data is summarized by species and by month on `/reports`. The SQL examples in `sql/queries.sql` include total catch, monthly catch and estimated value, and trip-level catch comparisons.

## Interpretation

`market_value` is an estimated amount entered with the catch record. It is not a verified sale transaction or live market price.
