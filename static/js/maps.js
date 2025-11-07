(function () {
  const map = L.map('map');
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19, attribution: '&copy; OpenStreetMap'
  }).addTo(map);

  const jobs = Array.isArray(window.JOBS) ? window.JOBS : [];
  const markers = [];
  const listEl = document.getElementById('results');

  function renderList(items) {
    listEl.innerHTML = '';
    if (!items.length) {
      listEl.innerHTML = '<div class="card">No jobs found.</div>';
      return;
    }
    items.forEach(j => {
      const a = document.createElement('a');
      a.className = 'card';
      a.href = `/job/${j.id}`;
      a.innerHTML = `<b>${j.title}</b><div class="desc">${j.description}</div>`;
      listEl.appendChild(a);
    });
  }

  function clearMarkers() { markers.forEach(m => map.removeLayer(m)); markers.length = 0; }

  function renderMarkers(items) {
    clearMarkers();
    const group = [];
    items.forEach(j => {
      if (j.lat && j.lng) {
        const m = L.marker([j.lat, j.lng]).addTo(map)
          .bindPopup(`<b>${j.title}</b><br/><a href="/job/${j.id}">View</a>`);
        markers.push(m);
        group.push(m.getLatLng());
      }
    });
    if (group.length) {
      const bounds = L.latLngBounds(group);
      map.fitBounds(bounds, { padding: [30, 30] });
    } else {
      map.setView([37.7749, -122.4194], 11); // default SF area
    }
  }

  function applyFilters() {
    const q = document.getElementById('q').value.trim().toLowerCase();
    const loc = document.getElementById('loc').value.trim().toLowerCase();
    const type = document.getElementById('type').value.trim().toLowerCase();

    const filtered = jobs.filter(j => {
      const s = (j.title + ' ' + j.description + ' ' + (j.location || '') + ' ' + (j.type || '')).toLowerCase();
      return (!q || s.includes(q)) && (!loc || s.includes(loc)) && (!type || s.includes(type));
    });

    renderList(filtered);
    renderMarkers(filtered);
  }

  document.getElementById('applyFilters').addEventListener('click', e => {
    e.preventDefault();
    applyFilters();
  });

  // initial paint
  renderList(jobs);
  renderMarkers(jobs);
})();
