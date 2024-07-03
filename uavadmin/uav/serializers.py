from rest_framework import serializers

from uavadmin.uav.models import *
from uavadmin.utils.serializers import CustomModelSerializer


class UavVehicleSerializer(CustomModelSerializer):
    """
    序列化器
    """

    name_map = serializers.SerializerMethodField()

    def get_name_map(self, obj: UavVehicle):
        try:
            return UavMap.objects.get(id=obj.map_id).name
        except Exception as e:
            return None

    class Meta:
        model = UavVehicle
        fields = "__all__"
        read_only_fields = ["id"]


class UavMapSerializer(CustomModelSerializer):
    """
    序列化器
    """

    num_airport = serializers.SerializerMethodField()

    def get_num_airport(self, obj: UavMap):
        try:
            return len(UavAirport.objects.filter(map_id=obj.id))
        except Exception as e:
            return None

    num_basement = serializers.SerializerMethodField()

    def get_num_basement(self, obj: UavMap):
        try:
            return len(UavBasement.objects.filter(map_id=obj.id))
        except Exception as e:
            return None

    class Meta:
        model = UavMap
        fields = "__all__"
        read_only_fields = ["id"]


class UavAirportSerializer(CustomModelSerializer):
    """
    序列化器
    """

    name_map = serializers.SerializerMethodField()

    def get_name_map(self, obj: UavAirport):
        try:
            return UavMap.objects.get(id=obj.map_id).name
        except Exception as e:
            return None

    class Meta:
        model = UavAirport
        fields = "__all__"
        read_only_fields = ["id"]


class UavBasementSerializer(CustomModelSerializer):
    """
    序列化器
    """

    name_map = serializers.SerializerMethodField()

    def get_name_map(self, obj: UavBasement):
        try:
            return UavMap.objects.get(id=obj.map_id).name
        except Exception as e:
            return None

    class Meta:
        model = UavBasement
        fields = "__all__"
        read_only_fields = ["id"]


class UavFlightSerializer(CustomModelSerializer):
    """
    序列化器
    """

    vehicle_uid = serializers.SerializerMethodField()

    def get_vehicle_uid(self, obj: UavFlight):
        try:
            v = UavVehicle.objects.get(id=obj.vehicle_id)
            return v.uid if v else None
        except Exception as e:
            return None

    def get_airport(self, id):
        try:
            return UavAirport.objects.get(id=id)
        except Exception as e:
            return None

    launch_airport_name = serializers.SerializerMethodField()

    def get_launch_airport_name(self, obj: UavFlight):
        try:
            v = self.get_airport(id=obj.launch_airport)
            return v.name if v else None
        except Exception as e:
            return None

    landing_airport_name = serializers.SerializerMethodField()

    def get_landing_airport_name(self, obj: UavFlight):
        try:
            v = self.get_airport(id=obj.landing_airport_name)
            return v.name if v else None
        except Exception as e:
            return None

    plan_launch_airport_name = serializers.SerializerMethodField()

    def get_plan_launch_airport_name(self, obj: UavFlight):
        try:
            v = self.get_airport(id=obj.plan_launch_airport)
            return v.name if v else None
        except Exception as e:
            return None

    plan_landing_airport_name = serializers.SerializerMethodField()

    def get_plan_landing_airport_name(self, obj: UavFlight):
        try:
            v = self.get_airport(id=obj.plan_landing_airport)
            return v.name if v else None
        except Exception as e:
            return None

    class Meta:
        model = UavFlight
        fields = "__all__"
        read_only_fields = ["id"]


class UavTrackSerializer(CustomModelSerializer):
    """
    序列化器
    """

    class Meta:
        model = UavTrack
        fields = "__all__"
        read_only_fields = ["id"]
