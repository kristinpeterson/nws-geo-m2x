import os
import requests
import json

from db import DB
from m2x.client import M2XClient

google_geocode_base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
google_geocode_params = 'key=%s&latlng=' % (os.environ["GOOGLE_API_KEY"])

m2x_client = M2XClient(os.environ["M2X_API_KEY"])

def get_location(lat, lng):
    '''
    Return the county and state for the given lat/lng using
    Google Geocoder API
    '''
    url = google_geocode_base_url + google_geocode_params + str(lat) + "," + str(lng)
    response = json.loads(requests.get(url).text)
    county = None
    state = None

    try:
        for address_component in response['results'][0]['address_components']:
            for a_type in address_component['types']:
                if a_type == 'administrative_area_level_2':
                    county = address_component['long_name'].replace(' County', '')
                    county = county.encode('utf8')
                if a_type == 'administrative_area_level_1':
                    state = address_component['short_name']
                    state = state.encode('utf8')
        print "%s, %s found for lat: %s, lng: %s" % (county, state, lat, lng)
    except Exception as e:
        print "County not found for lat: %s, lng: %s" % (lat, lng)
        print e

    return { 'county': county, 'state': state }

def get_fips(county,state):
    '''
    Return the FIPS6 county code for the given county/state.
    '''
    fips = None
    try:
        db = DB()
        db.execute("SELECT fips FROM fips WHERE countyname = '%s' AND state = '%s';" % (county, state))
        fips = db.cur.fetchone()[0]
        db.commit()
        print "FIPS %s found for %s, %s" % (fips, county, state)
    except Exception as e:
        print "FIPS not found for %s, %s" % (county, state)
        print e
        db.rollback()
    return fips

def get_ugc(county, state):
    '''
    Return the UGC code(s) for the given county/state.

    For more info on UGC format, see: http://www.nws.noaa.gov/emwin/winugc.htm
    '''
    try:
        db = DB()
        db.execute("SELECT state,zone FROM ugc WHERE countyname = '%s' AND state = '%s';" % (county, state))
        ugc = []
        if db.cur is not None:
            for record in db.cur:
                code = record[0] + 'Z' + record[1]
                ugc.append(code)
        db.commit()
    except Exception as e:
        print e
        db.rollback()

    if len(ugc) > 0:
        print "UGC(s) found for %s, %s:" % (county, state)
        ugc = ','.join(ugc)
    else:
        print "UGC(s) not found for %s, %s" % (county, state)
        ugc = None

    return ugc

def update_device(device_id, fips, ugc):
    '''
    Update device metadata if fips,ugc
    '''
    device = m2x_client.device(device_id)
    if fips is None:
        device.update_metadata_field(field='fips6', value='')
    else:
        device.update_metadata_field(field='fips6', value=fips)

    if ugc is None:
        device.update_metadata_field(field='ugc', value='')
    else:
        device.update_metadata_field(field='ugc', value=ugc)
