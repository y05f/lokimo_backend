from django.core.management.base import BaseCommand, CommandError
from advertisement.models import Advertisement, Data, Position, Status
import json


class Command(BaseCommand):
    help = "Populate the initial data from raw JSON file"

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            "--delete",
            action="store_true",
            help="Delete all data before populating the intial data",
        )

    def handle(self, *args, **options):
        advertisement = Advertisement.objects.all()
        if options["delete"]:
            advertisement.delete()

        f = open("lokimo-dataset-backend-test.json")
        rawdata = json.load(f)
        f.close()

        for ads_data in rawdata:
            ads_data.pop("id")
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
            else:
                position = None
            advertisement = Advertisement.objects.create(
                data=data, position=position, **ads_data
            )
        self.stdout.write(self.style.SUCCESS("Initial raw data successfully inserted"))
