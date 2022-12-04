from advertisement.models import Advertisement
from .serializers import AdvertisementSerializer
from rest_framework import mixins
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance as DistanceM
from django.contrib.gis.db.models.functions import Distance as Distance2P
from django.db.models import Avg, Min, Max


class AdvertisementList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    """
    get:
    List all advertisements.

    post:
    Creat an advertisement instance.
    """

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class AdvertisementDetail(
    mixins.RetrieveModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView
):
    """
    get:
    Get an advertisement by id.

    delete:
    Delete an advertisement by id.
    """

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class AdvertisementCity(APIView):
    """
    get:
    Get advertisements by city code (ex. "44097").
    """

    def get(self, request, city):
        advertisements = Advertisement.objects.filter(city=city)
        serializer = AdvertisementSerializer(advertisements, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdvertisementGeoPrice(APIView):
    """
    get:
    Retrieve average meter square prices by position and radius (ex. "/ads/geoprice/47.277050/-2.337642/700").
    """

    def get(self, request, lat, lng, radius):

        point = Point(float(lng), float(lat))
        # filter all locations that have a distance less or equal to the given radius from the given point
        advertisements = Advertisement.objects.filter(
            position__location__distance_lte=(point, DistanceM(m=float(radius))),
        )
        result = {}
        result["T1"] = advertisements.filter(rooms=1).aggregate(Avg("meter_square"))[
            "meter_square__avg"
        ]
        result["T2"] = advertisements.filter(rooms=2).aggregate(Avg("meter_square"))[
            "meter_square__avg"
        ]
        result["T3"] = advertisements.filter(rooms=3).aggregate(Avg("meter_square"))[
            "meter_square__avg"
        ]
        result["T4P"] = advertisements.filter(rooms__gte=4).aggregate(
            Avg("meter_square")
        )["meter_square__avg"]
        return Response(result, status=status.HTTP_200_OK)


class AdvertisementPriceEstimator(APIView):
    """
    get:
    Get price estimations using housing type (boolean 0(appartment) or 1(house)), rooms (integer),
    surface (integer) and location (lat and long).
    The prices are obtained by multipliying the surface by the meter square price.
    The meter square price is estimated in terms of min, avg and max of the top 5 closest
    ads with the same housing type and the same number of rooms
    (ex. "/ads/estimateprice/0/2/27/47.2743522/-2.3419564/")
    """

    def get(self, request, house, rooms, surface, lat, lng):
        point = Point(float(lng), float(lat), srid=4326)
        # filter the top 5 closest ads with the given housing type and rooms' number
        advertisements = (
            Advertisement.objects.filter(
                house=house,
                rooms=rooms,
            )
            .annotate(distance=Distance2P("position__location", point))
            .order_by("distance")
        )[:5]
        # estimate the price by multipliying the surface by the meter square price
        # the meter square price is obtained in terms of min, avg and max price of the top 5 ads
        result = {"min_price": "uknown", "avg_price": "uknown", "max_price": "uknown"}
        if advertisements:
            result["min_price"] = (
                float(surface)
                * advertisements.aggregate(Min("meter_square"))["meter_square__min"]
            )
            result["avg_price"] = (
                float(surface)
                * advertisements.aggregate(Avg("meter_square"))["meter_square__avg"]
            )
            result["max_price"] = (
                float(surface)
                * advertisements.aggregate(Max("meter_square"))["meter_square__max"]
            )

        return Response(result, status=status.HTTP_200_OK)
