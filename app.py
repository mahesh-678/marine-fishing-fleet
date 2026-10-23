import os
from datetime import datetime, date
from decimal import Decimal
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from sqlalchemy import func, case, URL
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'local-development-only-change-me')
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = os.getenv('APP_ENV', 'development').lower() == 'production'

if os.getenv('DATABASE_URL'):
    db_url = os.getenv('DATABASE_URL')
else:
    # URL.create safely escapes special characters (such as @) in DB_PASSWORD.
    db_url = URL.create(
        drivername='mysql+pymysql',
        username=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', '3306')),
        database=os.getenv('DB_NAME', 'marine_fleet_db'),
        query={'charset': 'utf8mb4'},
    )
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'connect_args': {
        'ssl': {
            'ca': os.getenv('DB_SSL_CA')
        } if os.getenv('DB_SSL_CA') else {}
    }
}

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin', 'organizer', 'viewer'), nullable=False, default='organizer')
    created_at = db.Column(db.DateTime, server_default=func.current_timestamp())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Fisherman(db.Model):
    __tablename__ = 'fishermen'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(25))
    village = db.Column(db.String(100), nullable=False)
    license_number = db.Column(db.String(60), unique=True)
    boats = db.relationship('Boat', back_populates='owner')


class Boat(db.Model):
    __tablename__ = 'boats'
    id = db.Column(db.Integer, primary_key=True)
    registration_number = db.Column(db.String(40), unique=True, nullable=False)
    boat_name = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('fishermen.id'), nullable=False)
    boat_type = db.Column(db.String(60), nullable=False)
    capacity_kg = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    status = db.Column(db.Enum('active', 'maintenance', 'inactive'), nullable=False, default='active')
    owner = db.relationship('Fisherman', back_populates='boats')
    trips = db.relationship('FishingTrip', back_populates='boat')


class MarineZone(db.Model):
    __tablename__ = 'marine_zones'
    id = db.Column(db.Integer, primary_key=True)
    zone_name = db.Column(db.String(120), nullable=False, unique=True)
    zone_type = db.Column(db.Enum('permitted', 'restricted', 'protected'), nullable=False)
    description = db.Column(db.Text)
    center_lat = db.Column(db.Numeric(10, 7), nullable=False)
    center_lng = db.Column(db.Numeric(10, 7), nullable=False)
    radius_km = db.Column(db.Numeric(8, 2), nullable=False, default=1)
    active = db.Column(db.Boolean, nullable=False, default=True)


class FishingRestriction(db.Model):
    __tablename__ = 'fishing_restrictions'
    id = db.Column(db.Integer, primary_key=True)
    zone_id = db.Column(db.Integer, db.ForeignKey('marine_zones.id'), nullable=False)
    restriction_name = db.Column(db.String(150), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text)
    zone = db.relationship('MarineZone')


class FishingTrip(db.Model):
    __tablename__ = 'fishing_trips'
    id = db.Column(db.Integer, primary_key=True)
    boat_id = db.Column(db.Integer, db.ForeignKey('boats.id'), nullable=False)
    captain_id = db.Column(db.Integer, db.ForeignKey('fishermen.id'), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    return_time = db.Column(db.DateTime)
    departure_port = db.Column(db.String(120), nullable=False)
    recorded_lat = db.Column(db.Numeric(10, 7))
    recorded_lng = db.Column(db.Numeric(10, 7))
    status = db.Column(db.Enum('planned', 'at_sea', 'returned', 'flagged'), nullable=False, default='planned')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=func.current_timestamp())
    boat = db.relationship('Boat', back_populates='trips')
    captain = db.relationship('Fisherman')
    catches = db.relationship('CatchRecord', back_populates='trip', cascade='all, delete-orphan')
    weather = db.relationship('WeatherRecord', back_populates='trip', cascade='all, delete-orphan')
    alerts = db.relationship('SafetyAlert', back_populates='trip', cascade='all, delete-orphan')


class FishSpecies(db.Model):
    __tablename__ = 'fish_species'
    id = db.Column(db.Integer, primary_key=True)
    common_name = db.Column(db.String(100), unique=True, nullable=False)
    scientific_name = db.Column(db.String(150))
    conservation_status = db.Column(db.String(60), default='Not assessed')
    breeding_season_notes = db.Column(db.Text)


