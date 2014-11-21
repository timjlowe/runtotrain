
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

function addAcordian(targetElement, accordianNumber, routeData)
	{
    //First parameter is where to put the accordian on the page, the second is the table data to show in the accordian.

	//Title displayed on the rolled up accordian
    var routeDataTitle = 'Run to: ' + routeData['station_name'] + ' station, ' + routeData['distance'] + 'km away. Running time: ' + routeData['runTime'];
	var routeDataTable = $("<table>")
	var	routeDataTableHeader = '<th>Leg</th><th>Start Station</th><th>Time</th>';

	routeDataTable.append(row = $(routeDataTableHeader));

	//Add the data rows to the table showing the route steps.
	$.each(routeData['routes'][0]['legs'], function (i,value) {
		var routeDataTableRow = '<tr><td>' +
			value['legId'] + '</td>' + '<td>' +
			value['Departure Station'] + '</td>' + '<td>' +
			value['Train Duration']
			+ '</td></tr>';

		routeDataTable.append(routeDataTableRow);

		})

	//Build the accordian
	var accordian = $("<dd>, { 'class': 'accordion-navigation'}");
		accordian.append('<a href="#panel'+ accordianNumber +'">' + routeDataTitle + '</a>');
		accordian.append('<div id="panel' + accordianNumber +'" class="content">');
	
		$('#' + targetElement).append(accordian);
		//Add the data to the accordian - couldn't get this to work if done before adding accordian to the page.
		$('#panel'+ accordianNumber).append(routeDataTable);
    }

function getStations(startAddress, destinationAddress, pace, runDistance, startDateTime, elementId)
	{
	//RouteQuery(startAddress=request.form['startAddress'],destinationAddress=request.form['destinationAddress'], \
	//pace=request.form['pace'],	distance=request.form['runDistance'], startDateTime=request.form['startDateTime'])

		countOfAccordians = 0;
		//Initial go and displaying results
		var htmlCode = '';

		$.ajax({
			type: 'POST',
			url: '/newSearch',
			contentType: "application/json; charset=utf-8",
			dataType: 'json',
			data: JSON.stringify({startAddress: startAddress,
				destinationAddress: destinationAddress,
				pace: pace,
				runDistance: runDistance,
				startDateTime: startDateTime}),
			success: function(data) {

				//TODO Need to sort results ready to display
				countOfAccordians = 0

				//This works: $.each(data["results"][0], function (key ,value) {
					$.each(data, function (key ,routeResults) {
						
					//Send each routeOption after sorting to be displayed
						addAcordian(elementId, countOfAccordians, routeResults)
						countOfAccordians = countOfAccordians +1
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





