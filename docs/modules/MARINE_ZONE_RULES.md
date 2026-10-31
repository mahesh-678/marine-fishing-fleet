# Marine Zones and Fishing Restrictions

## Marine zones

The `marine_zones` table stores a unique zone name, type, description, center latitude/longitude, radius in kilometres and active flag. Supported types are:

- `permitted`
- `restricted`
- `protected`

The application provides the `/zones` page for adding zones and toggling their active state. New zone coordinates are checked against latitude and longitude ranges, and the radius must be greater than zero.

## Date-based restrictions

The `fishing_restrictions` table stores a named restriction, its zone, start date, end date and optional notes. A database CHECK requires the end date to be on or after the start date.

During trip creation, the application checks whether the trip's departure date falls within the configured date range for a restriction associated with an active zone, provided the trip coordinate is inside that zone's configured radius.

## Data provenance and limitations

The included seed records explicitly describe zones and restriction dates as illustrative or synthetic examples. They are not authoritative government boundaries or current regulations. Replace them only with verified, appropriately licensed sources before considering any operational use.
