# Database Query Benchmarks

## Objective

Measure how the current MySQL schema and indexes perform for representative fleet-management queries. This document is a benchmark plan; no measured timings are asserted here.

## Existing indexes

The current schema defines:

- `idx_trip_departure` on `fishing_trips(departure_time)`;
- `idx_trip_status` on `fishing_trips(status)`;
- `idx_catch_recorded_at` on `catch_records(recorded_at)`;
- `idx_alert_status` on `safety_alerts(status)`;
- `idx_restriction_dates` on `fishing_restrictions(start_date, end_date)`.

## Suggested benchmark queries

Run `EXPLAIN` for each query first. If supported by the MySQL version, use `EXPLAIN ANALYZE` to obtain execution details.

```sql
EXPLAIN ANALYZE
SELECT id, boat_id, captain_id, departure_time, status
FROM fishing_trips
WHERE status = 'at_sea';
```

```sql
EXPLAIN ANALYZE
SELECT id, trip_id, species_id, quantity_kg, market_value
FROM catch_records
WHERE recorded_at >= '2026-10-01'
  AND recorded_at < '2026-11-01';
```

```sql
EXPLAIN ANALYZE
SELECT id, trip_id, alert_type, severity, created_at
FROM safety_alerts
WHERE status = 'open';
```

## Measurement method

1. Record MySQL version and database host/plan (avoid publishing credentials or host secrets).
2. Record approximate row counts for each relevant table.
3. Run each query several times under comparable conditions.
4. Record execution plan, actual time and rows examined where available.
5. Report the median of repeated runs and note cache/warm-up conditions.
6. Compare plans before and after any index change using the same data and query.

## Results table

| Query | Table row count | Index/plan observed | Run 1 | Run 2 | Run 3 | Median | Notes |
|---|---:|---|---:|---:|---:|---:|---|
| Trip status filter | To measure | To measure | — | — | — | — | — |
| Catch date range | To measure | To measure | — | — | — | — | — |
| Open alert filter | To measure | To measure | — | — | — | — | — |

Do not claim a speed-up unless both measurements were performed under comparable conditions. Small sample tables may not show a meaningful index advantage.