class CatchRecord(db.Model):
    __tablename__ = 'catch_records'
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('fishing_trips.id'), nullable=False)
    species_id = db.Column(db.Integer, db.ForeignKey('fish_species.id'), nullable=False)
    quantity_kg = db.Column(db.Numeric(10, 2), nullable=False)
    recorded_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    market_value = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    notes = db.Column(db.Text)
    trip = db.relationship('FishingTrip', back_populates='catches')
    species = db.relationship('FishSpecies')


class WeatherRecord(db.Model):
    __tablename__ = 'weather_records'
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('fishing_trips.id'), nullable=False)
    observed_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    condition_text = db.Column(db.String(80), nullable=False)
    wind_speed_kmh = db.Column(db.Numeric(6, 2), default=0)
    wave_height_m = db.Column(db.Numeric(5, 2), default=0)
    advisory_level = db.Column(db.Enum('normal', 'caution', 'warning', 'danger'), nullable=False, default='normal')
    notes = db.Column(db.Text)
    trip = db.relationship('FishingTrip', back_populates='weather')


class SafetyAlert(db.Model):
    __tablename__ = 'safety_alerts'
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('fishing_trips.id'), nullable=False)
    zone_id = db.Column(db.Integer, db.ForeignKey('marine_zones.id'))
    alert_type = db.Column(db.Enum('restricted_zone', 'seasonal_ban', 'weather', 'manual_review'), nullable=False)
    severity = db.Column(db.Enum('low', 'medium', 'high', 'critical'), nullable=False, default='medium')
    message = db.Column(db.String(500), nullable=False)
    status = db.Column(db.Enum('open', 'reviewing', 'resolved'), nullable=False, default='open')
    created_at = db.Column(db.DateTime, server_default=func.current_timestamp())
    resolved_at = db.Column(db.DateTime)
    trip = db.relationship('FishingTrip', back_populates='alerts')
    zone = db.relationship('MarineZone')


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if current_user.role not in ('admin', 'organizer'):
            abort(403)
        return view(*args, **kwargs)
    return wrapped


@app.context_processor
def inject_globals():
    return {'current_year': datetime.now().year}


