
import apiKeys
import urllib.request
import json
from datetime import datetime, timedelta
try:
	from runtotrainapp import app
except ImportError:
	print ('Error importing runtotrainapp')

class TransportApi:
	def __init__(self, routeQuery):
		#Instance variable rather than Class variable
		self.routeQuery = routeQuery
		self.maxDistance = 0
		self.targetStations = []
		self.resultsString = []

	#def resultsPrintAndAppend(self, result):
		#TODO Replace with JSON builder of some sort
		#Print a string and also add it to the results list that will be returned to the web page.
	#	self.resultsString.append(result)
	#	print (result)

	def getTime(self, timeToModify, adjustment=0):
		'''Add minutes to the passed in time.'''

		adjustedTime = timeToModify + timedelta(minutes=adjustment)
		return adjustedTime

	def doStationLookup(self, stationURL):
		'''Lookup stations within X km of specified point and add to targetStations'''
		#TODO move URL bulding in here
		#TODO Fix bug below:
		print ('Do Station Lookup')
		if (app.config['READ_FROM_FILES'] == True):
			print ('JSON read from file1')
			try:
				with open(app.config['FILENAME']) as json_data:
					stationsJSON = json.load(json_data)
				json_data.close()
			except Exception as err:
				print ('Error opening: ' + app.config['FILENAME'] + str(err))
		else:
			try:
				stationResponse = urllib.request.urlopen(stationURL)
				stationsJSON = json.loads(stationResponse.readall().decode('utf-8'))
			
			except (URLError(err)):
				print ('Error connecting to: ' + stationURL)
				return ('Error getting station data')

			if app.config['WRITE_TO_FILE'] == True:
				with open(app.config['FILENAME'], 'w') as outfile:
					json.dump(stationsJSON, outfile, sort_keys = True, indent = 4, ensure_ascii=False)

		print ('Stations JSON')
		print (json.dumps(stationsJSON, indent = 4))

		if ('error' in stationsJSON):
		#TODO How do we display errors to the gui?			
			#self.resultsPrintAndAppend('Sorry, leaves on the line, please try later')
			#print (stationsJSON)
			print ('Error getting stations: ' + stationURL)
			stations = ''
			return False
		else:	
			stations = stationsJSON['stations']
		
		print ('Stations')
		print (json.dumps(stations, indent = 4))

		print ('Starting loop through stations to build station subset (targetStations)')
		#Loop through the stations and add to results list
		#TODO move to seperate function
		
		i = 0
		while (i < (len(stations)-1)):
			distance = int((stations[i]['distance']))/1000
			print ('Distance:' + str(distance))
			if distance > self.maxDistance:
				self.maxDistance = distance
				print ('maxDistance: ' + str(self.maxDistance))
			runTime = (self.routeQuery.getPace() * distance) + self.routeQuery.getDelayBeforeBoarding()
			i = i + 1	
			
			#Used to order stations by proximity to target run
			#May want to move this to the gui
			#Also may want to implement the weighting logic here.
			differenceFromTargetDistance = abs(distance - self.routeQuery.getDistance())
			self.targetStations.append({'differenceFromTargetDistance' : differenceFromTargetDistance, \
				'distance' : distance, \
				'runTime' : runTime, \
				'station_code' : stations[i]['station_code'], \
				'station_name' : stations[i]['name'], \
				'longitude' : stations[i]['longitude'], \
				'latitude' : stations[i]['latitude']})
		return True

	def getStations(self):
		''' Find all of the stations with in the specified distance of the start Long / Lat.
		Arguments:
		routeQuery - will include locations, distance etc.
		'''
		stationLookupURL='http://transportapi.com/v3/uk/train/stations/near.json?'
		maxDistance = 0
		resultPage=1
		
		#Long / Lat Boundaries for UK coordinates
		maxUKLatitude=58
		minUKLatitude=50
		maxUKLongitude=1.7
		minUKLongitude= -5.8
		latitude = self.routeQuery.getStartAddress().getLatitude()
		longitude = self.routeQuery.getStartAddress().getLongitude()

		#Validate search for stations is in the UK.	
		if ((latitude > maxUKLatitude) or (latitude < minUKLatitude)):
			raise ValueError ('Latitude out of bounds')
		
		if ((longitude > maxUKLongitude) or (longitude < minUKLongitude)):
			raise ValueError ('Longitude out of bounds')
					
		

		#TODO - SEPERATE OUT THE CALL TO Transport API,  then if in the results, the max distance is less than the target distance make another call recursively.		
		#		Use maxDistance and resultPage
		# 		resultPage is set to a hard limit of 5 in order to prevent excessive calls to the API.
		while ((self.maxDistance < self.routeQuery.distance) and (resultPage < 3)):
			print ('maxDistance: ' +  str(self.maxDistance) + 'routeQueryDistance: ' + str(self.routeQuery.distance) + ' Result page: ' + str(resultPage))

			stationLookupQuery='lon='+str(longitude)+'&lat='+str(latitude)+'&page=' + str(resultPage) + \
				'&api_key=' + apiKeys.getTransportApiKey()['key'] + '&app_id='+ apiKeys.getTransportApiKey()['app_id']
			
			stationUrl = stationLookupURL+stationLookupQuery
			print ('Station Lookup URL: ' + stationUrl)

			if (self.doStationLookup(stationUrl) == False):
				break
			resultPage += 1

		#Order by difference between target distance and actual distance, then just query top 3.
		self.targetStations.sort(key=lambda x: x["differenceFromTargetDistance"])
		print ('Sorted Stations:')
		print (json.dumps(self.targetStations, indent = 4))
		return self.targetStations

	def makeRoutingCall(self, routingURL, runTime):
		'''Query routing service for routes for the specified station and then add them to the results list'''
		#TODO Need to handle errors e.g. :{"error":"Not found"}
		try:
			routingResponse = urllib.request.urlopen(routingURL)
			routingResults = json.loads(routingResponse.readall().decode('utf-8'))
		except  URLError(err):
			print ('Error opening: ' + routingURL)
			return ('Error')

		processedRouteResults=[]

		#Process routing results adding required fields to the results List.
		if ('routes' in routingResults):
			routes = routingResults['routes']
			i = 0
			#Routes from a Station
			while i < len(routes)-1:
				#TODO Sort out run time
				totalDuration = '{:%H:%M}'.format(datetime.strptime(routes[i]['duration'], '%H:%M:%S') + ( timedelta(minutes=runTime)))
				j=0
				legs=[]
				#Legs of a Route
				while j < len(routes[i]['route_parts']):
					if routes[i]['route_parts'][j]['mode'] != 'foot':
						legs.append([[0, 'Journey Leg', str(j+1)], \
							[1, 'Mode', routes[i]['route_parts'][j]['mode']], \
							[2, 'Departure Station', routes[i]['route_parts'][j]['from_point_name']], \
							[3, 'Destination Station' , routes[i]['route_parts'][j]['to_point_name']], \
							[4, 'Train terminates' , routes[i]['route_parts'][j]['destination']], \
							[5, 'Departure Time' , routes[i]['route_parts'][j]['departure_time']], \
							[6, 'Arrival Time' , routes[i]['route_parts'][j]['arrival_time']], \
							[7, 'Train Duration' , routes[i]['route_parts'][j]['duration']]]  )
					j=j+1

				i=i+1
				processedRouteResults.append({'routeID' : i+1, 'totalDuration' : totalDuration, 'legs' : legs})
		else:
			print ('No results')
		#print ('Processed Route Results')
		#print (processedRouteResults)
			#A station may be in range but have no way of getting to the specified destination at the departure time specified.
		return processedRouteResults
		
	def routeFromStartStationToDestination(self,targetStations):
		'''This will calculate route from the start station to the end.  Start off using the transport API,
		alternatively could do this ourselves longer term.
		
		http://transportapi.com/v3/uk/public/journey/from/{from_type}:{from_text}/to/{to_type}:{to_text}[.format]
		'''
		stationRouteResults = []
		maximumApiCalls = app.config['MAX_API_CALLS']
		routingBaseURL='http://transportapi.com/v3/uk/public/journey/from/'
		self.targetStations = targetStations
		#TODO - Confirm whether we should use station name instead of the longlat of the station?
		destinationByLongLatOrName='LongLat'
		
		i = 0
		#Iterate through the stations
		while (i < (len(targetStations)-1)):
			#Add on run time to Query start time to get earliest train time
			adjustedTime = self.getTime(self.routeQuery.getStartDateTime(), self.targetStations[i]['runTime'])
			earliestTrainTime = '{:%Y-%m-%d/%H:%M}'.format(adjustedTime)

			if destinationByLongLatOrName=='Name':
				#TODO Refactor below two queries
				#Build Query URL
				routingParams = 'lonlat:' + str(self.targetStations[i]['longitude']) + ',' + str(self.targetStations[i]['latitude']) + '/to/lonlat:' + \
					str(self.routeQuery.getDestinationAddress().getLongitude())+ ',' + str(self.routeQuery.getDestinationAddress().getLatitude()) + \
					'/at/' + earliestTrainTime + '.json?modes=train-tube-dlr-overground&api_key=' + apiKeys.getTransportApiKey()['key'] + \
					'&app_id='+ apiKeys.getTransportApiKey()['app_id']
			else:
				routingParams = 'stop:' + urllib.parse.quote(self.targetStations[i]['station_name']) + '/to/lonlat:' + \
					str(self.routeQuery.getDestinationAddress().getLongitude())+','+ str(self.routeQuery.getDestinationAddress().getLatitude()) + \
					'/at/' + earliestTrainTime + '.json?modes=train-tube-dlr-overground&api_key=' + apiKeys.getTransportApiKey()['key'] + \
					'&app_id='+ apiKeys.getTransportApiKey()['app_id']

			routingURL = routingBaseURL + routingParams
			print ('RoutingURL: ' + routingURL)
			routeResults = self.makeRoutingCall(routingURL, targetStations[i]['runTime'])			

			if len(routeResults) >= 1:
				stationRouteResults.append({'station_name' : targetStations[i]['station_name'], \
					'distance' : targetStations[i]['distance'], \
					'runTime' : targetStations[i]['runTime'], \
					'routes' : routeResults })
			i = i + 1

			if (i >= maximumApiCalls):
				print ('break!')
				break
		return stationRouteResults			

if __name__ == '__main__':
	class app():
		config = {}
		def __init__(self):
			self.config={'READ_FROM_FILES' : True, 'FILENAME' : 'stations.txt'}

	app = app()	
	transportapi = TransportApi('')
	#transportapi.doStationLookup('http://transportapi.com/v3/uk/train/stations/near.json?lon=-0.2427249&lat=51.3481645&page=1&api_key=d9307fd91b0247c607e098d5effedc97&app_id=03bf8009')
	transportapi.makeRoutingCall('http://transportapi.com/v3/uk/public/journey/from/stop:Waddon/to/lonlat:-0.0235333,51.5054306/at/2014-12-02/14:21.json?modes=train-tube-dlr-overground&api_key=d9307fd91b0247c607e098d5effedc97&app_id=03bf8009', \
			15)

