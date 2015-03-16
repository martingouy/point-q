
window.requestAnimFrame = (function(){
	return  window.requestAnimationFrame ||
	window.webkitRequestAnimationFrame ||
	window.mozRequestAnimationFrame    ||
	function( callback ){
		window.setTimeout(callback, 1000 / 60);
	};
})();


window.birdeye = window.birdeye || {};

birdeye.init = function() {
	birdeye.simu_time = 0;
	birdeye.simu_time_step = 1.0;
	birdeye.timestep = 0.1;
	birdeye.linkColor = ["#b5ff12", "#bce510", "#c3cb0e", "#cab10c", "#d1970a", "#d87d08", "#df6306", "#e64904", "#ed2f02", "#f41500", "#ff0000"];
	birdeye.list_vehicles = history_vehicle.list_vehicles.slice();
	birdeye.myLayer = new WebGLLayer(map.dmap);
	birdeye.dataJson = {"type": "FeatureCollection", "features":[]};
	birdeye.myLayer.loadData(birdeye.dataJson);
	birdeye.myLayer.start();

};

birdeye.play = function() {
	if(!birdeye.isRunning) {
		birdeye._then = Date.now();
		birdeye.core.frame();
		birdeye.isRunning = true;
	}
};

birdeye.pause = function() {
	window.cancelAnimationFrame(birdeye.animationFrameLoop);
	birdeye.isRunning = false;
};

birdeye.restart = function() {
	birdeye.simu_time = 0;
	birdeye.list_vehicles = history_vehicle.list_vehicles.slice();
	birdeye.play();
};

birdeye.goto = function(time) {
	birdeye.list_vehicles = history_vehicle.list_vehicles.slice();
	birdeye.simu_time = time;
};


birdeye.core = {
	frame: function() {

		birdeye.now = Date.now();
		birdeye._delta = (birdeye.now - birdeye._then) / 1000; // Converts to seconds (optional)

		if (birdeye._delta >= birdeye.timestep){
			if (birdeye.simu_time >= maxtimesim) {
				birdeye.pause();
			}
			else {
				birdeye.simu_time += birdeye.simu_time_step;

				var moment_2_display = moment(dash_int.get_moment_origin()).add(birdeye.simu_time,'s');
				dash_int.display_time(moment_2_display);
				dash_int.progressBar.go(parseInt(birdeye.simu_time / maxtimesim * 100));

            	birdeye.core.posVeh(history_vehicle, birdeye.simu_time, map);

            	var time_truncated = birdeye.simu_time | 0;

            	if (time_truncated % 5 == 0){
					var sorted_by_color = birdeye.core.sortByColor(birdeye.simu_time)

					for (var i = 0; i < birdeye.linkColor.length; i++) {
						var percent = i * 10;
						map.color_links(sorted_by_color[percent.toString()], birdeye.linkColor[i]);
					}
				}

				birdeye._then = birdeye.now;
			}
		}
		
		birdeye.animationFrameLoop = window.requestAnimFrame(birdeye.core.frame);
	},

	posVeh : function(history, t, map) {
		// We iterate over the vehicles to know which ones are in the network at time t

 		var geojson_2_draw = {"type": "FeatureCollection", "features":[]};
		for (var j = 0; j < birdeye.list_vehicles.length; j++){ 

			veh_id = birdeye.list_vehicles[j];
			var vehicle = history[veh_id];
			// First step: is the vehicle in the network ?
			if (vehicle.t_en_netw <= t && t <= vehicle.t_ex_netw) {
				try{
					// Second step: we must know the link
					var i_located_link;

					for (var i = 0; i < vehicle.hist.length; i++) {
						var link = vehicle.hist[i];
						if (t <= link.t_leave){
							i_located_link = i;
							break;
						}
					}

					// Third step: Percentage of the link traveled
					var link = vehicle.hist[i_located_link];
					var elapsed_time = t - link.t_arrival_c_link;
					var total_time_traveling = (link.t_leave - link.t_arrival_c_link) - (link.t_start_departure - link.t_arrival_queue);
					var elapsed_time_traveling = elapsed_time;
					var percentage = 0;

					if (link.t_arrival_queue <= t && t <= link.t_start_departure) {
						elapsed_time_traveling = link.t_arrival_queue - link.t_arrival_c_link;
					}
					else if (t > link.t_start_departure){
						elapsed_time_traveling = t - (link.t_start_departure - link.t_arrival_queue) - link.t_arrival_c_link;
					}

					percentage = elapsed_time_traveling / total_time_traveling;
					percentage = percentage.toFixed(3);

					// Fourth step: Coordinates of the vehicle
					var polyline = map.dmap.data.getFeatureById("link_"+link.link).getGeometry();
					var position = polyline.GetPointAtDistance(polyline.Distance()*percentage);

					// Fifth step: Generate Geojson
					var new_feature = {"type": "Feature", "properties":{}, "geometry": {"type": "Point"}};
					new_feature.geometry["coordinates"] = [position.lng(), position.lat()];
					geojson_2_draw.features.push(new_feature);

					// Sixth step: We plot it
					birdeye.myLayer.features_.points.floats = [];
	            	birdeye.myLayer.features_.points.count = 0;
					birdeye.myLayer.loadData(geojson_2_draw);
				}
				catch(e) {console.log('Error while plotting a vehicle');}
			}

			else if (t > vehicle.t_ex_netw) {
				birdeye.list_vehicles.splice(j, 1);
				j--;
			}
			else if (t < vehicle.t_en_netw) {
				break;
			}
		}
	},

	sortByColor : function(time) {
		var history = json_birdeye[time.toString()];
		var sorted_by_color = {'0': [], '10':[], '20':[], '30': [], '40':[], '50':[], '60': [], '70':[], '80':[],  '90':[], '100':[]};

		for (var link in history) {
			var occupation = history[link];
			var occupation_percent = Math.round(occupation * 10)*10;
			if (occupation_percent > 100) {
				sorted_by_color['10'].push(link);
			}
			else {
				sorted_by_color[occupation_percent.toString()].push(link)
			}
		}

		return(sorted_by_color);
	}
}

