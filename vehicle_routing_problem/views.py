from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
import json
import urllib

access_token="pk.eyJ1IjoiY2Ftc2tpdGhlZGV2IiwiYSI6ImNra3NxMnN1MzBqcGIycG9peHZleHQ0bG4ifQ.wR-JCGHhBO3xQiHqAiAKUg"
base_uri="https://api.mapbox.com"

def address_to_location(address):
    url_address = urllib.parse.quote_plus(str(address))
    r = requests.get(f"{base_uri}/geocoding/v5/mapbox.places/{url_address}.json?access_token={access_token}")
    json_data = r.json()
    return ",".join(map(str, json_data['features'][0]['center']))

# Create your views here.
def index(request):
    if request.method != 'POST':
        return JsonResponse(None, safe=False)

    body = json.loads(request.body)

    if not 'locations' in body:
        return JsonResponse({"error": "locations must be present"})

    if len(body['locations']) <= 0:
        return JsonResponse({"error": "locations must be and array/list and not empty"})

    coordinate_str = ";".join(list(map(address_to_location, body['locations'])))

    r = requests.get(f"{base_uri}/optimized-trips/v1/mapbox/driving/{coordinate_str}?access_token={access_token}")
    json_data = r.json()

    # json_data['waypoints'] = sorted(json_data['waypoints'], key=lambda i: (i['waypoint_index']))
    return JsonResponse(json_data, safe=False)
