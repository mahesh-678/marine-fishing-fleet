# Current Limitations and Future Improvements

## Current limitations

1. **Illustrative marine data:** seed zones, coordinates, restriction periods, weather and catch values are sample data, not official government datasets.
2. **Simplified geofencing:** the application checks a circular radius around a zone center. It does not evaluate official polygon boundaries or account for GPS uncertainty.
3. **No live GPS feed:** trip coordinates are entered as a record; the application does not continuously track vessels.
4. **No live weather integration:** weather observations exist in the database and sample data, but the application does not currently expose a weather-entry workflow or automatically derive weather alerts from those rows.
5. **Limited species administration:** species are stored in the database and used in catch forms/reports; a full species CRUD page is not currently implemented.
6. **Limited audit history:** the current schema does not include a comprehensive audit log of who changed each operational record.
7. **Prototype security posture:** additional CSRF, rate limiting, authorization testing and production monitoring should be implemented before real deployment.
8. **Reporting scope:** reports summarize stored catch quantities and estimated values; they are not accounting or verified sales reports.

## Future improvements

- Import verified marine boundaries and applicable restrictions from authoritative sources.
- Use polygon geofencing and spatial indexes (for example, a suitable MySQL spatial implementation or PostGIS).
- Integrate authenticated GPS telemetry and timestamped vessel tracks.
- Integrate a trusted marine weather provider and define reviewed weather-alert rules.
- Add species administration, pagination, CSV export and richer search/filtering.
- Add audit history, automated integration tests, backups and restore procedures.
- Introduce a tested role/permission matrix and production security controls.
- Add repeatable load and query benchmarks using representative data volumes.

## Intended use

This project is an academic DBMS prototype. It must not be used as a navigation, emergency response, enforcement or legal compliance system.
