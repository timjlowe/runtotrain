

function testFunction()
	{
		document.write("YOOOOOOOHOOOOO");
	}	

function ajaxCallForStations(location, distance) 
	{
		var htmlCode = '';

		$.ajax({
			type: "GET",
			url: "/newSearch",
			//contentType: "application/json; charset=utf-8",
			//dataType: 'json',
			//data: {location: location, distance: distance},

		
		});
	}
//DOESNT WORK NEED TO FIX
function displayStations(stationResponse)	
	{
		
		document.write(stationResponse);
		//$.each(stationResponse, function(i, station) {
		//	('<tr>').append(
	//		('<td>').text(station.name),
//			('<td>').text(station.distance)
		//).appendTo('#station_table');
		//})
	}
function getStations(location, distance)
	{
		ajaxCallForStations(location, distance).done(displayStations);
	}
