///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Functions Search in array
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function in_array(string, array){
	var result = false;
	for(var i=0; i<array.length; i++){
		if(array[i] == string){
			result = true;
		}
	}
	return result;
}

function index_array(link1, link2, array) {
	var result = -1;
	for (var i = 0; i < array.length; i++) {
		if(array[i][0] == link1 && array[i][1] == link2) {
			return i;
		}
	}

	return result;
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Function Generate Graph
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function generate_json_plot(link_id, type, t_start, t_end, last_analysis, granul, link_occupancy, sep_queues_origin) {
	// First case: type flow
	if (type == 'flow') {
		// on crée une requête ajax asynchrone
		$.getJSON('../pointqanalysis/ajax?action=generate_json_plot', {'links': link_id, 'type': type, 't_start': t_start, 't_end': t_end, 'granul': granul}, function(data) {
				var chart = new CanvasJS.Chart("flowchart", data);
				chart.render();

				if (last_analysis == 'flow') {
					$('html, body').animate({
						scrollTop: $("#generate").offset().top
					}, 1000);
					// we reset the generate button
					$('#generate button').button('reset');
				}
		});
	}
	// Second cas: type queue
	else if (type == 'queue') {
		// on crée une requête ajax asynchrone
		$.getJSON('../pointqanalysis/ajax?action=generate_json_plot', {'queues': link_id, 'type': type, 't_start': t_start, 't_end': t_end, 'link_occupancy': link_occupancy, 'sep_queues_origin': sep_queues_origin}, function(data) {
				var chart = new CanvasJS.Chart("queuechart", data);
				chart.render();

				if (last_analysis == 'queue') {
					$('html, body').animate({
						scrollTop: $("#generate").offset().top
					}, 1000);
					// we reset the generate button
					$('#generate button').button('reset');
				}
		});
	}
    else if (type == 'OD'){
    	console.log('about to call ajax for TT');
		$.getJSON('../pointqanalysis/ajax?action=generate_json_plot', {'ODs': link_id, 'type': type, 't_start': t_start, 't_end': t_end}, function(data) {
			console.log('received data');
			var chart = new CanvasJS.Chart("TTchart", data);
			chart.render();
			if (last_analysis == 'OD') {
				$('html, body').animate({
					scrollTop: $("#generate").offset().top
				}, 1000);
				// we reset the generate button
				$('#generate button').button('reset');
			}
		});
    }

}