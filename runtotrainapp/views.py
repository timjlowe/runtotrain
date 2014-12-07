import sys
sys.path.insert(0, '../libraries')
from flask import Flask
from flask import request
from flask import render_template
from flask import url_for
from datetime import datetime, timedelta
from runtotrainapp import app
from runtotrainapp import apiKeys
from runtotrainapp import googleapi
from runtotrainapp import transportapi
from runtotrainapp import routequery
import json


#import location

#MAIN
#app = Flask(__name__, instance_relative_config=True)
#app.config.from_pyfile('config.py')

@app.route('/')
@app.route('/index')
def index():
	return render_template('index-ajax.html')

@app.route('/newSearch', methods=['POST'])
def newSearch():
	
#try:
	jsonForm = request.get_json()
	print (json.dumps(jsonForm, indent=4, sort_keys=True))
	routeQuery = routequery.RouteQuery(startAddress=jsonForm['startAddress'],destinationAddress=jsonForm['destinationAddress'], \
	distance=jsonForm['runDistance'], pace=jsonForm['pace'],	 \
	startDateTime=jsonForm['startDateTime'])

	transportApi = transportapi.TransportApi(routeQuery)
	#Get the stations inline with target run distance
	stations = transportApi.getStations()
	#TODO - Setup accordian headers
	#Should then call for results and populate accordian one at a time.
	#Then get the routes from those Stations
	results = (transportApi.routeFromStartStationToDestination(stations))
	print (results)
	finalResults = (json.dumps(results, indent=4, sort_keys=True))
	print (finalResults)
	return finalResults

#except (ValueError, KeyError, TypeError) as e:
#	print ('Error  %s' % e)
	#	return ('Error')

#TJL Test Ajax
@app.route('/TJLnewSearch', methods=['POST'])
def TJLnewSearch():

	#print (str(json.loads(request.form)))
	#Sample data
	stationResults =  {'results' : [ \
	{ 'route_id' : 1, 'station' : 'New Malden', 'distance' : 5.1, \
	'legs' : [ \
	{'leg' : 1, 'type' : 'train', 'start_station' : 'Ewell West', 'time' : '20:32'}, \
	{'leg' : 2, 'type' : 'train', 'start_station' : 'Waterloo', 'time' : '21:09'} ] }, \
	{ "route_id" : 2, 'station' : 'Ewell East', 'distance' : 6.1, \
	'legs' : [ \
	{'leg' : 1, 'type' : 'train', 'start_station' : 'Ewell East', 'time' : '20:45'}, \
	{'leg' : 2, 'type' : 'train', 'start_station' : 'Victoria', 'time' : '21:04'} ] }, \
	{ "route_id" : 3, 'station' : 'New Malden', 'distance' : 5.1,\
	'legs' : [ \
	{'leg' : 1, 'type' : 'train', 'start_station' : 'New Malden', 'time' : '20:55'}, \
	{'leg' : 2, 'type' : 'train', 'start_station' : 'Victoria', 'time' : '21:04'} ] } ] }
	
	#stationResults = {'results' : 'test'}

	stationResultsJson = (json.dumps(stationResults, indent=4, sort_keys=True))
	#print (stationResultsJson)
	print (request.data)

	return stationResultsJson


#if __name__ == '__main__':
#	app.debug = True
#	app.run(host='0.0.0.0')



