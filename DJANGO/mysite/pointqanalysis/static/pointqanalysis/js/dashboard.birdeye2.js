var history_vehicle = {};
history_vehicle = JSON.parse(history_vehicle);


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
	birdeye.coordinates = [];
	birdeye.simu_time = 0;
	birdeye.simu_time_step = 1.0;
	birdeye.timestep = 0.1;
	birdeye.linkColor = ["#b5ff12", "#bce510", "#c3cb0e", "#cab10c", "#d1970a", "#d87d08", "#df6306", "#e64904", "#ed2f02", "#f41500", "#ff0000"];

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
	birdeye.play();
};

birdeye.goto = function(time) {
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
				var moment_2_display = moment(moment_origin).add(birdeye.simu_time,'s');
				display_moment(moment_2_display);

				nanobar.go(parseInt(birdeye.simu_time / maxtimesim * 100));

				birdeye.core.clearMarkers();
				birdeye.core.buildArray(birdeye.simu_time.toString() + ".0");
				birdeye.core.showMarkers();


				birdeye._then = birdeye.now;
			}
		}
		
		birdeye.animationFrameLoop = window.requestAnimFrame(birdeye.core.frame);
	},

	Color : function(nb_veh) {
		if (nb_veh < 5) {
			return '#55FE00';
		}
		else if (nb_veh < 10) {
			return '#FEF600';
		}
		else if (nb_veh <15) {
			return '#FE0000';
		}
		else {
			return '#FE0000';
		}

	},

	buildArray : function(time) {
		var positions = history_vehicle[time];
		console.log(time);
		console.log(positions);
		birdeye.coordinates = [];
		for (vehicle in positions) {
			var location = new google.maps.LatLng(positions[vehicle][0], positions[vehicle][1]);
			var marker = new google.maps.Marker({ position: location});
			birdeye.coordinates.push(marker);
			console.log(marker);
		}
	},

	setAllMap : function(map) {
		for (var i = 0; i < birdeye.coordinates.length; i++) {
			birdeye.coordinates[i].setMap(map);
		}
	},

	clearMarkers : function() {
		birdeye.core.setAllMap(null);
	},

	showMarkers : function() {
		birdeye.core.setAllMap(map);
	}
}

