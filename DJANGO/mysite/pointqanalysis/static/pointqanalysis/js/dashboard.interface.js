var dash_interface = function(options) {

	/* ********************************************************
					VARIABLES
	******************************************************** */
	var nanobar;
	var moment_origin = moment({hour: 0, minute: 0, second: 0});
	var animation_start, animation_end;
	var maxtimesim = options.maxtimesim;

	/* ********************************************************
					INITIALIZATION
	******************************************************** */

	var init = function(){

		// NANOBAR 
		var nano_options = {
			bg: '#333',
			// leave target blank for global nanobar
			target: document.getElementById('nanobar'),
			// id for new nanobar
			id: 'mynano'
		};
		nanobar = new Nanobar(nano_options);
		nanobar.go(0);

		// hide loader
		$('.loader').hide();

		// switch to conf menu
		switch_left_panel('param', true);

		// Show init moment
		$('#set_origin_h').val('00');
		$('#set_origin_m').val('00');
		$('#set_origin_s').val('00');

		// init filters
		filters.init();
	};

	/* ********************************************************
					DISPLAY ELEMENTS
	******************************************************** */
	
				
	var display_moment = function(time){

		// We clear and replace the time on the map
		$('#time-display').empty();
		$('#time-display').append(time.format('HH:mm:ss'));

		// We display it in the jump section
		$('#field_time_simu_h').val(time.hour());
		$('#field_time_simu_m').val(time.minute());
		$('#field_time_simu_s').val(time.second());
	};

	
	var  display_startend_time = function(){
		// function to display the end_time
		$('#start_time').empty();
		var start_moment = moment(moment_origin).add(animation_start,'s');
		$('#start_time').append(start_moment.format('HH:mm:ss'));

		// function to display the end_time
		$('#end_time').empty();
		var end_moment = moment(moment_origin).add(animation_end,'s');
		$('#end_time').append(end_moment.format('HH:mm:ss'));
	};

	var switch_left_panel = function(choice, blocked){
		if (choice == 'control') {
			$('#control').show();
			$('#param').hide();
		}
		else if (choice == 'param') {
			$('#param').show();
			$('#control').hide();
			$('#set_t_start').val(0);
			$('#set_t_end').val(maxtimesim);
			// Show init moment
			$('#set_origin_h').val('00');
			$('#set_origin_m').val('00');
			$('#set_origin_s').val('00');

			if (blocked) {
				$('#close_config').hide();
			}
			else {
				$('#close_config').show();
			}
		}
	};


	/* ********************************************************
					CONTROLS
	******************************************************** */

	// FILTERS

	var filters = {

		path : [],
		path_temp : [],
		counter_path : 0,
		index_path : [],
		pick_path : false,
		OD : [],
		OD_temp : [],
		index_OD : [],
		counter_OD : 0,

		init : function(){

			$('#btn_path').hide();

			// add listener on the map
			map.dmap.data.addListener('click', function(event) {
				if (event.feature.getGeometry().getType() == 'LineString') {

					// if click to add link to current path
					if($('#f_path').parent().hasClass('active') && filters.pick_path) {
						filters.path_temp.push(event.feature.getProperty('id'));
						filters.display_links('path');
						map.color_links([event.feature.getProperty('id')], '#30D630');
					}
					// if click to add to current OD
					else if ($('#f_od').parent().hasClass('active')) {
						filters.OD_temp.push(event.feature.getProperty('id'));
						map.color_links([event.feature.getProperty('id')], '#30D630');

						if (filters.OD_temp.length == 2) {
							filters.OD.push(filters.OD_temp);
							map.color_links(filters.OD_temp, 'blue');
							filters.index_OD.push(filters.counter_OD);
							filters.counter_OD += 1;
							filters.OD_temp = [];
						}
						filters.display_links('od');
					}
				}
			});

			// add listeners
			$('.radio_filter').change(function(){
				var choice = 'none';
				if($(this).children().first().attr('id') == 'f_path') {
					choice = 'path';
				}
				else if ($(this).children().first().attr('id') == 'f_od') {
					choice = 'od';
				}
				filters.display_links(choice);
			});

			$('#new_path').click(function(){filters.pick_path = true; filters.path_temp = []; filters.display_links('path');});
			$('#save_path').click(function(){
				filters.pick_path = false; 
				if (filters.path_temp.length > 0){
					filters.index_path.push(filters.counter_path);
					filters.counter_path += 1;
					filters.path.push(filters.path_temp);
				}
				map.color_links(filters.path_temp, 'blue');
				filters.path_temp = [];
				filters.display_links('path');
			});

			$('#f_links').on('mouseover', '.saved_path', function(){
				var id = parseInt($(this).attr('id').slice(5));
				links = filters.path[id];
				map.color_links(links, '#30D630');
			});

			$('#f_links').on('mouseout', '.saved_path', function(){
				var id = parseInt($(this).attr('id').slice(5));
				links = filters.path[id];
				map.color_links(links, 'blue');
			});

			$('#f_links').on('click', '.delete_path', function(){
				var id = parseInt($(this).parent().attr('id').slice(5));
				links = filters.path[id];
				map.color_links(links, 'blue');
				filters.index_path.splice(filters.index_path.indexOf(id), 1);
				filters.display_links('path');
			});

			$('#f_links').on('mouseover', '.saved_OD', function(){
				var id = parseInt($(this).attr('id').slice(3));
				links = filters.OD[id];
				map.color_links(links, '#30D630');
			});

			$('#f_links').on('mouseout', '.saved_OD', function(){
				var id = parseInt($(this).attr('id').slice(3));
				links = filters.OD[id];
				map.color_links(links, 'blue');
			});

			$('#f_links').on('click', '.delete_OD', function(){
				var id = parseInt($(this).parent().attr('id').slice(3));
				links = filters.OD[id];
				map.color_links(links, 'blue');
				filters.index_OD.splice(filters.index_OD.indexOf(id), 1);
				filters.display_links('od');
			});

			$('.generate').click(function(){
				filters.generate();
			});

			$('#new_visu').click(function(){
				birdeye.pause();
				map.reset_colors();
				birdeye.clearmarkers();
				switch_left_panel('param', false);
			});

			$('#close_config').click(function(){
				switch_left_panel('control', false);
			});
		},

		display_links : function(choice) {

			$('#f_links').empty();
			$('#btn_path').hide();
			if(choice == 'path') {
				$('#btn_path').show();

				if (this.pick_path){
					$('#f_links').append('<h4>Click on the map to select the path</h4>')
					$('#f_links').append(JSON.stringify(this.path_temp));
				}

				if (filters.index_path.length > 0){
					$('#f_links').append('<br /><h4>Saved paths:</h4>');
				}

				for (var i = 0; i < this.index_path.length; i++){
					var index = this.index_path[i];
					$('#f_links').append('<span class="saved_path" id = "path_' + index +'"><img class="delete_path" src="'+ ref_img +'close.png" />Path n° '+ i +'</span><br />');
				}
							
			}
			else if (choice == 'od') {
				$('#f_links').append('<h4>Click on the map to select the OD:</h4>')
				$('#f_links').append(JSON.stringify(this.OD_temp));
				if (filters.index_OD.length > 0){
					$('#f_links').append('<br /><h4>Saved OD:</h4>');
				}

				for (var i = 0; i < this.index_OD.length; i++){
					var index = this.index_OD[i];
					$('#f_links').append('<span class="saved_OD" id = "OD_' + index +'"><img class="delete_OD" src="'+ ref_img +'close.png" />'+ JSON.stringify(this.OD[index]) +'</span><br />');
				}

			}
		},

		generate : function(){

			// Time selection
			var t_start = parseInt($('#set_t_start').val());
			var t_end = parseInt($('#set_t_end').val());

			// Time validation
			if (!(t_start >= 0 && t_end <= maxtimesim)){
				alert('Time interval selected is not valid !');
				return 1;
			}

			// Filter
			choice = 'none';
			if ($('#f_path').parent().hasClass('active')){choice = 'path';}
			else if ($('#f_od').parent().hasClass('active')){choice = 'od';}

			// Time origin
			var hour = parseInt($('#set_origin_h').val());
			var minute = parseInt($('#set_origin_m').val());
			var second = parseInt($('#set_origin_s').val());

			// we check if they are all integer
			if (isInt(hour) && isInt(minute) && isInt(second)){
				if (hour < 0 || hour > 23 || minute < 0 || minute > 59 || second < 0 || second > 59 ) {
					alert('Integer out of bound');
					return 1;
				}
				else {
					moment_origin = moment({'hour': hour, 'minute': minute, 'second': second});
					display_startend_time();
				}
			}
			else {
				alert('You must provide integer arguments');
				return 1;
			}

			// Build options
			var options = {};
			options['t_start'] = t_start;
			options['t_end'] = t_end;
			options['filter'] = choice;
			options['paths'] = [];
			for (var i = 0; i < this.index_path.length; i++){
				var index = this.index_path[i];
				options.paths.push(this.path[index]);
			}
			options['ods'] = [];
			for (var i = 0; i < this.index_OD.length; i++){
				var index = this.index_OD[i];
				options.ods.push(this.OD[index]);
			}

			// Show laoder, Hide map
			$('#map-canvas').hide();
			$('.loader').show();

			$.post( "../pointqanalysis/ajax?action=bird_traj", {'action': 'bird_traj','conf': JSON.stringify(options)}, function( data ) {
				data = JSON.parse(data);

				if (!data.vehicles || !data.occupation){
					$("#step1").empty();
					$("#step1").append('<h3>The data hasn\'t been processed yet, please come back in few minutes</h3>')
				}
				else {
					animation_start = t_start;
					animation_end = t_end;

					// Animation Conf
					conf = {};
					conf.end_time = animation_end;
					conf.start_time = animation_start;
					conf.json_birdeye = data.occupation;
					conf.history_vehicle = data.vehicles;

					birdeye.modifnewsimu(conf);

					// Interface conf
					display_startend_time();
					switch_left_panel('control', false);
					// Hide laoder, Show map
					$('#map-canvas').show();
					$('.loader').hide();

					birdeye.restart();
				}
			});
		}
	};

	// BASIC CONTROLS

		// PLAY
		$('.play').click(function() {
			birdeye.play();
		});

		// PAUSE
		$('.pause, #field_time_simu, .time_origin, .jump').click(function() {
			birdeye.pause();
		});

		// RESTART
		$('.restart').click(function() {
			birdeye.restart();
		});

	// SPEED CONTROL

		$('.radio_speed').click(function(){
			var id = $(this).children().first().attr('id');
			
			if (id == "radio_s1") {
				birdeye.timestep = 0.1;
				birdeye.simu_time_step = 0.1;
			}
			else if (id == "radio_s2") {
				birdeye.timestep = 0.1;
				birdeye.simu_time_step = 1;
			}
			else if (id == "radio_s3") {
				birdeye.pause();
				birdeye.simu_time = Math.round(birdeye.simu_time / 10) * 10;
				birdeye.timestep = 0.1;
				birdeye.simu_time_step = 10;
				birdeye.play();
			}
		});

	// JUMP TO
		$('.btn-jump').click(function(){
			// First step, we gather the values
			var hour = $('#field_time_simu_h').val();
			var minute = $('#field_time_simu_m').val();
			var second = $('#field_time_simu_s').val();

			// Second step, we check if they are all integer within correct bonds
			if (isInt(hour) && isInt(minute) && isInt(second)){
				if (hour < 0 || hour > 23 || minute < 0 || minute > 59 || second < 0 || second > 59 ) {
					alert('Integer out of bound');
				}
				else {
					// we create a moment and determine the difference with the origin moment in seconds
					var moment_jumped = moment({'hour': hour, 'minute': minute, 'second': second});
					
					var difference = moment_jumped.diff(moment_origin, 's');

					if (difference < animation_start || difference >= animation_end) {
						alert('The moment you entered hasn\'t been simulated');
					}
					else {
						// we approximate the value to the nearest multiple of 5
						while(difference % 5 != 0){
							difference += 1;
						}

						birdeye.goto(difference);
					}
				}
			}
		});


	/* ********************************************************
					TOOLS
	******************************************************** */

	var isInt = function(x) {
		var y = parseInt(x, 10);
		return !isNaN(y) && x == y && x.toString() == y.toString();
	};

	/* ********************************************************
					INIT + RETURN OBJECT
	******************************************************** */

	init();
	return {get_moment_origin: function(){return moment_origin}, progressBar: nanobar, display_time: function(time){display_moment(time);}, switch_left_panel: function(choice, blocked){switch_left_panel(choice, blocked);}};

};
