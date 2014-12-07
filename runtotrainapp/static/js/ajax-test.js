
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
    var routeDataTitle = '<b>' + routeData['station_name'] + '</b> station, ' + (routeData['distance']).toFixed(1) + 'km away. Running time: ' + (routeData['runTime']).toFixed(0) + 'mins' +
    	'; Earliest Arrival: <b>' + routeData['earliestHomeArrival'] + '</b>';
	var routeDataTable = $('<table>');
	//var	routeDataTableHeader = '<th>Leg</th><th>Start Station</th><th>Time</th>';
	var	routeDataTableHeader =  '<tr>';
	var tableCols = routeData['routes'][0]['legs'][0].length
	
	$.each(routeData['routes'][0]['legs'][0], function(key, value) {

	//Need to correctly handle the array here.	
    	routeDataTableHeader = routeDataTableHeader + '<th>' + value[1] + '</th>';
		});
	routeDataTableHeader +- '</tr>';
	routeDataTable.append(routeDataTableHeader);

	//Add the data rows to the table showing the route steps.
	$.each(routeData['routes'], function (i,valueRoute) {
		$.each(valueRoute['legs'], function (i,valueRow) {
			var routeDataTableRow = '<tr>';
			$.each( valueRow, function (key, value){
    			routeDataTableRow = routeDataTableRow + '<td>' + value[2] + '</td>';
    		});
    		routeDataTableRow += '</tr>';
			routeDataTable.append(routeDataTableRow);
		});
		var summaryRow = '<tr><td colspan="' + tableCols + '"><b>Arrival Time: ' + valueRoute['arrivalTime'] +
			' Total Travel Time (inc Run): ' + valueRoute['totalDuration'] + '</b></td></tr>'
		routeDataTable.append(summaryRow)

	});
	
	console.log(routeDataTable);
	//Build the accordian
	var accordian = $("<dd>, { 'class': 'accordion-navigation'}");
		accordian.append('<a href="#panel'+ accordianNumber +'">' + routeDataTitle + '</a>');
		accordian.append('<div id="panel' + accordianNumber +'" class="content">');
	
		$('#' + targetElement).append(accordian);
		//Add the data to the accordian - couldn't get this to work if done before adding accordian to the page.
		$('#panel'+ accordianNumber).append(routeDataTable);
    }

function getStations(startAddress, destinationAddress, pace, runDistance, startDateTime, elementId, progressElementId, buttonId)
	{
	//RouteQuery(startAddress=request.form['startAddress'],destinationAddress=request.form['destinationAddress'], \
	//pace=request.form['pace'],	distance=request.form['runDistance'], startDateTime=request.form['startDateTime'])

		//countOfAccordians = 0;
		//Initial go and displaying results
		console.log(startAddress)
		console.log(destinationAddress)
		console.log(pace)
		console.log(runDistance)
		console.log(startDateTime)
		console.log(elementId)
		var htmlCode = '';
		$('#' + elementId).empty();

		$('#' + buttonId).class = "button disabled";
		showElement(progressElementId);
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
		    	hideElement(progressElementId);

		    },
  			error: function(jqXHR,  textStatus, errorThrown ) {

				//called when there is an error
				hideElement(progressElementId);
				console.log(jqXHR);
				console.log(textStatus);
				//console.log(errorThrown);
			}	
		});	
	}
function hideElement(elementToHide)
	{
		console.log('Hide' + elementToHide)
		$("#"+elementToHide).hide();
	}

function showElement(elementToShow)
	{
		console.log('Show' + elementToShow)
		$("#"+elementToShow).show();
	}	





