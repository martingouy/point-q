$(function() {

	initialize();

	///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	// Interface
	///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

	$("#link_question").click(function(){
		$('#linkModal').modal();
	});
	$("#queue_question").click(function(){
		$('#queueModal').modal();
	});
	$("#OD_question").click(function(){
		$('#ODModal').modal();
	});
	$( "#clear_links_button" ).click(function() {
		$(".img_delete_flow").each(function() {
	    		deletable_flow_link(this);
		});
	});
	$( "#clear_ODs_button" ).click(function() {
		$(".img_delete_OD").each(function() {
		    deletable_OD(this);
		});
	});
	$( "#clear_queues_button" ).click(function() {
		$(".img_delete_queue").each(function() {
		    deletable_queue(this);
		});
	});

	//Manual Link
	$("#add_link").keyup(function(event){
	if(event.keyCode == 13){
	    $("#add_link_button").click();
	}
	});
	$( "#add_link_button" ).click(function() {
	                        var ids=$("#add_link").val();
			        ids=ids.split(" ");			    
	    $.each(ids, function( index, id_li ){
				// we add the link id to list_link
		addLink(id_li);
		$('#add_link').val("");
	    });
	});
	$("#add_q1").keyup(function(event){
	if(event.keyCode == 13){
	    $("#add_q_button").click();
	}
	});

        $("#add_q_button").click(function() {
						// we add the link id to list_queue_temp\
	    var pairs=$("#add_q1").val();
	    if (pairs !=""){
	    pairs=pairs.split("] ");
		$.each(pairs,function( index, pair ){
		    var matches = pair.match(/(\d+),\s*(\d+)/);
		    addQueue([matches[1],matches[2]]);
		    $("#add_q1").val("");
		});
	    }    
	});
    $("#add_OD").keyup(function(event){
	if(event.keyCode == 13){
	    $("#add_OD_button").click();
	}
    });
    $("#add_OD_button").click(function() {
						// we add the link id to list_queue_temp\
	    var pairs=$("#add_OD").val();
	    if (pairs !=""){
	    pairs=pairs.split("] ");
		$.each(pairs,function( index, pair ){
		    var matches = pair.match(/(\d+),\s*(\d+)/);
		    addOD([matches[1],matches[2]]);
		    $("#add_OD").val("");
		});
	    }
    });
	// Slider time simul
	var t_start_analysis;
	var t_end_analysis;

	$("#slider_time").ionRangeSlider({
		min: 0,
		max: maxtimesim,
		type: 'double',
		step: 1,
		postfix: " s",
		hasGrid: true,
		gridMargin: 15,
		onLoad: function (obj) {        // callback is called after slider load and update
			t_start_analysis = obj['fromNumber'];
			t_end_analysis = obj['toNumber'];
		},
		onChange: function (obj) {      // callback is called on every slider change
			t_start_analysis = obj['fromNumber'];
			t_end_analysis = obj['toNumber'];
		},
		onFinish: function (obj) {      // callback is called on slider action is finished
			t_start_analysis = obj['fromNumber'];
			t_end_analysis = obj['toNumber'];
		}
	});

	// Slider time granularity
	granularity= maxtimesim/ 2;
	$("#box_granularity").val(granularity);
	$("#box_granularity").keyup(function() {
					  granularity=$("#box_granularity").val();
					  });

	// granularity hide/show
	$('#lb_btn_analysis_flows').click(function() {
		if($('#btn_analysis_flows').prop('checked')) {
			$('#div_granularity').hide();
		}
		else {
			$('#div_granularity').show();
		}
	});

	// Generate plots
	$('#generate button').click(function() {

		// we delete previous plots
		$('#flowchart').children().remove();
		$('#queuechart').children().remove();
		$('#TTchart').children().remove();

		// we reset the heights of the plots divs
		$('#flowchart').css({'height': '', 'margin-bottom' : ''});
		$('#queuechart').css({'height': ''});
		$('#TTchart').css({'height': ''});

		// we determine which is the last analysis to be made
		var last_analysis = 'flow';
		if ($('#btn_analysis_queues').prop('checked') && list_queues.length != 0){
			last_analysis = 'queue';
		}
		if ($('#btn_analysis_TT').prop('checked') && list_ODs.length != 0){
			last_analysis = 'OD';
		}

		// if we want a flow analysis
		if ($('#btn_analysis_flows').prop('checked')) {

			if (list_links.length > 0 && t_end_analysis - t_start_analysis >= granularity) {

				$('#generate button').button('loading');
				$('#flowchart').css({'height': '400px', 'margin-bottom': '50px'});

				// generate flows plots
				var links = list_links[0];

				for (var i = 1; i < list_links.length; i++) {
					links += '-' + list_links[i];
				}

				// we generate the plot
				generate_json_plot(links, 'flow', t_start_analysis, t_end_analysis, last_analysis, granularity, false, false);
			}

			else {
				$('#generate button').button('reset');
			}
		}

		// if we want a queue analysis
		if ($('#btn_analysis_queues').prop('checked')) {

			if (list_queues.length > 0) {

				$('#generate button').button('loading');
				$('#queuechart').css({'height': '400px'});

				// we check if we want to separate queues based on origin links
				if (!$('#cb_queue_origin').prop('checked')) {
					// generate queues plots
					var queues = list_queues[0][0] + '.' + list_queues[0][1];

					for (var i = 1; i < list_queues.length; i++) {
						queues += '-' + list_queues[i][0] + '.' + list_queues[i][1];
					}
				}
				else {
					var i = 0;
					var queues = '';
					for (key in queues_w_origin) {
						var key = key.split(',');
						link_1 = key[0].substring(1);
						link_2 = key[1].substring(0, key[1].length - 1);

						if (i == 0) {
							queues += queues_w_origin[key] + '.' + link_1 + '.' + link_2;
							i++;
						}
						else {
							queues += '-' + queues_w_origin[key] + '.' + link_1 + '.' + link_2;
							i++;
						}
					}
				}

				// variable to know if we want total link occupancy
				var link_occupancy = $('#link_occupancy').prop('checked');

				// variable to know if we want separate queues based on origin links
				var sep_queues_origin = $('#cb_queue_origin').prop('checked');

				generate_json_plot(queues, 'queue', t_start_analysis, t_end_analysis, last_analysis, 0, link_occupancy, sep_queues_origin);
			}
		}

		if ($('#btn_analysis_TT').prop('checked')) {
			console.log('producing TT analysis')
			if (list_ODs.length > 0) {

				$('#generate button').button('loading');
				$('#TTchart').css({'height': '400px'});

				// generate queues plots
				var ODs = list_ODs[0][0] + '.' + list_ODs[0][1];

				for (var i = 1; i < list_ODs.length; i++) {
					ODs += '-' + list_ODs[i][0] + '.' + list_ODs[i][1];
				}
				generate_json_plot(ODs, 'OD', t_start_analysis, t_end_analysis, last_analysis, 0, false, false);
			}
		}
	});

	
	// Initial state : Hide queues/ OD / Queue with origin
	$('#queue').hide();
	$('#OD').hide();
	$('#left_tree_2').hide();

	// Show/Hide flow or queue div
	$('#left_tree label').click(function() {
		if ($(this).attr('analysis') == 'flow') {
			$('#queue').hide();
			$('#OD').hide();
			$('#flow').show();
			$('#left_tree_2').hide();
			indicator = 'flow';
		}
		else if ($(this).attr('analysis') == 'queue') {
			$('#flow').hide();
			$('#OD').hide();
			$('#queue').show();
			$('#left_tree_2').hide();
			indicator = 'queue';
		}
		else if ($(this).attr('analysis') == 'OD') {
			$('#flow').hide();
			$('#OD').show();
			$('#queue').hide();
			$('#left_tree_2').hide();
			indicator = 'OD';
		}
	});

	// Show the configuration panel 
	$('#config_queue_origin').click(function() {
		sync_panel();
		html_panel();
		$('#left_tree').hide();
		$('#left_tree_2').show();
	});

	// Hide configuration panel
	$('#queue_w_origin img').click(function() {
		$('#left_tree').show();
		$('#left_tree_2').hide();
	});

	$('#cb_queue_origin').click(function(){
		sync_panel();
	});

	// Generate the configuration panel

	// function to sync queues_w_origin with list_queues
	function sync_panel(){

		// we add new values
		for (var i = 0; i < list_queues.length; i++) {
			// we convert the queue into string
			str_queue = '[' + list_queues[i][0] + ',' + list_queues[i][1] + ']';

			// we check if the key already exist
			var flag = false;

			for (var key in queues_w_origin) {
				if (str_queue == key) {
					flag = true;
				}
			}

			if (flag == false) {
				queues_w_origin[str_queue] = 0;
			}
		}

		// we delete values
		for (var key in queues_w_origin) {

			// we check if the value exists
			var flag = false;

			for (var i = 0; i < list_queues.length; i++) {
				// we convert the queue into string
				str_queue = '[' + list_queues[i][0] + ',' + list_queues[i][1] + ']';
				if (str_queue == key) {
					flag = true;
				}
			}
			// we delete the key
			if (flag == false) {
				delete queues_w_origin[key];
			}
		}
	}

	// function to generate the html code for the panel
	function html_panel(){
		var code_html = '<table class="table" id="table_queue_w_origin"><tr><td>Queue</td><td>Origin</td></tr>';

		for (var key in queues_w_origin){
			code_html += '<tr><td>' + key + '</td><td><input type="text" class="form-control" queue="' + key + '" value="' + queues_w_origin[key] + '" /></td></tr>';
		}

		code_html += '</table>';
		// we replace the html code of the panel
		$('table#table_queue_w_origin').replaceWith(code_html);

		// we update the origin when modified
		$('#queue_w_origin input').change(function(){
			var new_value = $(this).val();
			var key = $(this).attr('queue');

			// we modify queues_w_origin
			queues_w_origin[key] = new_value;
		});
	}
});	