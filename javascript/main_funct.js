var host = "http://" + window.location.host;

var xhttp = new XMLHttpRequest();
xhttp.open("GET", host + "/list1/build" , false);
xhttp.send();
document.getElementById("sector_list").innerHTML = xhttp.responseText;

function change_sector(name,bool,t) {
	xhttp.open("GET", host + "/list1/select/"+name+"/"+bool+"/"+t, false);
	xhttp.send();
	sankey_update();
}