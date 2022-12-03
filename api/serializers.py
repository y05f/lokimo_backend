from rest_framework import serializers
from advertisement.models import Status, Data, Position, Advertisement


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        # fields = "__all__"
        exclude = ["id"]


class PositionSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lng = serializers.FloatField()


class DataSerializer(serializers.ModelSerializer):
    status = StatusSerializer()

    class Meta:
        model = Data
        # fields = "__all__"
        exclude = ["id"]


class AdvertisementSerializer(serializers.ModelSerializer):
    data = DataSerializer()
    position = PositionSerializer(allow_null=True)

    class Meta:
        model = Advertisement
        fields = "__all__"

    def create(self, validated_data):
        data_data = validated_data.pop("data")
        status_data = data_data.pop("status")
        position_data = validated_data.pop("position")
        if position_data:
            longitude = position_data.pop("lng")
            latitude = position_data.pop("lat")
            location_data = {
                "location": "POINT(" + str(longitude) + " " + str(latitude) + ")"  # WKT
            }
            position = Position.objects.create(**location_data)
        else:
            position = None
        status = Status.objects.create(**status_data)
        data = Data.objects.create(status=status, **data_data)
        advertisement = Advertisement.objects.create(
            data=data, position=position, **validated_data
        )
        return advertisement
