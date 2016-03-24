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
            htm += '<b><u> Omgeving: '+ inv[0][0] + '</u></b>'
            htm += '<br>Investering in Euros<br>';
        for(k=0; k<inv.length; k++){
        htm += '<p>';

        //if (inv[k][1] == '2010'){
        //   htm += '<i><b>Year: 2014</i></b> -- ';}
        if(inv[k][1] == '2011')
        {
        //else if(inv[k][1]=='2013*')
        //{   htm += '<i><b>Year: 2013 </i></b>-- '
        //}
        //else {
                htm += '<i><b>Jaar: ' + inv[k][1] + '</i></b> <br>';
        
                htm += '<u>Bedrijfsgebouwen:</u> '+inv[k][3]+' mln <br> ';
                htm += '<u>Grond-weg- en waterbouwkundige werken:</u> '+inv[k][4]+'mln <br> ';
                htm += '<u>Vervoermiddelen:</u> '+inv[k][5]+' mln <br> ';
                htm += '<u>Machines en installaties:</u> '+inv[k][6]+' mln <br> ';
                htm += '<u>In cultuur gebrachte activa:</u> '+inv[k][7]+' mln <br> ';
                htm += '<u>Overdrachtskosten op grond:</u> '+inv[k][8]+' mln <br> ';
                htm += '<u>Computerprogrammatuur en databanken:</u> '+inv[k][9]+' mln <br> ';
                htm += '<u>Onderzoek en ontwikkeling:</u> '+inv[k][10]+' mln <br> ';
                htm += '<u>Overige investeringen:</u> '+inv[k][11]+' mln <br> ';
        }
        }
            }
        

        to = data.links[j]['target'];
        from = data.links[j]['source'];
        htm += '<br> <i>Aantal studenten van ';
        htm += data.nodes[from]['name'] + ' ->'+ data.nodes[to]['name'] + '</i>: ' +data.links[j]['value'];
    

}
    htm += '</p>'
    htm += '</p>'
    htm += '</div>'; 
    document.getElementById("info").innerHTML = htm;
}


function info_update() {
	start_wait(["waitI"]);
	var xhttp = new XMLHttpRequest();
	xhttp.open("GET", host + "/info/update", true)
	xhttp.send();
	xhttp.onreadystatechange = function(){
		if (xhttp.readyState == 4 && xhttp.status == 200) {
			var data = JSON.parse(xhttp.responseText);
			show_info(data);
			stop_wait(["waitI"]);
		}
	}
}

info_update()
