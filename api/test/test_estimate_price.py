from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from advertisement.models import Advertisement, Data, Status, Position
from api.serializers import AdvertisementSerializer
import json


class AdvertisementEstimatePriceTest(APITestCase):
    def setUp(self):
        f = open("test_data.json")
        rawdata = json.load(f)
        f.close()

        for ads_data in rawdata:
            data_data = ads_data.pop("data")
            status_data = data_data.pop("status")
            position_data = ads_data.pop("position")
            status = Status.objects.create(**status_data)
            data = Data.objects.create(status=status, **data_data)
            if position_data:
                longitude = position_data.pop("lng")
                latitude = position_data.pop("lat")
                location_data = {
                    "location": "POINT(" + str(longitude) + " " + str(latitude) + ")"
                }
                position = Position.objects.create(**location_data)
            advertisement = Advertisement.objects.create(
                data=data, position=position, **ads_data
            )

    def test_get_geo_prices(self):
        """
        Ensure we can estimate price of a house or appartement.
        """
        data_kwargs = {
            "house": 0,
            "rooms": 2,
            "surface": 27,
            "lat": 47.2743522,
            "lng": -2.3419564,
        }
        url = reverse("estimate-price", kwargs=data_kwargs)
        response = self.client.get(url, format=None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_result = {
            "min_price": 140805.0,
            "avg_price": 174285.0,
            "max_price": 207765.0,
        }
        self.assertEqual(response.data, expected_result)