@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Welcome back.', 'success')
            return redirect(request.args.get('next') or url_for('dashboard'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been signed out.', 'info')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    total_fishermen = Fisherman.query.count()
    total_boats = Boat.query.count()
    active_trips = FishingTrip.query.filter(FishingTrip.status.in_(['planned', 'at_sea'])).count()
    open_alerts = SafetyAlert.query.filter(SafetyAlert.status != 'resolved').count()
    monitored_zones = MarineZone.query.filter_by(active=True).count()
    total_catch = db.session.query(func.coalesce(func.sum(CatchRecord.quantity_kg), 0)).scalar() or 0
    recent_alerts = SafetyAlert.query.order_by(SafetyAlert.created_at.desc()).limit(6).all()
    recent_trips = FishingTrip.query.order_by(FishingTrip.departure_time.desc()).limit(6).all()
    species_rows = db.session.query(FishSpecies.common_name, func.coalesce(func.sum(CatchRecord.quantity_kg), 0).label('kg')).outerjoin(CatchRecord, CatchRecord.species_id == FishSpecies.id).group_by(FishSpecies.id, FishSpecies.common_name).order_by(func.sum(CatchRecord.quantity_kg).desc()).all()
    chart_labels = [r[0] for r in species_rows]
    chart_values = [float(r[1] or 0) for r in species_rows]
    return render_template('dashboard.html', total_fishermen=total_fishermen, total_boats=total_boats,
                           active_trips=active_trips, open_alerts=open_alerts, monitored_zones=monitored_zones,
                           total_catch=float(total_catch), recent_alerts=recent_alerts,
                           recent_trips=recent_trips, chart_labels=chart_labels, chart_values=chart_values)


@app.route('/fishermen', methods=['GET', 'POST'])
@admin_required
def fishermen():
    if request.method == 'POST':
        try:
            full_name = request.form.get('full_name', '').strip()
            phone = request.form.get('phone', '').strip() or None
            village = request.form.get('village', '').strip()
            license_number = request.form.get('license_number', '').strip() or None

            if not full_name or not village:
                raise ValueError('Full name and village are required.')

            fisherman = Fisherman(
                full_name=full_name,
                phone=phone,
                village=village,
                license_number=license_number
            )

            db.session.add(fisherman)
            db.session.commit()
            flash('Owner added successfully.', 'success')
            return redirect(url_for('fishermen'))

        except Exception as exc:
            db.session.rollback()
            flash(f'Could not add owner. Check the details and license number. ({exc})', 'danger')

    owners = Fisherman.query.order_by(Fisherman.full_name).all()
    return render_template('fishermen.html', owners=owners)


@app.route('/fishermen/<int:fisherman_id>/edit', methods=['POST'])
@admin_required
def edit_fisherman(fisherman_id):
    fisherman = db.get_or_404(Fisherman, fisherman_id)

    try:
        full_name = request.form.get('full_name', '').strip()
        village = request.form.get('village', '').strip()
        phone = request.form.get('phone', '').strip() or None
        license_number = request.form.get('license_number', '').strip() or None

        if not full_name or not village:
            raise ValueError('Full name and village are required.')

        fisherman.full_name = full_name
        fisherman.village = village
        fisherman.phone = phone
        fisherman.license_number = license_number

        db.session.commit()
        flash('Owner details updated successfully.', 'success')

    except Exception as exc:
        db.session.rollback()
        flash(f'Could not update owner. Check the details and license number. ({exc})', 'danger')

    return redirect(url_for('fishermen'))


@app.route('/fishermen/<int:fisherman_id>/delete', methods=['POST'])
@admin_required
def delete_fisherman(fisherman_id):
    fisherman = db.get_or_404(Fisherman, fisherman_id)

    # Prevent deleting an owner referenced by a boat or fishing trip.
    has_boats = Boat.query.filter_by(owner_id=fisherman.id).first()
    has_trips = FishingTrip.query.filter_by(captain_id=fisherman.id).first()

    if has_boats or has_trips:
        flash(
            'This owner cannot be deleted because they are associated with a boat or fishing trip. Edit the owner instead.',
            'warning'
        )
        return redirect(url_for('fishermen'))

    db.session.delete(fisherman)
    db.session.commit()
    flash('Owner deleted successfully.', 'success')
    return redirect(url_for('fishermen'))



@app.route('/boats', methods=['GET', 'POST'])
@admin_required
def boats():
    if request.method == 'POST':
        try:
            boat = Boat(registration_number=request.form['registration_number'].strip(),
                        boat_name=request.form['boat_name'].strip(), owner_id=int(request.form['owner_id']),
                        boat_type=request.form['boat_type'].strip(), capacity_kg=Decimal(request.form['capacity_kg']),
                        status=request.form.get('status', 'active'))
            if boat.capacity_kg <= 0:
                raise ValueError('Capacity must be greater than zero.')
            db.session.add(boat); db.session.commit()
            flash('Boat added successfully.', 'success')
            return redirect(url_for('boats'))
        except Exception as exc:
            db.session.rollback(); flash(f'Could not add boat. Check required fields and unique registration. ({exc})', 'danger')
    return render_template('boats.html', boats=Boat.query.order_by(Boat.id.desc()).all(), fishermen=Fisherman.query.order_by(Fisherman.full_name).all())


@app.route('/boats/<int:boat_id>/status', methods=['POST'])
@admin_required
def boat_status(boat_id):
    boat = db.get_or_404(Boat, boat_id)
    new_status = request.form.get('status')
    if new_status not in ('active', 'maintenance', 'inactive'):
        abort(400)
    boat.status = new_status; db.session.commit()
    flash('Boat status updated.', 'success')
    return redirect(url_for('boats'))

@app.route('/boats/<int:boat_id>/delete', methods=['POST'])
@admin_required
def delete_boat(boat_id):
    boat = db.get_or_404(Boat, boat_id)

    # Prevent deletion if the boat has existing fishing trips.
    if FishingTrip.query.filter_by(boat_id=boat.id).first():
        flash(
            'This boat cannot be deleted because it has associated fishing trips.',
            'warning'
        )
        return redirect(url_for('boats'))

    db.session.delete(boat)
    db.session.commit()

    flash(f'Boat "{boat.boat_name}" deleted successfully.', 'success')
    return redirect(url_for('boats'))


@app.route('/trips', methods=['GET', 'POST'])
@admin_required
def trips():
    if request.method == 'POST':
        try:
            trip = FishingTrip(boat_id=int(request.form['boat_id']), captain_id=int(request.form['captain_id']),
                               departure_time=datetime.fromisoformat(request.form['departure_time']),
                               departure_port=request.form['departure_port'].strip(),
                               recorded_lat=Decimal(request.form['recorded_lat']) if request.form.get('recorded_lat') else None,
                               recorded_lng=Decimal(request.form['recorded_lng']) if request.form.get('recorded_lng') else None,
                               status=request.form.get('status', 'planned'), notes=request.form.get('notes', '').strip() or None)
            db.session.add(trip); db.session.flush()
            evaluate_trip(trip)
            db.session.commit(); flash('Trip recorded and safety checks evaluated.', 'success')
            return redirect(url_for('trips'))
        except Exception as exc:
            db.session.rollback(); flash(f'Could not record trip. Check the values. ({exc})', 'danger')
    return render_template('trips.html', trips=FishingTrip.query.order_by(FishingTrip.departure_time.desc()).all(), boats=Boat.query.filter_by(status='active').all(), fishermen=Fisherman.query.order_by(Fisherman.full_name).all())


def haversine_km(lat1, lon1, lat2, lon2):
    import math
    r = 6371.0
    p1, p2 = math.radians(float(lat1)), math.radians(float(lat2))
    dp = math.radians(float(lat2) - float(lat1))
    dl = math.radians(float(lon2) - float(lon1))
    a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2 * r * math.asin(min(1, math.sqrt(a)))


def evaluate_trip(trip):
    """Basic radius-based demo check; not a legal/geospatial compliance determination."""
    if trip.recorded_lat is None or trip.recorded_lng is None:
        return
    trip_date = trip.departure_time.date()
    for zone in MarineZone.query.filter_by(active=True).all():
        distance = haversine_km(trip.recorded_lat, trip.recorded_lng, zone.center_lat, zone.center_lng)
        inside = distance <= float(zone.radius_km)
        if inside and zone.zone_type in ('restricted', 'protected'):
            exists = SafetyAlert.query.filter_by(trip_id=trip.id, zone_id=zone.id, alert_type='restricted_zone').first()
            if not exists:
                db.session.add(SafetyAlert(trip_id=trip.id, zone_id=zone.id, alert_type='restricted_zone', severity='high', message=f'Trip location falls within the demo radius for "{zone.zone_name}". Verify against official boundaries.'))
                trip.status = 'flagged'
        if inside:
            restrictions = FishingRestriction.query.filter(FishingRestriction.zone_id == zone.id, FishingRestriction.start_date <= trip_date, FishingRestriction.end_date >= trip_date).all()
            for restriction in restrictions:
                exists = SafetyAlert.query.filter_by(trip_id=trip.id, zone_id=zone.id, alert_type='seasonal_ban').first()
                if not exists:
                    db.session.add(SafetyAlert(trip_id=trip.id, zone_id=zone.id, alert_type='seasonal_ban', severity='high', message=f'Trip date overlaps the configured restriction "{restriction.restriction_name}". Verify the applicable official rule.'))
                    trip.status = 'flagged'


@app.route('/trips/<int:trip_id>/status', methods=['POST'])
@admin_required
def trip_status(trip_id):
    trip = db.get_or_404(FishingTrip, trip_id)
    status = request.form.get('status')
    if status not in ('planned', 'at_sea', 'returned', 'flagged'):
        abort(400)
    trip.status = status
    if status == 'returned' and not trip.return_time:
        trip.return_time = datetime.now()
    db.session.commit(); flash('Trip status updated.', 'success')
    return redirect(url_for('trips'))


@app.route('/catches', methods=['GET', 'POST'])
@admin_required
def catches():
    if request.method == 'POST':
        try:
            quantity = Decimal(request.form['quantity_kg']); value = Decimal(request.form.get('market_value') or '0')
            if quantity <= 0 or value < 0:
                raise ValueError('Quantity must be positive and value cannot be negative.')
            record = CatchRecord(trip_id=int(request.form['trip_id']), species_id=int(request.form['species_id']),
                                 quantity_kg=quantity, market_value=value,
                                 recorded_at=datetime.fromisoformat(request.form['recorded_at']) if request.form.get('recorded_at') else datetime.now(),
                                 notes=request.form.get('notes', '').strip() or None)
            db.session.add(record); db.session.commit(); flash('Catch record added.', 'success')
            return redirect(url_for('catches'))
        except Exception as exc:
            db.session.rollback(); flash(f'Could not add catch record. ({exc})', 'danger')
    records = CatchRecord.query.order_by(CatchRecord.recorded_at.desc()).all()
    return render_template('catches.html', records=records, trips=FishingTrip.query.order_by(FishingTrip.departure_time.desc()).all(), species=FishSpecies.query.order_by(FishSpecies.common_name).all())


@app.route('/zones', methods=['GET', 'POST'])
@admin_required
def zones():
    if request.method == 'POST':
        try:
            zone = MarineZone(zone_name=request.form['zone_name'].strip(), zone_type=request.form['zone_type'],
                              description=request.form.get('description', '').strip() or None,
                              center_lat=Decimal(request.form['center_lat']), center_lng=Decimal(request.form['center_lng']),
                              radius_km=Decimal(request.form['radius_km']), active=True)
            if not (-90 <= float(zone.center_lat) <= 90 and -180 <= float(zone.center_lng) <= 180 and float(zone.radius_km) > 0):
                raise ValueError('Latitude, longitude, or radius is outside the valid range.')
            db.session.add(zone); db.session.commit(); flash('Marine zone added.', 'success')
            return redirect(url_for('zones'))
        except Exception as exc:
            db.session.rollback(); flash(f'Could not add zone. ({exc})', 'danger')
    return render_template('zones.html', zones=MarineZone.query.order_by(MarineZone.zone_name).all())


@app.route('/zones/<int:zone_id>/toggle', methods=['POST'])
@admin_required
def toggle_zone(zone_id):
    zone = db.get_or_404(MarineZone, zone_id); zone.active = not zone.active
    db.session.commit(); flash('Zone status updated.', 'success')
    return redirect(url_for('zones'))


@app.route('/alerts')
@login_required
def alerts():
    status = request.args.get('status', 'all')
    query = SafetyAlert.query
    if status in ('open', 'reviewing', 'resolved'):
        query = query.filter_by(status=status)
    return render_template('alerts.html', alerts=query.order_by(SafetyAlert.created_at.desc()).all(), selected_status=status)


@app.route('/alerts/<int:alert_id>/status', methods=['POST'])
@admin_required
def alert_status(alert_id):
    alert = db.get_or_404(SafetyAlert, alert_id)
    status = request.form.get('status')
    if status not in ('open', 'reviewing', 'resolved'):
        abort(400)
    alert.status = status
    alert.resolved_at = datetime.now() if status == 'resolved' else None
    db.session.commit(); flash('Alert updated.', 'success')
    return redirect(url_for('alerts'))


@app.route('/reports')
@login_required
def reports():
    monthly = db.session.query(func.date_format(CatchRecord.recorded_at, '%Y-%m').label('month'), func.sum(CatchRecord.quantity_kg).label('kg'), func.sum(CatchRecord.market_value).label('value')).group_by('month').order_by('month').all()
    species = db.session.query(FishSpecies.common_name, func.coalesce(func.sum(CatchRecord.quantity_kg), 0).label('kg'), func.coalesce(func.sum(CatchRecord.market_value), 0).label('value')).outerjoin(CatchRecord, CatchRecord.species_id == FishSpecies.id).group_by(FishSpecies.id, FishSpecies.common_name).order_by(func.sum(CatchRecord.quantity_kg).desc()).all()
    return render_template('reports.html', monthly=monthly, species=species)


@app.route('/api/map-data')
@login_required
def map_data():
    zones_data = [{'id': z.id, 'name': z.zone_name, 'type': z.zone_type, 'lat': float(z.center_lat), 'lng': float(z.center_lng), 'radius_km': float(z.radius_km), 'active': bool(z.active)} for z in MarineZone.query.all()]
    trips_data = [{'id': t.id, 'boat': t.boat.boat_name, 'captain': t.captain.full_name, 'status': t.status, 'lat': float(t.recorded_lat), 'lng': float(t.recorded_lng), 'departure': t.departure_time.isoformat(sep=' ')} for t in FishingTrip.query.filter(FishingTrip.recorded_lat.isnot(None), FishingTrip.recorded_lng.isnot(None)).all()]
    return jsonify({'zones': zones_data, 'trips': trips_data})


@app.errorhandler(403)
def forbidden(_error):
    return render_template('error.html', code=403, message='Your account does not have permission to perform this action.'), 403


@app.errorhandler(404)
def not_found(_error):
    return render_template('error.html', code=404, message='The requested page could not be found.'), 404


with app.app_context():
    # The schema.sql script is the source of truth for MySQL. create_all also supports quick local setup.
    try:
        db.create_all()
        admin_username = os.getenv('ADMIN_USERNAME', 'admin')
        admin_password = os.getenv('ADMIN_PASSWORD')
        if admin_password and not User.query.filter_by(username=admin_username).first():
            initial_admin = User(username=admin_username, role='admin')
            initial_admin.set_password(admin_password)
            db.session.add(initial_admin)
            db.session.commit()
        elif not admin_password:
            print('[Startup] ADMIN_PASSWORD is not set; no initial admin account was created.')
    except Exception as startup_error:
        # Allow the app file to load so the developer sees the database error on first request/logs.
        print(f'[Startup database warning] {startup_error}')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=os.getenv('FLASK_DEBUG', '0') == '1')
