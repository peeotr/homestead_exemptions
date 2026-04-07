function(el, x) {
  var map = this;
  var mapData = MAPDATA_PLACEHOLDER;
  var clusterGroup = L.markerClusterGroup();
  map.addLayer(clusterGroup);

  var nameList = NAMELIST_PLACEHOLDER;
  var datalist = document.getElementById('nameOptions');
  nameList.forEach(function(n) {
    var opt = document.createElement('option');
    opt.value = n;
    datalist.appendChild(opt);
  });

  function renderMarkers(data) {
    clusterGroup.clearLayers();
    data.forEach(function(row) {
      var m = L.circleMarker([row.lat, row.long], {
        radius: 7.5,
        color: '#0078ff',
        fillOpacity: 0.7,
        stroke: false
      }).bindPopup(
        'Address: ' + row.address + '<br/>' +
        'Owner: ' + row.name + '<br/>' +
        'Total Exemptions: ' + row.owner_count
      );
      clusterGroup.addLayer(m);
    });
  }

  renderMarkers(mapData);

  document.getElementById('nameSearch')
    .addEventListener('input', function() {
      var val = this.value.toLowerCase().trim();
      var filtered = val
        ? mapData.filter(function(r) {
            return r.name && r.name.toLowerCase().includes(val);
          })
        : mapData;
      renderMarkers(filtered);
    });
}
