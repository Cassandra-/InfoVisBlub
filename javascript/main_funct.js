var host = "http://" + window.location.host;

var xhttp = new XMLHttpRequest();

xhttp.open("GET", host + "/list1/build" , false);
xhttp.send();
document.getElementById("sector_list").innerHTML = xhttp.responseText;

function sankey_update() {}

function change_sector(name,bool,t) {
	xhttp.open("GET", host + "/list1/select/"+name+"/"+bool+"/"+t, false);
	xhttp.send();
	document.getElementById("sector_list").innerHTML = xhttp.responseText;
	sankey_update();
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
	xhttp.open("GET", host + "/years/"+values[0]+"/"+values[1], false);
	xhttp.send();
	sankey_update();
});