from django.urls import include, path
from rest_framework import routers

from uavadmin.uav.view import (
    UavAirportView,
    UavBasementView,
    UavFlightView,
    UavMapView,
    UavVehicleView,
)

uav_url = routers.SimpleRouter()
uav_url.register(r"uav_vehicle", UavVehicleView.UavVehicleViewSet)
uav_url.register(r"uav_flight", UavFlightView.UavFlightViewSet)
uav_url.register(r"uav_basement", UavBasementView.UavBasementViewSet)
uav_url.register(r"uav_airport", UavAirportView.UavAirportViewSet)
uav_url.register(r"uav_map", UavMapView.UavMapViewSet)

urlpatterns = [
    path("", include(uav_url.urls)),
]
