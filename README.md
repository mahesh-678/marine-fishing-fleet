# Marine Fishing Fleet Management and Safe-Zone Monitoring System

A full-stack DBMS project prototype for recording fishermen, boats, fishing trips, catch records, marine-zone markers, configured restrictions, weather observations and safety alerts.

## Technology stack

- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript
- **Dashboard charts:** Chart.js
- **Interactive map:** Leaflet + OpenStreetMap tiles
- **Backend:** Python 3, Flask
- **Database:** MySQL 8+
- **Authentication:** Flask-Login with hashed passwords
- **SQL concepts:** primary/foreign keys, constraints, indexes, joins, aggregates, subqueries, CTE, trigger, stored procedure

## Features

- Login-protected dashboard with fleet, trip, alert and catch KPIs.
- Boat register with operational-status updates.
- Fishing-trip register with optional latitude/longitude and status updates.
- Basic radius-based check of trip coordinates against configured restricted/protected demo zones.
- Catch register linked to trip and fish species.
- Marine-zone management and enable/disable control.
- Safety-alert review workflow: open, reviewing, resolved.
- Interactive map showing configured zone circles and recorded trip points.
- Reports for catch quantity and estimated market value by month and species.
- SQL examples, sample data, a stored procedure and a validation trigger.

## Important data and safety limitations

This is an educational prototype, not a navigation or enforcement tool. The included marine zones, restrictions, coordinates, dates, weather and catch records are **illustrative sample data**. They are not official government boundaries or current fishing regulations. The radius check uses circles around a center point; it does not perform authoritative polygon geofencing, account for GPS uncertainty, or determine legal violations. Do not use it for real-world navigation, enforcement, or safety decisions. For real deployment, obtain authoritative datasets and regulatory guidance, use verified geospatial boundaries (for example, PostGIS or MySQL spatial features), add audit logging, robust authorization, backups, HTTPS and operational review.

## Requirements

- Python 3.10 or newer
- MySQL 8.0 or newer
- A web browser
- Internet access for CDN assets and OpenStreetMap map tiles (or self-host those assets for offline use)

## Setup on Windows PowerShell

### 1. Create the database

Install and start MySQL, then open MySQL Workbench or a MySQL terminal and run these files in order:

1. `sql/schema.sql`
2. `sql/seed.sql`

Example from a terminal where `mysql` is on PATH:

```powershell
mysql -u root -p < sql/schema.sql
mysql -u root -p < sql/seed.sql
```

### 2. Configure environment variables

Copy `.env.example` to `.env` and edit the MySQL credentials. For example:

```env
SECRET_KEY=replace-with-a-long-random-secret
FLASK_DEBUG=1
DB_HOST=localhost
DB_PORT=3306
DB_NAME=marine_fleet_db
DB_USER=root
DB_PASSWORD=your_mysql_password
ADMIN_USERNAME=admin
ADMIN_PASSWORD=ChangeMe123!
```

Use a unique secret and strong admin password. The values above are for a local demo only. Never commit `.env` to a public repository.

### 3. Create a virtual environment and install packages

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, you can run the environment's Python directly:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 4. Start the app

```powershell
python app.py
```

Open <http://127.0.0.1:5000>.

The application creates any missing ORM tables and creates an initial admin account using `ADMIN_USERNAME` and `ADMIN_PASSWORD` if no matching user exists. The SQL scripts remain the reference for the full schema, sample data and advanced SQL examples. If you change the schema later, update the SQL scripts and model definitions together.


## Deployment (Render + external MySQL)

This app is configured for deployment as a Python web service. It requires a **reachable MySQL 8 database**; Render does not provide a MySQL database in this service configuration. Create a MySQL database with a provider that allows connections from your web service, run `sql/schema.sql` and `sql/seed.sql` against it, then deploy this folder as a Render Web Service.

1. Push the contents of this project folder to a GitHub repository. Do not commit `.env`.
2. In Render, create a Web Service from that repository. Set the root directory to the folder containing `app.py` if the app is nested in the repository.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
5. Add environment variables: `APP_ENV=production`, `FLASK_DEBUG=0`, a long random `SECRET_KEY`, `DB_HOST`, `DB_PORT=3306`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `ADMIN_USERNAME`, and a strong `ADMIN_PASSWORD`. Use the database provider's actual connection values.
6. Set health check path to `/health`.
7. After the first successful deployment, open the public URL and sign in using the admin credentials you configured.

`render.yaml` is included as a starting point. If you use Render Blueprint deployment, supply the external database values when prompted. Keep the MySQL server's network access restricted to the web service/provider's supported connection method.

The UI has been simplified for review by removing repeated prototype disclaimers and the on-screen demo password. The sample marine-zone records remain illustrative; keep that limitation in the project documentation and do not present the system as an official navigation or enforcement service.

## Setup on macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your local MySQL credentials
mysql -u root -p < sql/schema.sql
mysql -u root -p < sql/seed.sql
python app.py
```

## Login

Set `ADMIN_USERNAME` and `ADMIN_PASSWORD` in `.env` before first startup. The application creates the initial administrator only when `ADMIN_PASSWORD` is configured and no account with that username exists. Do not use a default password on a public deployment.

## Suggested demo flow

1. Sign in and explain the dashboard KPIs.
2. Open **Boats** and demonstrate vessel status updates.
3. Open **Fishing trips** and create a trip with coordinates near one of the sample zones.
4. Show how the configured radius check can create a safety alert. Verify the generated alert text and explain that it is only a demonstration.
5. Add a catch record for that trip.
6. Open **Reports** and explain grouping and aggregation by species/month.
7. Open `sql/queries.sql` to demonstrate joins, `NOT EXISTS`, CTEs and a distance approximation.
8. Open `sql/routines.sql` to demonstrate the stored procedure and trigger.

## Folder structure

```text
marine_fishing_fleet/
├── app.py
├── requirements.txt
├── .env.example
├── README.md
├── docs/
│   └── project_report.md
├── sql/
│   ├── schema.sql
│   ├── seed.sql
│   ├── queries.sql
│   └── routines.sql
├── static/
│   ├── css/style.css
│   └── js/app.js
└── templates/
    ├── base.html
    ├── login.html
    ├── dashboard.html
    ├── boats.html
    ├── trips.html
    ├── catches.html
    ├── zones.html
    ├── alerts.html
    ├── reports.html
    └── error.html
```

## Troubleshooting

- **`Access denied for user`:** check `DB_USER` and `DB_PASSWORD` in `.env`.
- **`Unknown database`:** run `sql/schema.sql` first.
- **No demo records:** run `sql/seed.sql` after the schema script.
- **Cannot connect to MySQL:** confirm the MySQL service is running and `DB_PORT` is correct.
- **Map is blank:** the browser needs internet access to load OpenStreetMap tiles and the Leaflet CDN; check the browser console.
- **Duplicate registration / zone:** registration numbers and zone names must be unique.
- **No fishermen/species in dropdowns:** load `sql/seed.sql` or add records to the relevant tables.

## Project scope extensions

Possible future work includes CRUD for fishermen and species, recording return times and weather in the UI, official polygon geofencing, CSV export, password reset, audit logs, pagination, automated tests, Docker deployment and a production-grade role/permission matrix.
