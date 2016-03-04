// Create the Google Map…
var map = new google.maps.Map(d3.select("#map").node(), {
    zoom: 8,
    center: new google.maps.LatLng(52.3, 5.3),
    mapTypeId: google.maps.MapTypeId.ROADMAP
});

var lineSymbol = {
    path: google.maps.SymbolPath.FORWARD_OPEN_ARROW
};

d3.json("flow.json", function(error, data) {
    if (error) throw error;
    
    d3.json("cities_2.json", function(error, cities) {
        if (error) throw error;

        for (var from in data) {
            for (var to in data[from]) {
                var from_coords = cities[from];
                var to_coords = cities[to];

                var line = new google.maps.Polyline({
                    path: [{lat: from_coords[0], lng: from_coords[1]},
                           {lat: to_coords[0], lng: to_coords[1]}],
                    icons: [{
                        icon: lineSymbol,
                        offset: '100%'
                    }],
                    map: map,
                    strokeColor: 'limegreen',
                    strokeOpacity: 0.7,
                    strokeWeight: data[from][to] / 5 // TODO: normalize properly
                });
            }
        }
    });
});
