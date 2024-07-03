from datetime import datetime

from django.db import models
from django.utils import timezone

from uavadmin.utils.models import CoreModel, get_custom_app_models, table_prefix


class UavVehicle(CoreModel):
    uid = models.CharField(max_length=64, verbose_name="设备识别码")
    model = models.CharField(max_length=64, verbose_name="型号")

    map_id = models.BigIntegerField()
    airport_id = models.BigIntegerField()

    status = models.IntegerField(verbose_name="状态", default=0, help_text="[]")

    class Meta:
        db_table = "uav_vehicle"
        verbose_name = "UAV"
        verbose_name_plural = verbose_name
        ordering = ("create_datetime",)
        app_label = "uav"

    def __str__(self):
        return f"{self.name}"


class UavMap(CoreModel):
    name = models.CharField(max_length=64, verbose_name="name")

    longitude = models.FloatField(verbose_name="经度")
    latitude = models.FloatField(verbose_name="纬度")
    altitude = models.FloatField(verbose_name="海拔")

    status = models.IntegerField(verbose_name="状态", default=0, help_text="[]")

    class Meta:
        db_table = "uav_map"
        verbose_name = "UAV"
        verbose_name_plural = verbose_name
        ordering = ("create_datetime",)
        app_label = "uav"

    def __str__(self):
        return f"{self.name}"


class UavAirport(CoreModel):
    name = models.CharField(max_length=64, verbose_name="name")
    city = models.CharField(max_length=64, verbose_name="city", null=True)

    map_id = models.BigIntegerField()
    x = models.FloatField(verbose_name="相对坐标，米")
    y = models.FloatField(verbose_name="相对坐标，米")
    z = models.FloatField(verbose_name="相对坐标，米")

    longitude = models.FloatField(verbose_name="经度", null=True)
    latitude = models.FloatField(verbose_name="纬度", null=True)
    altitude = models.FloatField(verbose_name="海拔", null=True)

    throughput = models.IntegerField(verbose_name="日吞吐量", default=0)
    num_wait_launch = models.IntegerField(
        verbose_name="等待起飞数量", null=True, default=0
    )
    num_wait_landing = models.IntegerField(
        verbose_name="等待降落数量", null=True, default=0
    )

    status = models.IntegerField(verbose_name="状态", default=0, help_text="[]")

    class Meta:
        db_table = "uav_airport"
        verbose_name = "UAV"
        verbose_name_plural = verbose_name
        ordering = ("create_datetime",)
        app_label = "uav"

    def __str__(self):
        return f"{self.name}"


class UavBasement(CoreModel):
    uid = models.CharField(max_length=64, verbose_name="基站编号")
    city = models.CharField(max_length=64, verbose_name="city", null=True)

    map_id = models.BigIntegerField()
    x = models.FloatField(verbose_name="相对坐标，米")
    y = models.FloatField(verbose_name="相对坐标，米")
    z = models.FloatField(verbose_name="相对坐标，米")

    longitude = models.FloatField(verbose_name="经度", null=True)
    latitude = models.FloatField(verbose_name="纬度", null=True)
    altitude = models.FloatField(verbose_name="海拔", null=True)

    eirp = models.CharField(max_length=64, verbose_name="eirp")
    band_width = models.CharField(max_length=64, verbose_name="band_width")
    num_channel = models.IntegerField(default=0, verbose_name="num_channel")

    status = models.IntegerField(verbose_name="状态", default=0, help_text="[]")

    class Meta:
        db_table = "uav_basement"
        verbose_name = "UAV"
        verbose_name_plural = verbose_name
        ordering = ("create_datetime",)
        app_label = "uav"

    def __str__(self):
        return f"{self.name}"


class UavFlight(CoreModel):
    vehicle_id = models.BigIntegerField(verbose_name="飞行器ID")
    map_id = models.BigIntegerField()

    launch_airport = models.BigIntegerField(verbose_name="起飞机场", null=True)
    launch_time = models.DateTimeField(verbose_name="起飞时间", null=True)
    landing_airport = models.BigIntegerField(verbose_name="降落机场", null=True)
    landing_time = models.DateTimeField(verbose_name="降落时间", null=True)
    trace = models.JSONField(verbose_name="轨迹", null=True)

    plan_launch_airport = models.BigIntegerField(verbose_name="计划起飞机场", null=True)
    plan_launch_time = models.DateTimeField(verbose_name="计划起飞时间", null=True)
    plan_landing_airport = models.BigIntegerField(
        verbose_name="计划降落机场", null=True
    )
    plan_landing_time = models.DateTimeField(verbose_name="计划降落时间", null=True)

    flight_duration = models.IntegerField(verbose_name="时长，毫秒", null=True)
    flight_distance = models.FloatField(verbose_name="距离，公里", null=True)
    flight_mileage = models.FloatField(verbose_name="里程，公里", null=True)

    status = models.IntegerField(verbose_name="状态", default=0, help_text="[]")

    class Meta:
        db_table = "uav_flight"
        verbose_name = "UAV"
        verbose_name_plural = verbose_name
        ordering = ("create_datetime",)
        app_label = "uav"

    def __str__(self):
        return f"{self.name}"


class UavTrack(CoreModel):
    topic = models.CharField(max_length=64, verbose_name="topic")
    pos = models.JSONField(verbose_name="轨迹", null=True)
    # create_time = models.DateTimeField(default=timezone.now)

    status = models.IntegerField(verbose_name="状态", default=0, help_text="[]")

    # def save(self, *args, **kwargs):
    #     # Ensure the timestamp has milliseconds precision
    #     self.create_time = self.create_time.replace(
    #         microsecond=int(self.create_time.microsecond / 1000) * 1000
    #     )
    #     super().save(*args, **kwargs)

    class Meta:
        db_table = "uav_track"
        verbose_name = "UAV"
        verbose_name_plural = verbose_name
        ordering = ("create_datetime",)
        app_label = "uav"

    def __str__(self):
        return f"{self.name}"
