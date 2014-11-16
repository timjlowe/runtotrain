

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

function getStationAndRoutes(targetElement)
	{
    //<dd class="accordion-navigation">
    //	<a href="#panel3">Accordion 3</a>
    //	<div id="panel3" class="content">
    //  		Panel 3. Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
    //	</div>  

	var accordian = $("<dd>, { 'class': 'accordion-navigation'}");
		accordian.append('<a href="#panel3"> Accordian3</a>');
		accordian.append('<div id="panel3" class="content">').append("TEXTTEXT");

		$(targetElement).html(accordian)

    }


function getStations(location, distance, elementId)
	{
		//Initial go and displaying results
		var htmlCode = '';

		$.ajax({
			type: "POST",
			url: "/newSearch",
			contentType: "application/json; charset=utf-8",
			dataType: 'json',
			data: {location: location, distance: distance},
			success: function(data) {
				//Setup Table

				var table = $("<table>")//.attr("border", "1");
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
		getStationAndRoutes("#queryResults2")
	}





