var GMAP = function(id_div, geojson, node_marker) {

	var map;

	var init = function() {

		// Create a simple map.
		map = new google.maps.Map(document.getElementById(id_div), {
		    disableAutoPan: true,
			zoom: 16,
			center: {lat: 34.149156, lng: -118.0677},
			disableDefaultUI: true,
		});

		map.data.addGeoJson(geojson);
		zoom(map);
	   
		map.data.setStyle(function(feature){
			var color='blue';
			if (feature.getProperty('isColorful')) {
				color = '#30D630';
			}
			return({
				icon: node_marker,
				//strokeColor: '#0019ff',
				strokeColor: color,
				strokeOpacity: 0.8,
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

	};

	var processPoints = function(geometry, callback, thisArg) {
		/**
		 * Process each point in a Geometry, regardless of how deep the points may lie.
		 * @param {google.maps.Data.Geometry} geometry The structure to process
		 * @param {function(google.maps.LatLng)} callback A function to call on each
		 *     LatLng point encountered (e.g. Array.push)
		 * @param {Object} thisArg The value of 'this' as provided to 'callback' (e.g.
		 *     myArray)
		 */
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
	};


	var zoom = function(){
		/**
		 * Update a map's viewport to fit each geometry in a dataset
		 * @param {google.maps.Map} map The map to adjust
		 */
		var bounds = new google.maps.LatLngBounds();
		map.data.forEach(function(feature) {
			processPoints(feature.getGeometry(), bounds.extend, bounds);
		});
		map.fitBounds(bounds);
	};


	init();

	return {

		color_links: function(list_links, color) {
			for (var i = 0; i < list_links.length; i++) {
				var feat=map.data.getFeatureById("link_"+list_links[i]);
				map.data.overrideStyle(feat, {strokeColor: color, zIndex: google.maps.Marker.MAX_ZINDEX+1, strokeOpacity: .8});
			}
		},

		reset_colors: function() {
			map.data.forEach(function(feature){
				if (feature.getGeometry().getType() == 'LineString'){
					map.data.overrideStyle(feature, {strokeColor: 'blue', zIndex: google.maps.Marker.MAX_ZINDEX+1, strokeOpacity: .8});
				}
			});
		},

		dmap: map
	};
}
