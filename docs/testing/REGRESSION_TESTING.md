# Regression Testing

Regression testing checks that changes to the Flask application, templates or SQL schema do not break previously working features.

## Recommended regression checklist

After modifying the application or database, re-run the relevant tests from `TESTING.md`:

1. Application starts and `/health` responds.
2. Login, logout and role-based route restrictions work.
3. Fisherman creation, editing and deletion safeguards work.
4. Boat creation, status updates and deletion safeguards work.
5. Trip creation and status updates work.
6. Trip creation still evaluates active zones and configured date restrictions.
7. Catch validation and catch insertion work.
8. Alert filtering and status changes work.
9. Dashboard KPI totals and recent-record sections load.
10. Monthly and species reports return correct totals.
11. SQL examples and stored procedure/trigger scripts execute against the current schema.

## Database change checks

- Compare the updated `sql/schema.sql` with the deployed schema.
- Confirm every foreign key still references the intended parent key.
- Re-run seed loading only when safe for the target database; understand the effect of `INSERT IGNORE` and existing IDs.
- Check that indexes and constraints have not been unintentionally removed.

## Result recording template

| Date | Commit / version | Test IDs | Passed | Failed | Notes / evidence |
|---|---|---|---:|---:|---|
| Not yet recorded | — | — | — | — | Run the checklist and fill this table with observed results. |

No regression test execution is claimed by this document until the table is populated with actual test evidence.
