var dash_interface = function(options) {

	/* ********************************************************
					VARIABLES
	******************************************************** */
	var nanobar;
	var moment_origin = moment({hour: 0, minute: 0, second: 0});
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

		// TIME ORIGIN
		$('#set_origin_h').val(moment_origin.hour());
		$('#set_origin_m').val(moment_origin.minute());
		$('#set_origin_s').val(moment_origin.second());

		//init end time
		display_end_time();
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

	
	var  display_end_time = function(){
		// function to display the end_time
		$('#end_time').empty();
		var end_moment = moment(moment_origin).add(maxtimesim,'s');
		$('#end_time').append(end_moment.format('HH:mm:ss'));
	};


	/* ********************************************************
					CONTROLS
	******************************************************** */

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
				birdeye.timestep = 0.1;
				birdeye.simu_time_step = 10;
			}
		});

	// SET TIME ORIGIN
		$('.set_time_origin').click(function(){
			var hour = $('#set_origin_h').val();
			var minute = $('#set_origin_m').val();
			var second = $('#set_origin_s').val();

			// we check if they are all integer
			if (isInt(hour) && isInt(minute) && isInt(second)){
				if (hour < 0 || hour > 23 || minute < 0 || minute > 59 || second < 0 || second > 59 ) {
					alert('Integer out of bound');
				}
				else {
					moment_origin = moment({'hour': hour, 'minute': minute, 'second': second});
					display_end_time();
				}
			}
			else {
				alert('You must provide integer arguments');
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

					if (difference < 0 || difference >= maxtimesim) {
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
	return {get_moment_origin: function(){return moment_origin}, progressBar: nanobar, display_time: function(time){display_moment(time);}};

};
