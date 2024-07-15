import os

from django.apps import AppConfig


class UavConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "uavadmin.uav"

    # def ready(self):
    #     # if os.environ.get("RUN_MAIN") == "true":
    #     在Django应用启动时启动MQTT客户端 —— but 会频繁重连
    #     from .mqtt_client import mqtt_client
    #     mqtt_client.start_mqtt_client()
