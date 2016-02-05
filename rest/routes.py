import requests
import json

from nws_geo_m2x.utils import get_location
from nws_geo_m2x.utils import get_fips
from nws_geo_m2x.utils import get_ugc
from nws_geo_m2x.utils import update_device
from m2x.client import M2XClient
from xml.etree import ElementTree
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update(request):
    if request.method == "POST":
        # request.body contains the lat/long, which was sent 
        # using the IFTTT M2X -> Maker HTTP request recipe
        # Format:
        # { "lat": -12.34567, "lng": 67.89000, "device_id": "{device_id}" }
        response = json.loads(request.body)
        location = get_location(response['lat'], response['lng'])
        fips = get_fips(location['county'], location['state'])
        ugc = get_ugc(location['county'], location['state'])
        update_device(response['device_id'], fips, ugc)
            
    return HttpResponse("OK")
