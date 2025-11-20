// maps.js - single, cleaned-up client script for templates/maps.html
// - uses window.JOBS if present (server-rendered list)
// - otherwise fetches /api/jobs/locations (GeoJSON)
// - renders markers + popups and a clickable listing in #results
(function () {
  const mapEl = document.getElementById('map');
  const listEl = document.getElementById('results');
  const applyBtn = document.getElementById('applyFilters');
  if (!mapEl || !listEl) return;

  const DEFAULT_CENTER = [38.5816, -121.4944]; // Sacramento
  const DEFAULT_ZOOM = 12;

  const map = L.map('map').setView(DEFAULT_CENTER, DEFAULT_ZOOM);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
    maxZoom: 19,
  }).addTo(map);

  // State
  const markers = [];
  const markersById = new Map();
  let currentFeatures = [];

  // Utilities
  function escapeHtml(str) {
    if (str == null) return '';
    return String(str)
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll("'", '&#39;');
  }
  function isValidLatLng(lat, lng) {
    if (lat == null || lng == null) return false;
    const nlat = Number(lat);
    const nlng = Number(lng);
    return Number.isFinite(nlat) && Number.isFinite(nlng);
  }

  function clearMarkers() {
    markers.forEach((m) => {
      try { map.removeLayer(m); } catch (e) { /* ignore */ }
    });
    markers.length = 0;
    markersById.clear();
  }

  function addMarker(feature) {
    const p = feature.properties || {};
    const [lng, lat] = feature.geometry.coordinates;
    const marker = L.marker([Number(lat), Number(lng)]);
    const id = p.id ?? '';
    const title = escapeHtml(p.title ?? 'Untitled');
    const desc = escapeHtml(p.description ?? '');
    const url = p.url ?? (id ? `/job/${id}` : '#');

    const popup = document.createElement('div');
    const strong = document.createElement('strong');
    strong.textContent = p.title ?? 'Untitled';
    popup.appendChild(strong);
    if (desc) {
      const pEl = document.createElement('p');
      pEl.textContent = p.description ?? '';
      popup.appendChild(pEl);
    }
    const a = document.createElement('a');
    a.href = url;
    a.target = '_blank';
    a.rel = 'noopener';
    a.textContent = 'Open listing';
    popup.appendChild(a);

    marker.bindPopup(popup);
    marker.addTo(map);
    markers.push(marker);
    if (id !== null && id !== undefined) markersById.set(String(id), marker);
  }

  function renderList(features) {
    listEl.innerHTML = '';
    if (!features || !features.length) {
      listEl.innerHTML = '<div class="card">No jobs found.</div>';
      return;
    }
    features.forEach((f) => {
      const p = f.properties || {};
      const id = p.id ?? '';
      const title = p.title ?? 'Untitled';
      const location = p.location ?? '';
      const desc = p.description ?? '';

      const a = document.createElement('a');
      a.className = 'card';
      a.href = p.url ?? (id ? `/job/${id}` : '#');
      a.target = '_blank';
      a.rel = 'noopener';
      a.innerHTML = `<b>${escapeHtml(title)}</b><div class="desc">${escapeHtml(desc)}</div><div class="loc">${escapeHtml(location)}</div>`;

      // view on map button
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'view-on-map';
      btn.textContent = 'View on map';
      btn.style.marginLeft = '8px';
      btn.addEventListener('click', (ev) => {
        ev.preventDefault();
        const marker = markersById.get(String(id));
        if (marker) {
          map.setView(marker.getLatLng(), Math.max(map.getZoom(), 14));
          marker.openPopup();
        }
      });

      a.appendChild(btn);
      listEl.appendChild(a);
    });
  }

  function loadFeatures(geojson) {
    // Accept either GeoJSON FeatureCollection or server JOBS-array converted to geojson.
    if (!geojson || !Array.isArray(geojson.features)) {
      currentFeatures = [];
      renderList([]);
      clearMarkers();
      return;
    }
    currentFeatures = geojson.features;
    clearMarkers();

    currentFeatures.forEach((f) => {
      // Ensure geometry is Point and coordinates valid (lng, lat)
      if (!f.geometry || f.geometry.type !== 'Point') return;
      const coords = f.geometry.coordinates || [];
      if (!isValidLatLng(coords[1], coords[0])) return;
      addMarker(f);
    });

    renderList(currentFeatures);

    // Fit to bounds if we have markers
    if (markers.length) {
      const group = L.featureGroup(markers);
      map.fitBounds(group.getBounds(), { padding: [30, 30], maxZoom: 15 });
    } else {
      map.setView(DEFAULT_CENTER, DEFAULT_ZOOM);
    }
  }

  // Convert legacy JOBS array (server-passed) into GeoJSON
  function jobsArrayToGeoJSON(jobsArr) {
    if (!Array.isArray(jobsArr)) return { type: 'FeatureCollection', features: [] };
    const features = jobsArr.map((j) => {
      // be tolerant of various key names
      const lat = j.lat ?? j.latitude ?? j.latitude_float;
      const lng = j.lng ?? j.longitude ?? j.lon ?? j.longitude_float;
      if (!isValidLatLng(lat, lng)) return null;
      return {
        type: 'Feature',
        geometry: { type: 'Point', coordinates: [Number(lng), Number(lat)] },
        properties: {
          id: j.id ?? j.job_id ?? null,
          title: j.title ?? j.name ?? 'Untitled',
          description: j.description ?? '',
          location: j.location ?? '',
          url: j.url ?? null,
          type: j.type ?? null,
        },
      };
    }).filter(Boolean);
    return { type: 'FeatureCollection', features };
  }

  // Filtering
  function applyFilters() {
    const q = (document.getElementById('q')?.value ?? '').trim().toLowerCase();
    const loc = (document.getElementById('loc')?.value ?? '').trim().toLowerCase();
    const type = (document.getElementById('type')?.value ?? '').trim().toLowerCase();

    const filtered = currentFeatures.filter((f) => {
      const p = f.properties || {};
      const s = ((p.title || '') + ' ' + (p.description || '') + ' ' + (p.location || '') + ' ' + (p.type || '')).toLowerCase();
      return (!q || s.includes(q)) && (!loc || s.includes(loc)) && (!type || s.includes(type));
    });

    loadFeatures({ type: 'FeatureCollection', features: filtered });
  }

  if (applyBtn) {
    applyBtn.addEventListener('click', (ev) => {
      ev.preventDefault();
      applyFilters();
    });
  }

  // Init: prefer window.JOBS (server-rendered). Otherwise fetch API.
  (function init() {
    try {
      if (Array.isArray(window.JOBS) && window.JOBS.length) {
        const gj = jobsArrayToGeoJSON(window.JOBS);
        if (gj.features.length) {
          loadFeatures(gj);
          return;
        }
      }
    } catch (e) {
      console.warn('Error parsing window.JOBS', e);
    }

    // fallback to backend GeoJSON
    fetch('/api/jobs/locations')
      .then((res) => {
        if (!res.ok) throw new Error('Network response was not ok');
        return res.json();
      })
      .then((geojson) => loadFeatures(geojson))
      .catch((err) => {
        console.error('Failed to load job locations:', err);
        listEl.innerHTML = '<div class="card">Unable to load listings at the moment.</div>';
      });
  })();
})();
