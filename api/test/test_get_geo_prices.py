from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from advertisement.models import Advertisement, Data, Status, Position
from api.serializers import AdvertisementSerializer
import json


class AdvertisementGetGeoPricesTest(APITestCase):
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
        Ensure we can get prices by lat, long and within a redius.
        """
        lat = Advertisement.objects.all()[0].position.lat
        lng = Advertisement.objects.all()[0].position.lng
        url = reverse("get-geo-prices", kwargs={"lat": lat, "lng": lng, "radius": 700})
        response = self.client.get(url, format=None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_result = {"T1": None, "T2": 5215.0, "T3": None, "T4P": 5421.0}
        self.assertEqual(response.data, expected_result)
