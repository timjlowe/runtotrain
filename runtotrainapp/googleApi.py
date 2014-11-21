import urllib.parse
import urllib.request
import httplib2
import json
import apiKeys


def geoCodeLocation(location):
	geocodeURL='https://maps.googleapis.com/maps/api/geocode/json?'
	
	#lookupURL = geocodeURL + urllib.parse.urlencode({'address' : location.getAddress(), \
	#		'key' : apiKeys.getGoogleApiKey()})
	
	lookupURL = geocodeURL + urllib.parse.urlencode({'address' : location.getAddress()})
	print(lookupURL)
	googleResponse = urllib.request.urlopen(lookupURL)

	#TODO: Check the response header in order to select the correct encoding format rather than assuming utf-8
	decodedResponse = json.loads(googleResponse.readall().decode('utf-8'))
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

		
