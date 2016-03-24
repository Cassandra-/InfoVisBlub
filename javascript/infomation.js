function show_info(data)
{
    
	var width = document.getElementById("chart").clientWidth,
	    height = document.getElementById("chart").clientHeight;
    var htm = '<div style="overflow: auto; position: relative; width: '+width+'px; height: '+height+'px;"';
    city = [];
    for (j=0; j<data.links.length; j++)
    {   htm += '<p>'
        inv = data.links[j]['inv'];
        validate = 0;

        for (i=0; i<city.length; i++){
            if (city[i] == inv[0][0])
            { validate =1; break;}
        }
        if (validate==0){
            city.push(inv[0][0]);
            htm += '<b><u> Region: '+inv[0][0] + '</u></b>';
        for(k=0; k<inv.length; k++){
        htm += '<p>';

        if (inv[k][1] == '2010'){
            htm += '<i><b>Year: 2014</i></b> -- ';}
        else if(inv[k][1]=='2013*')
        {   htm += '<i><b>Year: 2013 </i></b>-- '
        }
        else {
            htm += '<i><b>Year: ' + inv[k][1] + '</i></b> --';
        }
        htm += 'Bedrijfsgebouwen: '+inv[k][3]+'mln Euro / ';
        htm += 'Grond-weg- en waterbouwkundige werken: '+inv[k][4]+'mln Euro / ';
        htm += 'Vervoermiddelen: '+inv[k][5]+'mln Euro / ';
        htm += 'Machines en installaties: '+inv[k][6]+'mln Euro / ';
        htm += 'In cultuur gebrachte activa: '+inv[k][7]+'mln Euro / ';
        htm += 'Overdrachtskosten op grond: '+inv[k][8]+'mln Euro / ';
        htm += 'Computerprogrammatuur en databanken: '+inv[k][9]+'mln Euro / ';
        htm += 'Onderzoek en ontwikkeling: '+inv[k][10]+'mln Euro / ';
        htm += 'Overige investeringen: '+inv[k][11]+'mln Euro / ';
    }
            }
        

        to = data.links[j]['target'];
        from = data.links[j]['source'];
        htm += '<br> <i>Nr of students from ';
        htm += data.nodes[from]['name'] + ' ->'+ data.nodes[to]['name'] + '</i>: ' +data.links[j]['value'];
    

}
    htm += '</p>'
    htm += '</p>'
    htm += '</div>'; 
    document.getElementById("info").innerHTML = htm;
}


function info_update() {
	start_wait(["waitS"]);
	var xhttp = new XMLHttpRequest();
	xhttp.open("GET", host + "/info/update", true)
	xhttp.send();
	xhttp.onreadystatechange = function(){
		if (xhttp.readyState == 4 && xhttp.status == 200) {
			var data = JSON.parse(xhttp.responseText);
			show_info(data);
			stop_wait(["waitS"]);
		}
	}
}

info_update()
