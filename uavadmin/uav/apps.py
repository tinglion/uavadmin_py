import os

from django.apps import AppConfig

from .mqtt_client import start_mqtt_client


class UavConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "uavadmin.uav"

    def ready(self):
        if os.environ.get("RUN_MAIN") == "true":
            print(f"@sting start mqtt")
            # 在Django应用启动时启动MQTT客户端
            start_mqtt_client()
