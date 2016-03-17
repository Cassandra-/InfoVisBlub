// Create the Google Map
var map = new google.maps.Map(d3.select("#map").node(), {
  zoom: 8,
  center: new google.maps.LatLng(52.3, 5.3),
  mapTypeId: google.maps.MapTypeId.TERRAIN,
  minZoom: 7,
  maxZoom: 13
});

function map_init() {
	document.getElementById("waitM").style.display="block";
	document.getElementById("waitM").style.cursor="wait";
	var xhttp = new XMLHttpRequest();
	xhttp.open("GET", host + "/regions/"+map.zoom, true);
	xhttp.send();
	xhttp.onreadystatechange = function(){
		var data = JSON.parse(xhttp.responseText);
		update_map(data);
		document.getElementById("waitM").style.display="none";
		document.getElementById("waitM").style.cursor="";
	}
}

function update_map(data) {
	var layer = d3.select(overlay.getPanes().overlayMouseTarget).select("div.stations");
	layer.selectAll(".marker").remove();
	
	// Draw each marker as a separate SVG element.
	// We could use a single SVG, but what size would it have?
	//overlay.draw = function() {
	var projection = overlay.getProjection();

	var marker = layer.selectAll("svg")
	  .data(d3.entries(data))
	  .each(transform) // update existing markers
	.enter().append("svg")
	  .each(transform)
	  .attr("width", function(i,d) { return i.value.rad * 2 + 2 + "px";})
	  .attr("height", function(i,d) { return i.value.rad * 2 + 2 + "px";})
	  .attr("class", "marker");

	// Add a circle.
	marker.append("circle")
	  .attr("r", function(i,d) { return i.value.rad; })
	  .attr("cx", function(i,d) {return i.value.rad+1;})
	  .attr("cy", function(i,d) {return i.value.rad+1;})
	  .attr("onclick", function(i,d) {return "update_regions("+i.value.special+","+i.key+")";})
	  .attr("style", function(i,d) {
						if (i.value.special) {
							return 'fill:blue;opacity:0.2;'
						} else if (i.value.selected == "true") {
							return 'fill:blue;';
						} else {
							return 'fill:brown;';
						}
					});

	function transform(d) {
	dl = new google.maps.LatLng(d.value.loc[0], d.value.loc[1]);
	dl = projection.fromLatLngToDivPixel(dl);
	return d3.select(this)
		.style("left", (dl.x - d.value.rad-1) + "px")
		.style("top", (dl.y - d.value.rad-1) + "px");
	}
};


var overlay = new google.maps.OverlayView();
// Add the container when the overlay is added to the map.
overlay.onAdd = function() {
	var layer = d3.select(this.getPanes().overlayMouseTarget).append("div")
		.attr("class", "stations");
	// Bind our overlay to the map…
	this.draw = map_init;
};
overlay.setMap(map);

map.addListener('zoom_changed', map_init);



function update_regions(special,id) {
	document.getElementById("waitM").style.display="block";
	document.getElementById("waitM").style.cursor="wait";
	var xhttp = new XMLHttpRequest();
	if (special) {
		xhttp.open("GET", host + "/regions/"+special+"/"+id+"/"+map.zoom, true);
	} else {
		xhttp.open("GET", host + "/regions/"+map.zoom+"/"+id+"/"+map.zoom, true);
	}
	xhttp.send();
	xhttp.onreadystatechange = function(){
		var data = JSON.parse(xhttp.responseText);
		update_map(data);
		sankey_update();
		document.getElementById("waitM").style.display="none";
		document.getElementById("waitM").style.cursor="";
	}
}