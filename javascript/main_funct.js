var host = "http://" + window.location.host;

var xhttp = new XMLHttpRequest();

xhttp.open("GET", host + "/list1/build" , true);
xhttp.send();
xhttp.onreadystatechange = function() {
	document.getElementById("sector_list").innerHTML = xhttp.responseText;
	document.getElementById("waitC").style.display="none";
	document.getElementById("waitC").style.cursor="";
}

function sankey_update() {}
function map_init() {}

function change_sector(name,bool,t) {
	document.getElementById("waitC").style.display="block";
	document.getElementById("waitC").style.cursor="wait";
	var xhttp = new XMLHttpRequest();
	xhttp.open("GET", host + "/list1/select/"+name+"/"+bool+"/"+t, true);
	xhttp.send();
	xhttp.onreadystatechange = function() {
		document.getElementById("sector_list").innerHTML = xhttp.responseText;
		sankey_update();
		map_init();
		document.getElementById("waitC").style.display="none";
		document.getElementById("waitC").style.cursor="";
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
		sankey_update();
		map_init();
	}
});