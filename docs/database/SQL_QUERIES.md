# SQL Queries Demonstrated

The executable examples are maintained in [`../../sql/queries.sql`](../../sql/queries.sql). This page explains the concepts represented there; use the SQL file as the source of truth for the complete statements.

| Query | Purpose | SQL concepts |
|---|---|---|
| 1. Total catch by species | Rank species by recorded catch quantity | `LEFT JOIN`, `SUM`, `GROUP BY`, `ORDER BY` |
| 2. Catch and estimated revenue by month | Summarize quantity and estimated value by calendar month | `DATE_FORMAT`, aggregates, grouping |
| 3. Boat trip and catch summary | Compare boats by number of trips and catch | Multiple `LEFT JOIN`s, `COUNT(DISTINCT)`, `COALESCE` |
| 4. Open safety alerts | Show alert details with vessel, captain and optional zone | Multiple joins, filtering, `FIELD` ordering |
| 5. Trips inside configured restricted/protected zone radii | Find recorded trip coordinates within a configured circular radius | Trigonometric functions, joins, coordinate-distance calculation |
| 6. Species without catch records | Find species never referenced by a catch | Correlated `NOT EXISTS` subquery |
| 7. Trips above average catch | Compare trip totals against the average trip total | Common table expression (CTE), aggregation, subquery |
| 8. Trips overlapping seasonal restrictions | Find trip dates within configured restriction periods | Date comparisons and joins |
| 9. Boat utilization by trip status | Count returned, at-sea and flagged trips for each boat | Conditional aggregation, `LEFT JOIN` |
| 10. Weather records requiring attention | List warning and danger weather observations with boat context | Joins and `IN` filtering |

## Example: total catch by species

```sql
SELECT fs.common_name, SUM(cr.quantity_kg) AS total_catch_kg
FROM fish_species fs
LEFT JOIN catch_records cr ON cr.species_id = fs.id
GROUP BY fs.id, fs.common_name
ORDER BY total_catch_kg DESC;
```

The `LEFT JOIN` keeps a species in the result even if no catch record exists for it. `SUM` calculates its total quantity.

## Example: species without recorded catches

```sql
SELECT fs.common_name
FROM fish_species fs
WHERE NOT EXISTS (
    SELECT 1
    FROM catch_records cr
    WHERE cr.species_id = fs.id
);
```

The correlated subquery checks whether at least one catch record exists for each species.

## Example: trip catch totals using a CTE

```sql
WITH trip_totals AS (
  SELECT ft.id AS trip_id, b.boat_name,
         COALESCE(SUM(cr.quantity_kg), 0) AS catch_kg
  FROM fishing_trips ft
  JOIN boats b ON b.id = ft.boat_id
  LEFT JOIN catch_records cr ON cr.trip_id = ft.id
  GROUP BY ft.id, b.boat_name
)
SELECT * FROM trip_totals
WHERE catch_kg > (SELECT AVG(catch_kg) FROM trip_totals)
ORDER BY catch_kg DESC;
```

## Important interpretation note

The zone-distance query is a circular-radius approximation around a configured center point. It is not a polygon boundary test or a legal determination. The project README documents this limitation.
