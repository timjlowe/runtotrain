

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

function addAcordian(targetElement, routeData)
	{
    //<dd class="accordion-navigation">
    //	<a href="#panel3">Accordion 3</a>
    //	<div id="panel3" class="content">
    //  		Panel 3. Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
    //	</div>  


	//Count of the number of accordian
	countOfAccordians = countOfAccordians +1;

    var routeDataTitle = routeData['station'] + ' - Distance: ' + routeData['distance'];
	var routeDataTable = $("<table>")
	var	routeDataTableHeader = '<th>Leg</th><th>Start Station</th><th>Time</th>';

	routeDataTable.append(row = $(routeDataTableHeader));


	//targetElement.append(routeDataTable, routeDataTableHeader);

		$.each(routeData['legs'], function (i,value) {
			var routeDataTableRow = '<tr><td>' + value['leg'] + '</td>' +
				'<td>' + value['start_station'] + '</td>' + 
				'<td>' + value['time'] + '</td></tr>';
				//alert(value['time'])

			routeDataTable.append(routeDataTableRow);

   		})

		//$("#"+targetElement).html(routeDataTable)

	var accordian = $("<dd>, { 'class': 'accordion-navigation'}");
		accordian.append('<a href="#panel'+ countOfAccordians +'">' + routeDataTitle + '</a>');
		//accordian.append('<a href="#' + accordianName + '"">' + routeDataTitle + '</a>');
		accordian.append('<div id="panel' + countOfAccordians +'" class="content">');
		//accordian.append('<div id="' + accordianName + '" class="content">');
		
	//var accordian = $("<dd>, { 'class': 'accordion-navigation'}");
	//	accordian.append('<a href="#' + accordianName + '>' + routeDataTitle + '</a>');
	//	accordian.append('<div id="' + accordianName + '" class="content">');
		
		//ToDo Need to add body of accordian
		$('#' + targetElement).append(accordian);
		$('#panel'+ countOfAccordians).append(routeDataTable);

    }

function getStations(location, distance, elementId)
	{
		countOfAccordians = 0;
		//Initial go and displaying results
		var htmlCode = '';

		$.ajax({
			type: "POST",
			url: "/newSearch",
			contentType: "application/json; charset=utf-8",
			dataType: 'json',
			data: {location: location, distance: distance},
			success: function(data) {

				//TODO Need to sort results ready to display


				//This works: $.each(data["results"][0], function (key ,value) {
					$.each(data['results'], function (key ,routeResults) {
						//document.write(routeResults['distance'])
						//What do we pass in above?
						//routeOptionOne =?
					//Send each routeOption after sorting to be displayed
						addAcordian(elementId, routeResults)
		    		})
		    },
  			error: function(e) {
				//called when there is an error
				//console.log(e.message);
			}	
		});	
	}

function TJLgetStations(location, distance, elementId)
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
		//displayStationAndRoutes(elementId)
	}





