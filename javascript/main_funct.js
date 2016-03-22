var host = "http://" + window.location.host;

var xhttp = new XMLHttpRequest();

xhttp.open("GET", host + "/list1/build" , true);
xhttp.send();
xhttp.onreadystatechange = function() {
	if (xhttp.readyState == 4 && xhttp.status == 200) {
		document.getElementById("sector_list").innerHTML = xhttp.responseText;
		stop_wait("waitC");
	}
}

function sankey_update() {}
function map_init() {}

function start_wait(ids) {
	if (typeof(ids) == "string") {
		document.getElementById(ids).style.display="block";
		document.getElementById(ids).style.cursor="wait";
	} else {
		for (var id in ids) {
			document.getElementById(ids[id]).style.display="block";
			document.getElementById(ids[id]).style.cursor="wait";
		}
	}
}
function stop_wait(ids) {
	if (typeof(ids) == "string") {
		document.getElementById(ids).style.display="none";
		document.getElementById(ids).style.cursor="";
	} else {
		for (var id in ids) {
			document.getElementById(ids[id]).style.display="none";
			document.getElementById(ids[id]).style.cursor="";
		}
	}
}
		

function change_sector(name,bool,t) {
	start_wait(["waitC","waitM","waitS","waitF"]);
	var xhttp = new XMLHttpRequest();
	xhttp.open("GET", host + "/list1/select/"+name+"/"+bool+"/"+t, true);
	xhttp.send();
	xhttp.onreadystatechange = function() {
		if (xhttp.readyState == 4 && xhttp.status == 200) {
			document.getElementById("sector_list").innerHTML = xhttp.responseText;
			//animate_table()
			sankey_update();
			map_init();
			stop_wait(["waitC"]);
		}
	}
}

function animate_table() {
	vertical_offset = 20; // Start at header height
	
	for ( index = 0; index < 20; index++) {
		$("#mytr"+index).stop().delay(300 * index).animate({ top: vertical_offset}, 300, 'swing');
		vertical_offset += 20.8;
	}
}

var range = document.getElementById('range');
noUiSlider.create(range, {
	start: [ 2011, 2014 ], // Handle start position
	step: 1, // Slider moves in increments of '10'
	margin: 0, // Handles must be more than '20' apart
	connect: true, // Display a colored bar between the handles
	//direction: 'rtl', // Put '0' at the bottom of the slider
	//orientation: 'vertical', // Orient the slider vertically
	behaviour: 'tap-drag', // Move handle on tap, bar is draggable
	range: { // Slider can select '0' to '100'
		'min': 2011,
		'max': 2014
	},
	pips: { // Show a scale with the slider
		mode: 'steps',
		density: 12
	}
});

// When the slider value changes, update the input and span
range.noUiSlider.on('update', function( values, handle ) {
	var xhttp = new XMLHttpRequest()
	xhttp.open("GET", host + "/years/"+values[0]+"/"+values[1], true);
	xhttp.send();
	xhttp.onreadystatechange = function() {
		if (xhttp.readyState == 4 && xhttp.status == 200) {
			sankey_update();
			map_init();
		}
	}
});