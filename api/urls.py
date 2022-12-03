from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("ads/", views.AdvertisementList.as_view(), name="list-post-ads"),
    path(
        "ads/<int:pk>/",
        views.AdvertisementRetrieveDelete.as_view(),
        name="get-delete-ads",
    ),
    path(
        "ads/city/<int:city>/", views.AdvertisementCity.as_view(), name="get-city-ads"
    ),
    path(
        "ads/geoprice/<str:lat>/<str:lng>/<int:radius>/",
        views.AdvertisementGeoPrice.as_view(),
        name="get-geo-prices",
    ),
    path(
        "ads/estimateprice/<str:house>/<int:rooms>/<int:surface>/<str:lat>/<str:lng>/",
        views.AdvertisementPriceEstimator.as_view(),
        name="estimate-price",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
