import sys
sys.path.insert(0, '../libraries')
from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from datetime import datetime, timedelta
import apiKeys
import googleApi
import transportapi
import json


class Location:
	'''A location object, used to set the longitude and latitude passed into the routing queries'''
	
	def __init__(self, address):
		self.setAddress(address)
	
	def setAddress(self, address):
		self.address=address
		#validate
		googleApi.geoCodeLocation(self)
		
	def getAddress(self):
		return self.address	
		
	def setLongitude(self, longitude):
		self.longitude = longitude	

	def getLongitude(self):
		return self.longitude
		
	def setLatitude(self, latitude):
		self.latitude = latitude	

	def getLatitude(self):
		return self.latitude
		
class RouteQuery:
	'''Sets up the query parameters.  This will be replaced by the front end'''
	
	def __init__(self, startAddress, destinationAddress, distance, pace, startDateTime, \
			distanceInKm=True, runFirst=True, delayBeforeBoarding=10):
		self.startAddress = Location(startAddress)
		self.destinationAddress = Location(destinationAddress)
		self.distance = int(distance)
		self.pace = float(pace)
		self.startDateTime = datetime.strptime(startDateTime, '%Y-%m-%d %H:%M:%S')
		self.distanceInKM = distanceInKm
		self.runFirst = runFirst
		self.delayBeforeBoarding = delayBeforeBoarding
		
	def setDistance(self, distance):
		self.distance = int(distance)
	
	def setPace(self, pace):
		self.pace = int(pace)
		
	def setStartAddress(self, address):
		self.startAddress.setAddress(address)
		
	def setDestinationAddress(self, address):
		self.destinationAddress.setAddress(address)
	
	def setDelayBeforeBoarding(self, delayBeforeBoarding):
		self.delayBeforeBoarding = delayBeforeBoarding

	def setStartDateTime(self, startDateTime):
		self.startDateTime = startDateTime

	def getDistance(self):
		return self.distance
	
	def getPace(self):
		return self.pace
		
	def getStartAddress(self):
		return self.startAddress
		
	def getDestinationAddress(self):
		return self.destinationAddress	

	def getDelayBeforeBoarding(self):
		return self.delayBeforeBoarding	

	def getStartDateTime(self):
		return self.startDateTime

app = Flask(__name__)
@app.route('/')
def start():
		
	return render_template('index-ajax.html')

@app.route('/TJLnewSearch', methods=['POST'])
def TJLnewSearch():
	print (request.form)

	routeQuery = RouteQuery(startAddress=request.form['startAddress'],destinationAddress=request.form['destinationAddress'], \
			pace=request.form['pace'],	distance=request.form['runDistance'], startDateTime=request.form['startDateTime'])

	#Setup the Search
	transportApi = transportapi.TransportApi(routeQuery)
	#Get the stations inline with target run distance
	stations = transportApi.getStations()
	#Get the routes
	transportApi.routeFromStartStationToDestination()

	return 'Hello query values: '

#TJL Test Ajax
@app.route('/newSearch', methods=['POST'])
def newSearch():

	#print (str(json.loads(request.form)))
	#Sample data
	stationResults = [ {'station' : 'New Malden', 'distance' : 5.1, 'longitude' : 42312, 'latitude' : 12312,\
	'routes' : [  \
	{ "route_id" : 1, \
	'legs' : [ \
	{'leg' : 1, 'type' : 'train', 'start_station' : 'Ewell West', 'time' : '20:32'}, \
	{'leg' : 2, 'type' : 'train', 'start_station' : 'Waterloo', 'time' : '21:09'} ] } ] }, \
	{'station' : 'Worcester Park', 'distance' : 4.2, 'longitude' : 32412, 'latitude' : 87312, \
	'routes' : [ \
	{ "route_id" : 1, \
	'legs' : [ \
	{'leg' : 1, 'type' : 'train', 'start_station' : 'Ewell East', 'time' : '20:45'}, \
	{'leg' : 2, 'type' : 'train', 'start_station' : 'Victoria', 'time' : '21:04'} ] }, \
	{ "route_id" : 2, \
	'legs' : [ \
	{'leg' : 1, 'type' : 'train', 'start_station' : 'New Malden', 'time' : '20:55'}, \
	{'leg' : 2, 'type' : 'train', 'start_station' : 'Victoria', 'time' : '21:04'} ] } ] } ]
						
	stationResultsJson = (json.dumps(stationResults))
	#print(stationResultsJson)
	return stationResultsJson

	#routeResults = [ {'mode' : 'Train', 'departureTime' : '21:04', 'arrivalTime' : '21:06'} ]






if __name__ == '__main__':
    app.run(debug=True)