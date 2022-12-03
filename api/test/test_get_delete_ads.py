from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from advertisement.models import Advertisement, Data, Status, Position
from api.serializers import AdvertisementSerializer
import json


class AdvertisementGetDeleteTest(APITestCase):
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

    def test_get(self):
        """
        Ensure we can get an advertisement by id.
        """
        example_ad = Advertisement.objects.all()
        url = reverse("get-delete-ads", kwargs={"pk": example_ad[0].id})
        response = self.client.get(url, format=None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data, AdvertisementSerializer(example_ad[0]).data)

    def test_delete(self):
        """
        Ensure we can delete an advertisement by id.
        """
        example_ad = Advertisement.objects.all()
        url = reverse("get-delete-ads", kwargs={"pk": example_ad[0].id})
        response = self.client.delete(url, pk=2, format=None)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
