import sys
sys.path.insert(0, '..')
sys.path.insert(0, '../../libraries')
import urllib.parse
import urllib.request
import httplib2
import json
import os
from runtotrainapp import app
from runtotrainapp import apiKeys

def geoCodeLocation(location):
	geocodeURL='https://maps.googleapis.com/maps/api/geocode/json?'
	
	#lookupURL = geocodeURL + urllib.parse.urlencode({'address' : location.getAddress(), \
	#		'key' : apiKeys.getGoogleApiKey()})
	
	lookupURL = geocodeURL + urllib.parse.urlencode({'address' : location.getAddress()})
	print(lookupURL)
	try:
		googleResponse = urllib.request.urlopen(lookupURL)
		decodedResponse = json.loads(googleResponse.readall().decode('utf-8'))
		if app.config['WRITE_TO_FILE'] == True:
			os.chdir(app.config['OUTPUT_DIRECTORY'])
			with open('googleapi.txt', 'w') as outfile:
				json.dump(decodedResponse, outfile, sort_keys = True, indent = 4, ensure_ascii=False)

	except urllib.error.URLError as e:
		print ('Error connecting to: ' + lookupURL + ' Exception: ' + e.reason)
		return ('Error')

	print ('Google Response')
	print (json.dumps(decodedResponse, indent = 4))

	#TODO: Check the response header in order to select the correct encoding format rather than assuming utf-8
	
	if (len(decodedResponse['results']) > 1):
		#TODO In this instance we should display a modal picker
		#Then update the long / lat AND the selected address
		print ("Ambiguous results: " + decodedResponse['results'])
	else:
		longLat = (decodedResponse['results'])[0]['geometry']['location']
		location.setLatitude(longLat['lat'])
		location.setLongitude(longLat['lng'])
		print (longLat['lat'])
		print (longLat['lng'])
	
if __name__ == '__main__':
	from location import Location
	import routequery
	location = Location('Canary Wharf')
