# Project Documentation

This folder contains technical documentation for the Marine Fishing Fleet Management and Safe-Zone Monitoring System.

## Database design

- [ER Diagram](database/ER_DIAGRAM.md)
- [Normalisation](database/NORMALISATION.md)
- [Data Dictionary](database/DATA_DICTIONARY.md)
- [Database Constraints](database/DATABASE_CONSTRAINTS.md)
- [SQL Queries](database/SQL_QUERIES.md)
- [Indexing and Optimization](database/INDEXING_AND_OPTIMIZATION.md)

## Application modules

- [Fleet Management](modules/FLEET_MANAGEMENT.md)
- [Fishing Trips](modules/FISHING_TRIPS.md)
- [Catch Management](modules/CATCH_MANAGEMENT.md)
- [Alert Logic](modules/ALERT_LOGIC.md)
- [Marine Zone Rules](modules/MARINE_ZONE_RULES.md)
- [Reporting Logic](modules/REPORTING_LOGIC.md)

## Testing and technical notes

- [Testing Guide](testing/TESTING.md)
- [Regression Testing](testing/REGRESSION_TESTING.md)
- [Database Benchmarks](testing/BENCHMARKS.md)
- [Security](technical/SECURITY.md)
- [Data Integrity](technical/DATA_INTEGRITY.md)
- [Limitations](technical/LIMITATIONS.md)

The documentation is based on the current repository files, especially `app.py`, `sql/schema.sql`, `sql/seed.sql`, `sql/queries.sql`, `sql/routines.sql` and `README.md`. Where a test or benchmark has not yet been executed, the relevant page explicitly identifies it as a plan rather than reporting invented results.
