# Dashboard and Reporting Logic

## Dashboard metrics

The authenticated `/dashboard` page calculates the following values from the database:

| Metric | Calculation |
|---|---|
| Total fishermen | Count of rows in `fishermen` |
| Total boats | Count of rows in `boats` |
| Active trips | Count of trips with status `planned` or `at_sea` |
| Open alerts | Count of alerts whose status is not `resolved` |
| Monitored zones | Count of zones with `active = true` |
| Total catch | Sum of `catch_records.quantity_kg`, defaulting to zero when there are no rows |

The dashboard also loads up to six most recent alerts and trips and prepares a species catch summary for a chart.

## Reports page

The authenticated `/reports` page calculates:

1. Monthly catch quantity and estimated market value, grouped by `YYYY-MM` from `catch_records.recorded_at`.
2. Catch quantity and estimated market value by species. The species summary uses an outer join so a species with no catch records can still appear with zero totals.

## SQL reference

`sql/queries.sql` contains additional report queries, including catch totals by species, monthly value, boat utilization, trip totals and weather records requiring attention.

## Interpretation

These reports summarize the records stored in the application. Their accuracy depends on the completeness and correctness of entered trip and catch data. Market value is user-entered estimated value, not verified revenue.
