var svg = d3.select("#chart").append("svg")

var make_sankey = function(energy) {
	svg.selectAll("*").remove();
	if (energy.links.length == 0) {
		var bar = svg.append("g")
					.attr("transform", "translate(10,10)");

		bar.append("text")
			.attr("x", 10)
			.attr("y", 30)
			.attr("dy", ".35em")
			.text("Not enough data");
		return;
	}
	
	var margin = {top: 1, right: 1, bottom: 1, left: 1},
		width = document.getElementById("chart").clientWidth - margin.left - margin.right,
		height = document.getElementById("chart").clientHeight - margin.top - margin.bottom;

	var formatNumber = d3.format(",.0f"),
		format = function(d) { return formatNumber(d) + " students"; },
		color = d3.scale.category20();

	svg
			.attr("width", width + margin.left + margin.right)
			.attr("height", height + margin.top + margin.bottom)
		.append("g")
			.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	var sankey = d3.sankey()
			.nodeWidth(15)
			.nodePadding(10)
			.size([width, height]);

	var path = sankey.link();
	
	sankey
			.nodes(energy.nodes)
			.links(energy.links)
			.layout(32);

	var link = svg.append("g").selectAll(".link")
			.data(energy.links)
		.enter().append("path")
			.attr("class", "link")
			.attr("d", path)
			.style("stroke", function(d) { return d.color; } )
			.style("stroke-width", function(d) { return Math.max(1, d.dy); })
			.sort(function(a, b) { return b.dy - a.dy; });

	link.append("title")
			.text(function(d) { return d.source.name + " -> " + d.target.name +"( "+d.region+" )"+ "\n" + format(d.value); });

	var node = svg.append("g").selectAll(".node")
			.data(energy.nodes)
		.enter().append("g")
			.attr("class", "node")
			.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
		.call(d3.behavior.drag()
			.origin(function(d) { return d; })
			.on("dragstart", function() { this.parentNode.appendChild(this); })
			.on("drag", dragmove));

	node.append("rect")
			.attr("height", function(d) { return d.dy; })
			.attr("width", sankey.nodeWidth())
			.style("fill", function(d) { return d.color = color(d.name.replace(/ .*/, "")); })
			.style("stroke", function(d) { return d3.rgb(d.color).darker(2); })
		.append("title")
			.text(function(d) { return d.name + "\n" + format(d.value); });

	node.append("text")
			.attr("x", -6)
			.attr("y", function(d) { return d.dy / 2; })
			.attr("dy", ".35em")
			.attr("text-anchor", "end")
			.attr("transform", null)
			.text(function(d) { return d.name; })
		.filter(function(d) { return d.x < width / 2; })
			.attr("x", 6 + sankey.nodeWidth())
			.attr("text-anchor", "start");

	function dragmove(d) {
		d3.select(this).attr("transform", "translate(" + 
		d.x + //(d.x = Math.max(0, Math.min(width - d.dx, d3.event.x)))+
			"," + (d.y = Math.max(0, Math.min(height - d.dy, d3.event.y))) + ")");
		sankey.relayout();
		link.attr("d", path);
	}
}

function sankey_update() {
	xhttp.open("GET", host + "/sankey/update", false)
	xhttp.send();
	var data = JSON.parse(xhttp.responseText);
	make_sankey(data);
}

sankey_update()