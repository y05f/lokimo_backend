from advertisement.models import Advertisement
from .serializers import AdvertisementSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance as DistanceM
from django.contrib.gis.db.models.functions import Distance as Distance2P
from django.db.models import Avg, Min, Max


class AdvertisementList(APIView):
    """
    List all advertisements, or create a new advertisement.
    """

    def get(self, request, format=None):
        advertisement = Advertisement.objects.all()
        serializer = AdvertisementSerializer(advertisement, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AdvertisementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdvertisementRetrieveDelete(APIView):
    """
    Retrieve or delete an advertisement instance.
    """

    def get_object(self, pk):
        try:
            return Advertisement.objects.get(pk=pk)
        except Advertisement.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        advertisement = self.get_object(pk)
        serializer = AdvertisementSerializer(advertisement)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        advertisement = self.get_object(pk)
        advertisement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdvertisementCity(APIView):
    """
    Retrieve advertisements by city code.
    """

    def get(self, request, city):
        advertisement = Advertisement.objects.filter(city=city)
        serializer = AdvertisementSerializer(advertisement, many=True)
        return Response(serializer.data)


class AdvertisementGeoPrice(APIView):
    """
    Retrieve average meter square prices by position and radius.
    """

    def get(self, request, lat, lng, radius, format=None):

        point = Point(float(lng), float(lat))

        advertisement = Advertisement.objects.filter(
            position__location__distance_lte=(point, DistanceM(m=float(radius))),
        )
        result = {}
        result["T1"] = advertisement.filter(rooms=1).aggregate(Avg("meter_square"))[
            "meter_square__avg"
        ]
        result["T2"] = advertisement.filter(rooms=2).aggregate(Avg("meter_square"))[
            "meter_square__avg"
        ]
        result["T3"] = advertisement.filter(rooms=3).aggregate(Avg("meter_square"))[
            "meter_square__avg"
        ]
        result["T4P"] = advertisement.filter(rooms__gte=4).aggregate(
            Avg("meter_square")
        )["meter_square__avg"]
        return Response(result, status=status.HTTP_200_OK)


class AdvertisementPriceEstimator(APIView):
    """
    Return price estimation using housing type, rooms, surface and address or location.
    The prices are given by multipliying the surface by the meter square price.
    The meter square price is estimated in terms of min, avg and max on the closest
    5 ads with the the same housing type and the number of rooms
    """

    def get(self, request, house, rooms, surface, lat, lng, format=None):
        point = Point(float(lng), float(lat), srid=4326)

        advertisement = (
            Advertisement.objects.filter(
                house=house,
                rooms=rooms,
            )
            .annotate(distance=Distance2P("position__location", point))
            .order_by("distance")
        )[:5]
        result = {"min_price": "uknown", "avg_price": "uknown", "max_price": "uknown"}
        if advertisement:
            result["min_price"] = (
                float(surface)
                * advertisement.aggregate(Min("meter_square"))["meter_square__min"]
            )
            result["avg_price"] = (
                float(surface)
                * advertisement.aggregate(Avg("meter_square"))["meter_square__avg"]
            )
            result["max_price"] = (
                float(surface)
                * advertisement.aggregate(Max("meter_square"))["meter_square__max"]
            )

        return Response(result)
