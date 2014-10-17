/**
 * Update a map's viewport to fit each geometry in a dataset
 * @param {google.maps.Map} map The map to adjust
 */
function zoom(map) {
	var bounds = new google.maps.LatLngBounds();
	map.data.forEach(function(feature) {
		processPoints(feature.getGeometry(), bounds.extend, bounds);
	});
	map.fitBounds(bounds);
}

/**
 * Process each point in a Geometry, regardless of how deep the points may lie.
 * @param {google.maps.Data.Geometry} geometry The structure to process
 * @param {function(google.maps.LatLng)} callback A function to call on each
 *     LatLng point encountered (e.g. Array.push)
 * @param {Object} thisArg The value of 'this' as provided to 'callback' (e.g.
 *     myArray)
 */
function processPoints(geometry, callback, thisArg) {
	if (geometry instanceof google.maps.LatLng) {
		callback.call(thisArg, geometry);
	} 
	else if (geometry instanceof google.maps.Data.Point) {
		callback.call(thisArg, geometry.get());
	} else {
		geometry.getArray().forEach(function(g) {
			processPoints(g, callback, thisArg);
		});
	}
}


function color_links(list_links, color) {
	for (var i = 0; i < list_links.length; i++) {
		var feat=map.data.getFeatureById("link_"+list_links[i]);
		map.data.overrideStyle(feat, {strokeColor: color, zIndex: google.maps.Marker.MAX_ZINDEX+1, strokeOpacity: .6});
	}
};


function initialize() {

	// Create a simple map.
	map = new google.maps.Map(document.getElementById('map-canvas'), {
	    disableAutoPan: true,
		zoom: 16,
		center: {lat: 34.149156, lng: -118.0677},
	});

	map.data.addGeoJson(geojson);
	zoom(map);
   
	map.data.setStyle(function(feature){
		var color='blue';
		if (feature.getProperty('isColorful')) {
			color = '#30D630';
		}
		return({
			icon: static_img_marker,
			//strokeColor: '#0019ff',
			strokeColor: color,
			strokeOpacity: 0.6,
			strokeWeight: 9,
		});
	});

	var infowindow = new google.maps.InfoWindow({
		content: 'sam',
		disableAutoPan:true
	});

	// Add infowindow when mouse on an element
	map.data.addListener('mouseover', function(event) {
		if (event.feature.getGeometry().getType() == 'LineString') {
			infowindow.setContent(event.feature.getProperty('id'))
			infowindow.setPosition({lat: event.latLng.lat() + 0.00005, lng: event.latLng.lng()});
			infowindow.open(map);
		}
	});

	map.data.addListener('mouseout', function(event) {
		infowindow.close();                    
	});

	map.data.addListener('click', function(event) {
		if (event.feature.getGeometry().getType() == 'LineString'){
			var id_no = event.feature.getProperty('id');
			if (indicator == 'first_link') {
				ori_dest_links[0] = id_no;
				$('#btn_origin_link').text(id_no);
				$('#btn_origin_link').attr('class', 'btn btn-default');
				indicator = '';
			}
			else if (indicator == 'second_link') {
				ori_dest_links[1] = id_no;
				$('#btn_destination_link').text(id_no);
				$('#btn_destination_link').attr('class', 'btn btn-default');
				indicator = '';
			}
		}

	});


}
