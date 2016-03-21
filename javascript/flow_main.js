// Create the Google Map…
var lines = [];
var flowmap = new google.maps.Map(d3.select("#flowmap").node(), {
    zoom: 8,
    center: new google.maps.LatLng(52.3, 5.3),
    mapTypeId: google.maps.MapTypeId.ROADMAP,
	minZoom: 7,
	maxZoom: 13
});
redraw(8);
draw_overlay(8);
stop_wait(["waitF"]);

flowmap.addListener('zoom_changed', function() {
	start_wait(["waitF"]);
    var zoom = flowmap.getZoom();
    redraw(zoom);
    draw_overlay(zoom);
	stop_wait(["waitF"]);
});

var lineSymbol = {
    path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW
};

function redraw(zoom)
{
    while (lines.length > 0)
        lines.pop().setMap(null);
    
    d3.json("../Flow/flow_" + zoom + ".json", function(error, data) {
        if (error) throw error;

        // get the sum of all migrations for arrow size normalisation
        var total = 0;
        for (var from in data) {
            for (var to in data[from]) {
                total += data[from][to];
            }
        }

        d3.json("../Flow/cities_" + zoom + "_clusters.json", function(error, cities) {
            if (error) throw error;

            for (var from in data) {
                for (var to in data[from]) {
                    if (from == to)
                        continue;

                    var from_coords = cities[from];
                    var to_coords = cities[to];

                    if (!from_coords || !to_coords)
                        continue;

                    var line = new google.maps.Polyline({
                        path: [{lat: from_coords[0], lng: from_coords[1]},
                               {lat: to_coords[0], lng: to_coords[1]}],
                        icons: [{
                            icon: lineSymbol,
                            offset: '100%'
                        }],
                        map: flowmap,
                        strokeColor: 'slategray',
                        strokeOpacity: 0.7,
                        strokeWeight: (data[from][to] / total) * 2000
                    });

                    lines.push(line);
                }
            }
        });
    });
}

function draw_overlay(zoom) {
  d3.json("../Flow/cities_" + zoom + "_clusters.json", function(error, data) {
    if (error) throw error;

    var overlay = new google.maps.OverlayView();
    d3.selectAll(".linestuff").remove();

    // Add the container when the overlay is added to the map.
    overlay.onAdd = function() {
        var layer = d3.select(this.getPanes().overlayLayer).append("div")
            .attr("class", "stations");

        // Draw each marker as a separate SVG element.
        // We could use a single SVG, but what size would it have?
        overlay.draw = function() {
        var projection = this.getProjection(),
            padding = 10;

        var marker = layer.selectAll("svg")
            .data(d3.entries(data))
            .each(transform) // update existing markers
            .enter().append("svg")
            .each(transform)
            .attr("class", "linestuff");

        // Add a circle.
        marker.append("circle")
            .attr("r", 5)
            .attr("cx", padding)
            .attr("cy", padding);

        function transform(d) {
            d = new google.maps.LatLng(d.value[0], d.value[1]);
            d = projection.fromLatLngToDivPixel(d);
            return d3.select(this)
                .style("left", (d.x - padding) + "px")
                .style("top", (d.y - padding) + "px");
        }
        };
    };

    // Bind our overlay to the map…
    overlay.setMap(flowmap);
    }
  );
}
