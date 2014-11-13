
import apiKeys
import urllib.request
import json
from datetime import datetime, timedelta 

class TransportApi:
	def __init__(self, routeQuery):
		#Instance variable rather than Class variable
		self.routeQuery = routeQuery
		self.maxDistance = 0
		self.targetStations = []
		self.resultsString = []

	def resultsPrintAndAppend(self, result):
		#TODO Replace with JSON builder of some sort
		#Print a string and also add it to the results list that will be returned to the web page.
		self.resultsString.append(result)
		print (result)

	def getTime(self, timeToModify, adjustment=0):
		#Add minutes to the current time
		print ("==========================Time:")
		print (type(timeToModify))
		print (timeToModify)

		adjustedTime = timeToModify + timedelta(minutes=adjustment)
		return adjustedTime

	def getMoreStations(self, stationURL):
		stationResponse = urllib.request.urlopen(stationURL)	
		stationsJSON = json.loads(stationResponse.readall().decode('utf-8'))

		if ('error' in stationsJSON):
		#TODO How do we display errors to the gui?			
			self.resultsPrintAndAppend('Sorry, leaves on the line, please try later')
			print (stationsJSON)
			print (stationURL)
			stations = ''
			return False
		else:	
			stations = stationsJSON['stations']
		
		#TODO Review below code.
			
		#Loop through the stations.
		i = 0
		while i < (len(stations)-1):
			distance = int((stations[i]['distance']))/1000
			if distance > self.maxDistance:
				self.maxDistance = distance
			runTime = (self.routeQuery.getPace() * distance) + self.routeQuery.getDelayBeforeBoarding()
			i = i + 1	
			
			#Used to order stations by proximity to target run
			differenceFromTargetDistance = abs(distance - self.routeQuery.getDistance())
			self.targetStations.append([differenceFromTargetDistance,distance,runTime,stations[i]['station_code'],stations[i]['name'],stations[i]['longitude'],stations[i]['latitude']])

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
					
		stationLookupQuery='lon='+str(longitude)+'&lat='+str(latitude)+'&page=' + str(resultPage) + \
				'&api_key=' + apiKeys.getTransportApiKey()['key'] + '&app_id='+ apiKeys.getTransportApiKey()['app_id']
		stationUrl = stationLookupURL+stationLookupQuery
		
		#TODO - SEPERATE OUT THE CALL TO Transport API,  then if in the results, the max distance is less than the target distance make another call recursively.		
		#		Use maxDistance and resultPage
		# 		resultPage is set to a hard limit of 5 in order to prevent excessive calls to the API.
		while ((self.maxDistance < self.routeQuery.distance) and (resultPage < 5)):
			if (self.getMoreStations(stationUrl) == False):
				break
			resultPage += 1

		#Order by difference between target distance and actual distance, then just query top 3.
		targetStations = sorted(self.targetStations, key=lambda station: station[0])
		#print (self.targetStations)
		return self.targetStations
		
	def routeFromStartStationToDestination(self):
		'''This will calculate route from the start station to the end.  Start off using the transport API,
		alternatively could do this ourselves longer term.
		
		http://transportapi.com/v3/uk/public/journey/from/{from_type}:{from_text}/to/{to_type}:{to_text}[.format]
		'''
		
		if (apiKeys.useTimsApiKeys == True):
			maximumApiCalls = 1
		else:
			maximumApiCalls = 5
		
		routingBaseURL='http://transportapi.com/v3/uk/public/journey/from/'
		
		#TODO - Confirm whether we should use station name instead of the longlat of the station?
		destinationByLongLatOrName='LongLat'
		
		i = 0
		#print ('Number of stations: ', str(len(self.targetStations)))
		while i < ((len(self.targetStations)-1)):
			#Add on run time to Query start time to get earliest train time
			print ("QueryTime Type: " + str(type(self.routeQuery.getStartDateTime())))
			adjustedTime = self.getTime(self.routeQuery.getStartDateTime(), self.targetStations[i][2])
			earliestTrainTime = '{:%Y-%m-%d/%H:%M}'.format(adjustedTime)

			#earliestTrainTime = '{:%Y-%m-%d/%H:%M}'.format(self.getTime(self.routeQuery.getStartDateTime(), self.targetStations[i][2]))
			
			if destinationByLongLatOrName=='Name':
				#Build Query URL
				routingParams = 'lonlat:' + str(self.targetStations[i][5]) + ',' + str(self.targetStations[i][6]) + '/to/lonlat:' + \
					str(self.routeQuery.getDestinationAddress().getLongitude())+','+ str(self.routeQuery.getDestinationAddress().getLatitude()) + \
					'/at/' + earliestTrainTime + '.json?modes=train-tube-dlr-overground&api_key=' + apiKeys.getTransportApiKey()['key'] + \
					'&app_id='+ apiKeys.getTransportApiKey()['app_id']
			else:
				routingParams = 'stop:' + urllib.parse.quote(self.targetStations[i][4]) + '/to/lonlat:' + \
					str(self.routeQuery.getDestinationAddress().getLongitude())+','+ str(self.routeQuery.getDestinationAddress().getLatitude()) + \
					'/at/' + earliestTrainTime + '.json?modes=train-tube-dlr-overground&api_key=' + apiKeys.getTransportApiKey()['key'] + \
					'&app_id='+ apiKeys.getTransportApiKey()['app_id']
			
			routingURL = routingBaseURL + routingParams
			runTime = self.targetStations[i][2]
			#print (routingURL)
			self.resultsPrintAndAppend('')
			self.resultsPrintAndAppend('------------------ Station Option ' + str(i+1) + ' ------------------')
			self.resultsPrintAndAppend('Run to Station: ' + self.targetStations[i][4])
			self.resultsPrintAndAppend('Distance to Station: ' + str(self.targetStations[i][1]) + 'km')
			#self.resultsPrintAndAppend('Arrival Time: '+ '{:%H:%M}'.format(self.getTime(self.targetStations[i][2])))
			
			#self.displayResults(routingURL,runTime=runTime)
			i = i + 1
			if i >= maximumApiCalls:
				break
		return self.resultsString			
