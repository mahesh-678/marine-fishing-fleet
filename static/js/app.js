async function initFleetMap(endpoint) {
  const element = document.getElementById('fleetMap');
  if (!element || typeof L === 'undefined') return;
  const map = L.map(element, {scrollWheelZoom: false}).setView([9.4, 79.2], 8);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18, attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);
  const colors = {permitted: '#168a70', restricted: '#d56d3c', protected: '#6658b7'};
  try {
    const response = await fetch(endpoint);
    if (!response.ok) throw new Error('Unable to load map records');
    const data = await response.json();
    const bounds = [];
    data.zones.forEach(zone => {
      const point = [zone.lat, zone.lng];
      const color = colors[zone.type] || '#148997';
      const marker = L.circle(point, {radius: zone.radius_km * 1000, color, fillColor: color, fillOpacity: .13, weight: 2, dashArray: zone.active ? null : '5 6'}).addTo(map);
      marker.bindPopup(`<strong>${escapeHtml(zone.name)}</strong><br>Type: ${escapeHtml(zone.type)}<br>Radius: ${zone.radius_km} km${zone.active ? '' : '<br>Inactive'}`);
      bounds.push(point);
    });
    data.trips.forEach(trip => {
      const point = [trip.lat, trip.lng];
      const marker = L.marker(point).addTo(map);
      marker.bindPopup(`<strong>Trip #${trip.id}: ${escapeHtml(trip.boat)}</strong><br>Captain: ${escapeHtml(trip.captain)}<br>Status: ${escapeHtml(trip.status)}<br>${escapeHtml(trip.departure)}`);
      bounds.push(point);
    });
    if (bounds.length) map.fitBounds(bounds, {padding: [20, 20], maxZoom: 10});
  } catch (error) {
    console.error(error);
    element.insertAdjacentHTML('beforeend', '<div class="map-load-error">Map data could not be loaded.</div>');
  }
}
function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
}

// Responsive sidebar: preserves ordinary Flask page navigation and form submissions.
(() => {
  const body = document.body;
  const toggle = document.getElementById('menuToggle');
  const backdrop = document.getElementById('sidebarBackdrop');
  const sidebar = document.getElementById('appSidebar');
  const closeMenu = () => {
    body.classList.remove('sidebar-open');
    if (toggle) toggle.setAttribute('aria-expanded', 'false');
  };
  if (toggle && sidebar) {
    toggle.addEventListener('click', () => {
      const open = !body.classList.contains('sidebar-open');
      body.classList.toggle('sidebar-open', open);
      toggle.setAttribute('aria-expanded', String(open));
    });
  }
  if (backdrop) backdrop.addEventListener('click', closeMenu);
  if (sidebar) sidebar.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
  window.addEventListener('resize', () => { if (window.innerWidth > 991) closeMenu(); });

  const dateLabel = document.getElementById('localDateLabel');
  if (dateLabel) {
    try {
      dateLabel.textContent = new Intl.DateTimeFormat(undefined, { weekday: 'short', month: 'short', day: 'numeric' }).format(new Date()).toUpperCase();
    } catch (_error) {
      dateLabel.textContent = 'OPERATIONS ONLINE';
    }
  }
})();
