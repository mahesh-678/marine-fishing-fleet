# Testing Guide and Test Cases

This file is a proposed manual test plan derived from the current routes, models and SQL schema. It does not claim that these tests have already been executed. Record actual results and evidence when testing the deployed or local application.

## Preconditions

- MySQL database is available and configured through environment variables.
- `sql/schema.sql` and `sql/seed.sql` have been applied as appropriate.
- Python dependencies are installed and the Flask application starts.
- A test admin/organizer account and a viewer account are available if role checks are being tested.

## Functional test cases

| ID | Test | Steps | Expected result |
|---|---|---|---|
| T01 | Health endpoint | Open `/health` | JSON response indicates `status: ok` |
| T02 | Login success | Submit valid username/password | User is redirected to dashboard |
| T03 | Login failure | Submit invalid credentials | Login page displays an error |
| T04 | Add fisherman | Submit required name and village | New fisherman appears in list |
| T05 | Duplicate license | Submit a license number already used | Database uniqueness prevents duplicate; application reports an error |
| T06 | Add boat | Submit unique registration and valid owner | Boat appears in boat list |
| T07 | Boat status | Change status among allowed values | Updated status is saved |
| T08 | Add trip | Select an active boat and captain; enter departure data | Trip is saved |
| T09 | Trip with zone overlap | Use test coordinates inside a synthetic restricted/protected radius | Appropriate demo alert is generated and trip is flagged |
| T10 | Add catch | Enter positive quantity and non-negative value | Catch record is saved |
| T11 | Invalid catch | Submit zero/negative quantity or negative value | Application rejects the input |
| T12 | Toggle zone | Change active state | Zone active state changes |
| T13 | Resolve alert | Change alert status to resolved | Status and resolution timestamp are updated |
| T14 | Reports | Open `/reports` with catch data | Monthly and species summaries are displayed |
| T15 | Viewer authorization | Attempt a route protected by `admin_required` as viewer | Request is denied with 403 |

## Database tests

Run the queries in `sql/queries.sql` and verify that:

- joins return records with the expected related boat, captain, trip and species;
- aggregate totals agree with manually summed sample rows;
- `NOT EXISTS` returns only species with no catch record;
- invalid foreign-key references are rejected;
- declared CHECK and UNIQUE constraints behave as expected on the deployed MySQL version.

## Evidence

For each executed test, record the test ID, date, environment, input data, actual result, pass/fail status and screenshot or log reference. Do not mark a test as passed until it has been run.
