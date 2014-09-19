
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

		function getObjects(obj, key, val) {
			var objects = [];
			for (var i in obj) {
				if (!obj.hasOwnProperty(i)) continue;
					if (typeof obj[i] == 'object') {
						objects = objects.concat(getObjects(obj[i], key, val));
					} 
				else if (i == key && obj[key] == val) {
					objects.push(obj);
				}
			}
			return objects;
		}

		var nodeInLinks
		var nodeOutLinks

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
				var nodeinfowindow = new google.maps.InfoWindow({
				    content: '<h5>Node:  1</h5><div><p><button type="button" class="btn btn-info btn-block" id="node_add_out">Add Out Links</button></p><p><button type="button" class="btn btn-info btn-block" id="node_add_in">Add In Links</button></p><p><button type="button" class="btn btn-info btn-block" id="node_add_queues">Add All Queues</button></p></div>',
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


			map.data.addListener('mousedown', function(event) {
				if (event.feature.getGeometry().getType() == 'LineString') {
				    map.data.overrideStyle(event.feature, {strokeColor: 'orange'});
				}			    
			});
			map.data.addListener('mouseup', function(event) {
				if (event.feature.getGeometry().getType() == 'LineString') {
				    map.data.revertStyle();
				}			    
			});

			map.data.addListener('click', function(event) {
			    if (event.feature.getGeometry().getType() == 'Point'){
				var id_no = event.feature.getProperty('id');
				console.log(event.feature.getId());
				$.getJSON('../pointqanalysis/ajax?action=get_from_node', {'node_id': id_no, 'type': 'flow'}, function(result) {
				    nodeinfowindow.setContent('<h5>Node: '+id_no+'</h5><div><p><button type="button" class="btn btn-info btn-block" id="node_add_out" onclick="nodeAddOutFunction()" onmouseover="nodeAddOutOver()" onmouseout="nodeAddOutOut()">Add Out Links</button></p><p><button type="button" class="btn btn-info btn-block" id="node_add_in" onclick="nodeAddInFunction()" onmouseover="nodeAddInOver()" onmouseout="nodeAddInOut()">Add In Links</button></p><p><button type="button" class="btn btn-info btn-block" id="node_add_queues" onclick="nodeAddQueueFunction()" onmouseover="nodeAddQueueOver()" onmouseout="nodeAddQueueOut()">Add All Queues</button></p></div>');
				nodeinfowindow.setPosition({lat: event.latLng.lat() + 0.00005, lng: event.latLng.lng()});
				nodeinfowindow.open(map);
				    var node=getObjects(topjson, 'id', id_no);
				    nodeInLinks=node[0].inputs;
				    nodeOutLinks=node[0].outputs;
				});
			    }
			    // Add the link to the list_links array
				if (event.feature.getGeometry().getType() == 'LineString') {
					// id of the link we clicked on (NOT the  actual feature id; the id stored in the "properties" field)
					var id_li = event.feature.getProperty('id');
					// if we want to select queues
					if (indicator == 'queue') {

						// if count is even
						if (count % 2 == 0) {

							// we increment count
							count = count + 1;

							// we add the link id to list_queue_temp
							list_queue_temp[0] = id_li;
							list_queue_temp_feat=event.feature;
						    // we change the color of the link
						    event.feature.setProperty('isColorful', true);
					 		map.data.revertStyle();
						}

						// if count is uneven
						else {
							// we increment count
							count = 0;
						    if (id_li!=list_queue_temp[0]){

							// we add the link id to list_queue_temp
							list_queue_temp[1] = id_li;

							// we add list_queue_temp to list_queues
							addQueue(list_queue_temp);
						    }
						    else {
							var link=getObjects(topjson, 'link_id', id_li);
							nodeOutLinks=link[0].outputs;

							$.each($.parseJSON(nodeOutLinks), function( index, id_li_out ) {
							    if (id_li_out !=-1){
								list_queue_temp[0] = id_li;
								list_queue_temp[1] = id_li_out;
								addQueue(list_queue_temp);
							    }
							});
						    }
						      
						    //we revert the color of the link
						    list_queue_temp_feat.setProperty('isColorful', false);
					 		map.data.revertStyle();

						}
					}
					// if we want to select flows
					else if (indicator == 'flow') {
					    addLink(id_li);
					}
				    else if (indicator == 'OD'){
					if (ODcount % 2 == 0) {

					    // we increment count
					    ODcount = ODcount + 1;

					    // we add the link id to list_queue_temp
					    list_OD_temp[0] = id_li;
					    list_OD_temp_feat = event.feature; 
					    // we change the color of the link
					 event.feature.setProperty('isColorful', true);
					 map.data.revertStyle();
					}else {
					    // we increment count
					    ODcount = 0;
					    // we add the link id to list_queue_temp
					    list_OD_temp[1] = id_li;
					    // we add list_OD_temp to list_ODs
					    addOD(list_OD_temp);
					    list_OD_temp_feat.setProperty('isColorful', false);
					 	map.data.revertStyle();
				    }
				}
				}
			});


		}

$("#flow").on("click",'.img_delete_flow',function(){deletable_flow_link(this);});
$("#queue").on("click",'.img_delete_queue',function(){deletable_queue(this);});
$("#OD").on("click",'.img_delete_OD',function(){deletable_OD(this);});
$("#flow").on("mouseover",'.link_li',function(){
    console.log('mouseover');
    var linkStr = $(this).attr('link');
    var feat=map.data.getFeatureById("link_"+linkStr);
    map.data.overrideStyle(feat, {strokeColor: '#30D630', zIndex: google.maps.Marker.MAX_ZINDEX+1, strokeOpacity: .8});
});
$("#flow").on("mouseout",'.link_li',function(){
    map.data.revertStyle();
});
$("#queue").on("mouseover",'.queue_li',function(){
    var link1Str = $(this).attr('link1');
    var link2Str = $(this).attr('link2');
    var feat1=map.data.getFeatureById("link_"+link1Str);
    var feat2=map.data.getFeatureById("link_"+link2Str);
    map.data.overrideStyle(feat1, {strokeColor: '#30D630', zIndex: google.maps.Marker.MAX_ZINDEX+1, strokeOpacity: .8});
    map.data.overrideStyle(feat2, {strokeColor: 'orange', zIndex: google.maps.Marker.MAX_ZINDEX+1, strokeOpacity: .8});
   
});
$("#queue").on("mouseout",'.queue_li',function(){
    map.data.revertStyle();
});
$("#OD").on("mouseover",'.OD_li',function(){
    var link1Str = $(this).attr('link1');
    var link2Str = $(this).attr('link2');
    var feat1=map.data.getFeatureById("link_"+link1Str);
    var feat2=map.data.getFeatureById("link_"+link2Str);
    map.data.overrideStyle(feat1, {strokeColor: '#30D630', zIndex: google.maps.Marker.MAX_ZINDEX+1, strokeOpacity: .8});
    map.data.overrideStyle(feat2, {strokeColor: 'orange', zIndex: google.maps.Marker.MAX_ZINDEX+1, strokeOpacity: .8});
});
$("#OD").on("mouseout",'.OD_li',function(){
    map.data.revertStyle();
});
		function deletable_flow_link(link_img) {
						// delete queue from list_queues
						var link = $(link_img).attr('link');
						if (list_links.indexOf(link) != -1) {
							list_links.splice(list_links.indexOf(link), 1);
						}

						// delete queue from DOM
						$(link_img).parent().remove();
		    map.data.revertStyle();
					}
		function deletable_queue(queue_img) {

						// delete queue from list_queues
						var link1 = $(queue_img).attr('link1');
						var link2 = $(queue_img).attr('link2');
						if (index_array(link1, link2, list_queues) != -1) {
							list_queues.splice(index_array(link1, link2, list_queues), 1);
						}

						// delete queue from DOM
						$(queue_img).parent().remove();
		    map.data.revertStyle();
					}
		function deletable_OD(OD_img) {
						// delete queue from list_queues
						var link1_torem = $(OD_img).attr('link1');
						var link2_torem = $(OD_img).attr('link2');
						console.log('attempting to remove'+link1_torem+', '+link2_torem+'from '+list_ODs);
						ind_torem=index_array(link1_torem, link2_torem, list_ODs);
						console.log('index is '+ind_torem)
						if (ind_torem!= -1) {
							console.log('found in array: '+link1_torem+', '+link2_torem+' at index '+ind_torem)
							list_ODs.splice(ind_torem, 1);
						}

						// delete queue from DOM
						$(OD_img).parent().remove();
		    map.data.revertStyle();
					}
function addLink(id_li){
    //add to list_links
				list_links.push(id_li.toString());
// we create the html element
				var html_element = '<li class="link_li" link="'+String(id_li)+'"><img src= "' + static_img_close +'" alt="close" class="img_delete_flow" link="'+ String(id_li) + '">' + String(id_li) + '</li>';
						// we append the html element to <ul>
						$('#ul_flow').append(html_element);
			    }
function addQueue(pair){
				    // we add list_queue_temp to list_queues
				    var pair=pair.slice(0);
				    list_queues.push(pair);

				    // we create the html element
				    var html_element = '<li class="queue_li" link1="'+pair[0].toString()+'" link2="'+pair[1].toString()+'"><img src="' + static_img_close + '" alt="close" class="img_delete_queue" link1="'+ pair[0]+ '" link2 = "' + pair[1]  + '">[' + pair[0] +','+pair[1] + ']</li>';

				    // we append it to <ul>
				    $('#ul_queues').append(html_element);
}
function addOD(pair){
				    // we add list_queue_temp to list_queues
				    var pair=pair.slice(0);
				    list_ODs.push(pair);
				    // we create the html element
				    var html_element = '<li class="OD_li" link1="'+pair[0].toString()+'" link2="'+pair[1].toString()+'"><img src="' + static_img_close + '" alt="close" class="img_delete_OD" link1="'+ pair[0]+ '" link2 = "' + pair[1]  + '">[' + pair[0] +','+pair[1] + ']</li>';

				    // we append it to <ul>
				    $('#ul_OD').append(html_element);
}
		    function nodeAddInFunction(){
			$.each($.parseJSON(nodeInLinks), function( index, id_li ) {
			    if (id_li != -1){
				addLink(id_li);
			    }
			});
		    }
                   function nodeAddOutFunction(){
			$.each($.parseJSON(nodeOutLinks), function( index, id_li ) {
			    if (id_li != -1){
				addLink(id_li);
			    }
			});
		    }
		    function nodeAddQueueFunction(){
			$.each($.parseJSON(nodeInLinks), function( index, id_li_in ) {
			    $.each($.parseJSON(nodeOutLinks), function( index, id_li_out ) {
				if (id_li_in !=-1 && id_li_out !=-1){
				    addQueue([id_li_in,id_li_out]);
				}
			    });
			});

		    }
function nodeAddOutOver(){
    $.each($.parseJSON(nodeOutLinks), function( index, id_li ) {
	if (id_li != -1){
	    var feat=map.data.getFeatureById("link_"+id_li.toString());
	    map.data.overrideStyle(feat, {strokeColor: '#30D630'});
	}
    });
}
function nodeAddOutOut(){
    map.data.revertStyle();
}
function nodeAddQueueOver(){
    $.each($.parseJSON(nodeOutLinks), function( index, id_li ) {
	if (id_li != -1){
	    var feat=map.data.getFeatureById("link_"+id_li.toString());
	    map.data.overrideStyle(feat, {strokeColor: 'orange'});
	}
    });
    $.each($.parseJSON(nodeInLinks), function( index, id_li ) {
	if (id_li != -1){
	    var feat=map.data.getFeatureById("link_"+id_li.toString());
	    map.data.overrideStyle(feat, {strokeColor: '#30D630'});
	}
    });
}
function nodeAddQueueOut(){
    map.data.revertStyle();
}
function nodeAddInOver(){
    $.each($.parseJSON(nodeInLinks), function( index, id_li ) {
	if (id_li != -1){
	    var feat=map.data.getFeatureById("link_"+id_li.toString());
	    map.data.overrideStyle(feat, {strokeColor: '#30D630'});
	}
    });
}
function nodeAddInOut(){
    map.data.revertStyle();
}