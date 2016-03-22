// Create the Google Map…
var lines = [];
var flowmap = new google.maps.Map(d3.select("#flowmap").node(), {
    zoom: 8,
    center: new google.maps.LatLng(52.3, 5.3),
    mapTypeId: google.maps.MapTypeId.ROADMAP,
	minZoom: 7,
	maxZoom: 13
});
var overlayF = new google.maps.OverlayView();
overlayF.onAdd = function() {
	var layer = d3.select(this.getPanes().overlayMouseTarget).append("div")
		.attr("class", "stations");
	this.draw = function(){};
};
// Bind our overlay to the map…
overlayF.setMap(flowmap);

var rect = document.getElementById('flowmap').getBoundingClientRect();
var inout = document.getElementById('in-out-but');
inout.style.top = rect.top+5+"px";
inout.style.left = rect.right-65+"px";1

show_from = true;
show_to = true;

//map.addListener('zoom_changed', map_init);
//redraw(8);
//draw_overlay(8);

flowmap.addListener('zoom_changed',flow_zoom);

function flow_zoom() {
	var zoom = Math.pow(2, flowmap.zoom - zoomer(map.zoom));
	if (zoomer(map.zoom) != map.zoom) {
		zoom /= 2;
	}
	var projection = overlayF.getProjection();
	var layer = d3.select(overlayF.getPanes().overlayMouseTarget).select("div.stations");
	layer.selectAll('.marker').each(transform);
	
	function transform(d) {
		dl = new google.maps.LatLng(d.value.loc[0], d.value.loc[1]);
		dl = projection.fromLatLngToDivPixel(dl);
		d3.select(this).select('circle')
				.attr("r", zoom*d.value.rad)
				.attr("cx", zoom*d.value.rad+1)
				.attr("cy", zoom*d.value.rad+1)
		return d3.select(this)
			.style("left", (dl.x - zoom*d.value.rad-1) + "px")
			.style("top", (dl.y - zoom*d.value.rad-1) + "px")
			.attr("width", zoom*d.value.rad * 2 + 2 + "px")
			.attr("height", zoom*d.value.rad * 2 + 2 + "px");
	}
}

function zoomer(zoom) {
	if (zoom == '9')
		return '8';
	if (zoom == '11')
		return '10';
	if (zoom == '13')
		return '12';
	return zoom;
}

/*flowmap.addListener('zoom_changed', function() {
	start_wait(["waitF"]);
    var zoom = flowmap.getZoom();
    redraw(zoom);
    draw_overlay(zoom);
	stop_wait(["waitF"]);
});*/

var lineSymbol = {
    path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW
};

function draw_lines(data) {
	while (lines.length > 0)
        lines.pop().setMap(null);
	
	for (var i in data) {
		var point = data[i];
		from_coords = point['loc'];
		if ('to_link' in point) {
			for (var j in point['to_link']) {
				var line = point['to_link'][j];
				to_coords = data[line['id']].loc;
				if ('col' in line) {
					put_line(from_coords,to_coords,line['n'],'black',data[line['id']]['name']);
				} else {
					put_line(from_coords,to_coords,line['n'],'red',data[line['id']]['name']);
				}
			}
		}
		if ('from_link' in point) {
			for (var j in point['from_link']) {
				var line = point['from_link'][j];
				to_coords = data[line['id']].loc;
				put_line(to_coords,from_coords,line['n'],'green',data[line['id']]['name']);
			}
		}
	}
	hide_lines();
	stop_wait("waitF");
}

function hide_lines() {
	for (var i in lines) {
		var line = lines[i];
		if (line.strokeColor == 'red') {
			if (show_to) {
				line.setMap(flowmap);
			} else {
				line.setMap(null);
			}
		} else if (line.strokeColor == 'green') {
			if (show_from) {
				line.setMap(flowmap);
			} else {
				line.setMap(null);
			}
		}
	}
}

function put_line(from_coords,to_coords,size,col,name) {
	var line = new google.maps.Polyline({
			path: [{lat: from_coords[0], lng: from_coords[1]},
				   {lat: to_coords[0], lng: to_coords[1]}],
			/*icons: [{
				icon: lineSymbol,
				offset: '100%'
			}],*/
			map: flowmap,
			strokeColor: col,
			strokeOpacity: 0.2,
			strokeWeight: (size),
			title: ""+size+" students"
		});
	
	if (col == 'green') {
		var coo = {lat:to_coords[0], lng:to_coords[1]};
		var cont = ("<b>"+size+" students left for: "+name+"</b>").replace(/,/g, ', ');
	} else {
		var coo = {lat:from_coords[0], lng:from_coords[1]};
		var cont = ("<b>"+size+" students came from: "+name+"</b>").replace(/,/g, ', ');
	}
	
	var infowindow = new google.maps.InfoWindow({
		content: cont
	});
	
	line.addListener('mouseover', function() {
        this.setOptions({
            strokeOpacity : 1
        });
    });

    line.addListener('mouseout', function() {
		if (show) {
			this.setOptions({
				strokeOpacity : 0.2
			});
		}
    });
	
	var show = true;
	line.addListener('click', function() {
		if (show) {
			infowindow.setPosition(coo);
			infowindow.open(flowmap);
			this.setOptions({
				strokeOpacity : 1
			});
		} else {
			infowindow.close();
			this.setOptions({
				strokeOpacity : 0.2
			});
		}
		show = !show;
	});
	
	infowindow.addListener('closeclick', function() {
		show = true;
		line.setOptions({
			strokeOpacity : 0.2
		});
	});
	
	lines.push(line);
}
