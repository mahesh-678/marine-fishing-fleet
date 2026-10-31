# Indexing and Query Optimization

## Indexes declared in the schema

`sql/schema.sql` creates the following secondary indexes:

| Index | Table and column(s) | Queries it may support |
|---|---|---|
| `idx_trip_departure` | `fishing_trips(departure_time)` | Date-range trip searches and ordering by departure time |
| `idx_trip_status` | `fishing_trips(status)` | Filtering trips by operational status |
| `idx_catch_recorded_at` | `catch_records(recorded_at)` | Date-range catch reports |
| `idx_alert_status` | `safety_alerts(status)` | Filtering open, reviewing or resolved alerts |
| `idx_restriction_dates` | `fishing_restrictions(start_date, end_date)` | Restriction date-window filtering |

Primary keys and UNIQUE constraints also create indexes in MySQL.

## Why indexes are useful

An index can reduce the number of rows MySQL must inspect for selective filters, joins or ordering. Indexes also require storage and add work to `INSERT`, `UPDATE` and `DELETE` operations. They should be chosen based on actual query patterns rather than added to every column.

## How to benchmark a query

Use the same database, data volume and query parameters when comparing plans. In a MySQL client, run:

```sql
EXPLAIN
SELECT *
FROM fishing_trips
WHERE status = 'at_sea';
```

For supported MySQL 8 versions, `EXPLAIN ANALYZE` executes the query and reports actual iterator timing:

```sql
EXPLAIN ANALYZE
SELECT *
FROM fishing_trips
WHERE departure_time >= '2026-10-01';
```

Record the database version, approximate row counts, query, plan and measured execution time. Repeat runs and report a median rather than relying on one measurement.

## Benchmark status

No measured execution-time results are included in this document yet. Add real results after running the benchmark queries against the project's actual Aiven/MySQL database. Do not treat example `EXPLAIN` output as a measured performance improvement.
