// Create the Google Map
var map = new google.maps.Map(d3.select("#map").node(), {
  zoom: 8,
  center: new google.maps.LatLng(52.3, 5.3),
  mapTypeId: google.maps.MapTypeId.TERRAIN,
  minZoom: 7,
  maxZoom: 11
});


function update_map() {
	console.log('hello');
	var layer = d3.select(overlay.getPanes().overlayMouseTarget).select("div.stations");
	layer.selectAll(".marker").remove();
	
	d3.json("./Geomap/cities_"+map.zoom+"_clusters.json", function(error, data) {
		if (error) throw error;
		// Draw each marker as a separate SVG element.
		// We could use a single SVG, but what size would it have?
		//overlay.draw = function() {
		  var projection = overlay.getProjection(),
			  padding = 0;

		  var marker = layer.selectAll("svg")
			  .data(d3.entries(data))
			  .each(transform) // update existing markers
			.enter().append("svg")
			  .each(transform)
			  .attr("class", "marker")
			  .attr("onclick", function(i,d) {return "update_regions(this,"+d+")";});

		  // Add a circle.
		  marker.append("circle")
			  .attr("r", 10)
			  .attr("cx", 11)
			  .attr("cy", 11);
			
		  function transform(d) {
			d = new google.maps.LatLng(d.value[0], d.value[1]);
			d = projection.fromLatLngToDivPixel(d);
			return d3.select(this)
				.style("left", (d.x - padding) + "px")
				.style("top", (d.y - padding) + "px");
		  }
		//};
	});
};


var overlay = new google.maps.OverlayView();
// Add the container when the overlay is added to the map.
overlay.onAdd = function() {
	var layer = d3.select(this.getPanes().overlayMouseTarget).append("div")
		.attr("class", "stations");
	// Bind our overlay to the map…
	this.draw = update_map;
};
overlay.setMap(map);

map.addListener('zoom_changed', update_map);



function update_regions(obj,id) {
	xhttp.open("GET", host + "/regions/"+map.zoom+"/"+id, false);
	xhttp.send();
	if (xhttp.responseText == 'true') {
		obj.children[0].style['fill'] = 'blue';
	} else {
		obj.children[0].style['fill'] = 'brown';
	}
	
	sankey_update();
}