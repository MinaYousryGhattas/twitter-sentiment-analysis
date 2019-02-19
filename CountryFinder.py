import geocoder
import string
# -*- coding: utf-8 -*-

# checking if the 'S' contain not english charectar
def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def get_Address(address):
    g1 = None
    # remove any punctuation from address string

    address = address.translate(str.maketrans('','',string.punctuation))
    if (address == ''):
        return None
    try:
        # get country from the full string by requesting arcgis api
        g1 = geocoder.arcgis(address, method='reverse')
        if (g1 == None or g1.country == ''):
            '''
            # if not found from all string we start by splitting address to keywords
            and the check each keyword
            '''
            for add in address.split(' '):
                g1 = geocoder.arcgis(add, method='reverse')
                if (g1 != None and g1.country != ''):
                    break

    finally:
        if (g1 == None or g1.country == ''):
            return None
        return g1.country
