from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from advertisement.models import Advertisement, Data, Status, Position
import json


DATA = {
    "buy": "true",
    "city": "44097",
    "data": {
        "bedroomsQuantity": 2,
        "city": "Mesquer",
        "floorQuantity": 1,
        "hasAirConditioning": "false",
        "hasAlarm": "false",
        "hasCellar": "false",
        "hasDoorCode": "false",
        "hasFirePlace": "false",
        "hasGarden": "true",
        "hasIntercom": "false",
        "hasPool": "false",
        "hasTerrace": "false",
        "heating": "radiateur \u00e9lectrique ",
        "link": "https://www.bienici.com/annonce/vente/mesquer/maison/3pieces/iad-france-1095069",
        "newProperty": "false",
        "publicationDate": "2022-08-04T15:09:07.742Z",
        "reference": "1072297",
        "status": {
            "autoImported": "true",
            "closedByUser": "false",
            "highlighted": "false",
            "is3dHighlighted": "false",
            "isLeading": "false",
            "onTheMarket": "true",
        },
        "title": "Vente Maison/villa 3 pi\u00e8ces",
        "transactionType": "buy",
        "yearOfConstruction": 1998,
    },
    "first_date": "2022-08-08",
    "good_id": "iad-france-1095069",
    "house": "true",
    "id": 1289498,
    "iris": "440970000",
    "last_date": "2022-09-30",
    "meter_square": 4629,
    "position": {"lat": 47.40422756768584, "lng": -2.455508739167056},
    "price": 416666,
    "rooms": 3,
    "surface": 90,
}


class AdvertisementListPostTest(APITestCase):
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

    def test_create_advertisement(self):
        """
        Ensure we can create a new advertisement object.
        """
        url = reverse("list-post-ads")
        response = self.client.post(url, DATA, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Advertisement.objects.count(), 4)
        self.assertEqual(Data.objects.count(), 4)
        self.assertEqual(Status.objects.count(), 4)
        self.assertEqual(Position.objects.count(), 4)
        self.assertEqual(
            Advertisement.objects.get(good_id="iad-france-1095069").price, 416666
        )
        self.assertEqual(
            Advertisement.objects.get(good_id="iad-france-1095069").data.city, "Mesquer"
        )
        self.assertTrue(
            Advertisement.objects.get(
                good_id="iad-france-1095069"
            ).data.status.onTheMarket
        )
        self.assertEqual(
            Advertisement.objects.get(good_id="iad-france-1095069").position.lat,
            47.40422756768584,
        )

    def test_get(self):
        """
        Ensure we can get a all advertisements.
        """
        url = reverse("list-post-ads")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
