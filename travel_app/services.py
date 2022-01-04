import json

import requests
from django.core.exceptions import MultipleObjectsReturned

from travel_app.models import Region, Location


class Parser:

    @staticmethod
    def start_parsing():
        response = requests.get("https://find-way.com.ua/media/com_jamegafilter/uk_ua/1.json")
        places_json = json.loads(response.content)
        for place_item in places_json:
            place = places_json.get(place_item)
            print(place.get("attr").get("name").get('frontend_value'))
            print(place.get("attr").get("cat").get('frontend_value')[-1])
            try:
                region, _ = Region.objects.get_or_create(name=place.get("attr").get("cat").get('frontend_value')[-1])
            except MultipleObjectsReturned:
                region = Region.objects.filter(name=place.get("attr").get("cat").get('frontend_value')[-1]).first()
            Location.objects.get_or_create(
                name=place.get("attr").get("name").get('frontend_value'),
                region=region,
            )
