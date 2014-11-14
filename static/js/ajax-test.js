

function testFunction()
	{
		document.write("YOOOOOOOHOOOOO");
	}	

function ajaxCallForStations(location, distance) 
	{

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
function getStations(location, distance, elementId)
	{
		var htmlCode = '';

		$.ajax({
			type: "POST",
			url: "/newSearch",
			contentType: "application/json; charset=utf-8",
			dataType: 'json',
			data: {location: location, distance: distance},
			success: function(data) {
				//Setup Table

				var table = $("<table>").attr("border", "1");
				table.append(row = $("<tr>"));
					$.each(data[0], function (key ,value) {
		 				row.append("<th>" + key);
		    		})

				$.each(data, function (i,value) {
					table.append(row = $("<tr>"));
						$.each(value, function (key,elementValue) {
		 				row.append("<td>" + elementValue + "</td>");
		   			})
		   		})

				$("#"+elementId).html(table)

		    },
  			error: function(e) {
				//called when there is an error
				//console.log(e.message);
			}	
		});
	}
