from django.contrib import admin
from .models import Advertisement, Data, Position, Status

admin.site.register(Status)
admin.site.register(Data)
admin.site.register(Position)
admin.site.register(Advertisement)
