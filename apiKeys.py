#If False, will use any public keys that are available.
useTimsApiKeys = False

def getTransportApiKey():
	''' Return TransportApiKeys '''
	if (useTimsApiKeys == True):
		api_key = {'app_id' : 'bdd013aa', 'key' : 'd3c6ec9a4b3b831510289fe15d36abf4'}
	else:
		api_key = {'app_id' : '03bf8009', 'key' : 'd9307fd91b0247c607e098d5effedc97'}
	
	return api_key
	
def getGoogleApiKey():
	''' Return Google API Keys '''
	if (useTimsApiKeys == True):
		api_key = ''
	else:
		api_key = ''
	
	return api_key