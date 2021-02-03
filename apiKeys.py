#If False, will use any public keys that are available.
useTimsApiKeys = False

def getTransportApiKey():
        ''' Return TransportApiKeys '''
        if (useTimsApiKeys == True):
                api_key = {'app_id' : '', 'key' : ''}
        else:
                api_key = {'app_id' : '', 'key' : ''}

        return api_key

def getGoogleApiKey():
        ''' Return Google API Keys '''
        if (useTimsApiKeys == True):
                api_key = ''
        else:
                api_key = ''

        return api_key
