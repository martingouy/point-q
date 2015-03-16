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
	birdeye.simu_time_step = 5;
	birdeye.history_json = history_json;
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
				//console.log(birdeye.simu_time_step);
				//console.log(birdeye.time_step);
				var moment_2_display = moment(moment_origin).add(birdeye.simu_time,'s');
				display_moment(moment_2_display);
				//$('#time-display').empty();
				//$('#time-display').append(moment_2_display);
				//$('#field_time_simu').val(moment_2_display);

				nanobar.go(parseInt(birdeye.simu_time / maxtimesim * 100));

				var sorted_by_color = birdeye.core.sortByColor(birdeye.simu_time)

				for (var i = 0; i < birdeye.linkColor.length; i++) {
					var percent = i * 10;
					color_links(sorted_by_color[percent.toString()], birdeye.linkColor[i]);
				}

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

	sortByColor : function(time) {
		var history = birdeye.history_json[time.toString()];
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

