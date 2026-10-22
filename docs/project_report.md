# Project Report: Marine Fishing Fleet Management and Safe-Zone Monitoring System

## 1. Abstract

The Marine Fishing Fleet Management and Safe-Zone Monitoring System is a database-driven web application prototype that organizes fishing fleet information and helps reviewers inspect fishing-trip records against configured demonstration zones and restrictions. It stores fishermen, boats, trips, species, catch records, weather observations, marine zones and safety alerts in a relational database. A web dashboard summarizes catch trends and trip activity, while an interactive map displays recorded coordinates and illustrative zone markers. The project demonstrates relational database design, referential integrity, complex SQL queries, aggregation, authentication, and a basic alert workflow.

## 2. Problem statement

Fishing activity creates records across vessels, people, trips, catches and changing marine conditions. Keeping these records in separate spreadsheets can make it difficult to trace a catch back to a trip, identify unresolved safety reviews, compare catch trends, or review whether a recorded trip overlaps a configured restriction period. This project centralizes those records and provides a consistent interface for entering, searching and summarizing them.

## 3. Objectives

- Maintain connected records for fishermen, boats, fishing trips, species and catch quantities.
- Configure marine-zone markers and date-based restrictions.
- Generate review alerts from configured rules and recorded trip coordinates.
- Track alert status through open, reviewing and resolved states.
- Summarize catch quantity and estimated market value by species and month.
- Demonstrate SQL constraints, joins, aggregates, subqueries, CTEs, indexes, a trigger and a stored procedure.

## 4. Scope

The prototype is designed for academic demonstration with synthetic data. It is not connected to live vessel tracking, official marine charts, government databases, live weather feeds or a verified fisheries regulation service. Its circular-radius calculation is a simplified teaching example.

## 5. Modules

1. **Authentication:** login/logout and password-hash verification.
2. **Fleet management:** vessel registration and status management.
3. **Trip management:** boat/captain assignment, departure details, optional coordinates and trip status.
4. **Catch management:** species, trip, quantity and estimated market value records.
5. **Marine zones:** zone type, center coordinate, radius and active state.
6. **Safety alerts:** review and resolution workflow for configured alerts.
7. **Dashboard and reports:** KPIs, map markers, species summaries and monthly catch totals.

## 6. Database entities and relationships

- One fisherman can own multiple boats.
- One boat can be associated with many fishing trips.
- A fisherman can captain multiple fishing trips.
- One fishing trip can have multiple catch records and weather records.
- One fish species can appear in many catch records.
- A marine zone can have multiple date-based fishing restrictions.
- A trip can produce multiple safety alerts; an alert may reference a marine zone.
- Users authenticate to access the web application.

## 7. Integrity and security

Primary keys identify rows, foreign keys preserve valid relationships, unique constraints protect boat registration and zone names, and checks reject invalid catch quantities and invalid trip return times in MySQL versions that enforce those checks. Passwords are stored as hashes using Werkzeug. Routes that modify records require an authenticated organizer/admin role; read-only users can access permitted reporting pages. For production, add CSRF protection, stronger permission tests, secure cookie settings, HTTPS, rate limiting, audit trails and managed secrets.

## 8. Advanced SQL demonstrated

- Multi-table joins for alerts and trip summaries.
- `GROUP BY` and aggregate functions for monthly and species-level catch summaries.
- `LEFT JOIN` to include species or boats with no related activity.
- `NOT EXISTS` to find species without recorded catches.
- A common table expression (CTE) to compare trip catches against average catch.
- A date-overlap query for restrictions.
- A simplified Haversine-style radius query for illustrative zone checks.
- Stored procedure `sp_catch_summary` and trigger `trg_catch_positive_quantity` in `sql/routines.sql`.

## 9. Test plan

| Test | Action | Expected result |
|---|---|---|
| Login success | Enter valid demo credentials | Dashboard opens |
| Login failure | Enter invalid password | Error message shown; no login |
| Unique boat registration | Add a duplicate registration | Insert is rejected and an error is shown |
| Positive catch | Add catch with quantity above zero | Record appears in catch table and reports |
| Invalid catch | Try quantity zero or negative | Form validation or database constraint rejects it |
| Zone alert | Create a trip point within a synthetic restricted/protected radius | An alert is created for manual review |
| Restriction overlap | Trip date falls within configured restriction dates and point is in the configured zone | Seasonal restriction alert is created |
| Resolve alert | Set an alert to resolved | Alert status and resolution timestamp update |
| Report aggregation | Add multiple catches for one species/month | Totals aggregate correctly |
| Role restriction | Sign in as a viewer and submit a modification request | Modification route returns 403 |

## 10. Limitations and future work

The application uses illustrative zone circles and sample restrictions, so it must not be treated as an official safety or compliance tool. Future work can add verified polygon boundaries, geospatial indexes, actual GPS ingestion, live marine weather data, CSV exports, pagination, richer audit history, automated tests, Docker-based deployment and additional CRUD workflows.

## 11. Conclusion

The project demonstrates how a relational database and web interface can centralize fleet records, link catch data to trips, and support review of configured safety conditions. It provides a practical setting for presenting normalization, relationships, constraints, complex SQL, triggers, stored procedures, authentication and dashboard reporting in a DBMS course.
