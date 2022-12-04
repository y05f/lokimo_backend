from django.contrib.gis.db import models
from django.contrib.gis.geos import Point


# All fields are preserved except id
# The schema follow the same schema of the initial JSON raw data


class Position(models.Model):
    location = models.PointField(geography=True, default=Point(0.0, 0.0))

    @property
    def lng(self):
        return self.location.x

    @property
    def lat(self):
        return self.location.y


class Status(models.Model):
    autoImported = models.BooleanField()
    closedByUser = models.BooleanField()
    highlighted = models.BooleanField()
    is3dHighlighted = models.BooleanField()
    isLeading = models.BooleanField()
    onTheMarket = models.BooleanField()


class Data(models.Model):
    address = models.CharField(max_length=250, blank=True, null=True)
    availableDate = models.CharField(max_length=50, blank=True)
    balconyQuantity = models.IntegerField(null=True)
    balconySurfaceArea = models.FloatField(null=True)
    bathroomsQuantity = models.IntegerField(null=True)
    bedroomsQuantity = models.IntegerField(null=True)
    city = models.CharField(max_length=50)
    exposition = models.CharField(max_length=50, blank=True)
    floor = models.IntegerField(null=True)
    floorQuantity = models.IntegerField(null=True)
    gardenSurfaceArea = models.FloatField(null=True)
    hasAirConditioning = models.BooleanField(null=True)
    hasAlarm = models.BooleanField(null=True)
    hasBalcony = models.BooleanField(null=True)
    hasCaretaker = models.BooleanField(null=True)
    hasCellar = models.BooleanField(null=True)
    hasDoorCode = models.BooleanField(null=True)
    hasElevator = models.BooleanField(null=True)
    hasFirePlace = models.BooleanField(null=True)
    hasGarden = models.BooleanField(null=True)
    hasIntercom = models.BooleanField(null=True)
    hasParquet = models.BooleanField(null=True)
    hasPool = models.BooleanField(null=True)
    hasSeparateToilet = models.BooleanField(null=True)
    hasTerrace = models.BooleanField(null=True)
    hasVideophone = models.BooleanField(null=True)
    heating = models.CharField(max_length=250, blank=True)
    isInStudentResidence = models.BooleanField(null=True)
    isRecent = models.BooleanField(null=True)
    link = models.CharField(max_length=250, blank=True)
    newOrOld = models.CharField(max_length=50, blank=True)
    newProperty = models.BooleanField()
    opticalFiberStatus = models.CharField(max_length=50, blank=True)
    outdoorParkingQuantity = models.IntegerField(null=True)
    parkingPlacesQuantity = models.IntegerField(null=True)
    priceWithoutFees = models.FloatField(null=True)
    publicationDate = models.CharField(max_length=50)
    reference = models.CharField(max_length=50, blank=True)
    showerRoomsQuantity = models.IntegerField(null=True)
    status = models.OneToOneField(Status, on_delete=models.CASCADE)
    terracesQuantity = models.IntegerField(null=True)
    thresholdDate = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=250, blank=True)
    toiletQuantity = models.IntegerField(null=True)
    transactionType = models.CharField(max_length=250)
    yearOfConstruction = models.IntegerField(null=True)

    def __str__(self):
        return self.title


class Advertisement(models.Model):
    # date and time of adding an ad to our backend
    created = models.DateTimeField(auto_now_add=True)
    # the rest of fields from the raw JSON file
    buy = models.BooleanField()
    data = models.OneToOneField(Data, on_delete=models.CASCADE)
    city = models.CharField(max_length=50)
    first_date = models.CharField(max_length=50)
    good_id = models.CharField(max_length=50)
    house = models.BooleanField()
    iris = models.CharField(max_length=50)
    last_date = models.CharField(max_length=50)
    meter_square = models.IntegerField()
    position = models.OneToOneField(Position, null=True, on_delete=models.CASCADE)
    price = models.FloatField()
    rooms = models.IntegerField()
    surface = models.IntegerField()

    def __str__(self):
        return self.data.title
