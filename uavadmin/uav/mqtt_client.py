# mqtt_client.py

import paho.mqtt.client as mqtt

from appuav.settings import MQTT_CONF
from uavadmin.uav.models import UavTrack


# 回调函数：连接时
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    for id in range(50):
        client.subscribe(f'{MQTT_CONF["MQTT_TOPIC_PREFIX"]}/{id}')


# 回调函数：接收消息时
def on_message(client, userdata, msg):
    # TODO 保存历史轨迹
    content = msg.payload.decode()
    print(f"Received message: {content} on topic {msg.topic}")
    UavTrack.objects.create(topic=msg.topic, pos=content)


# mqtt_client.py (添加断开连接处理)
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")
        client.reconnect()


class MqttClient:
    def __init__(self):
        self.client = None
        self.client_sender = None

    def publish_message(self, message, topic=f'{MQTT_CONF["MQTT_TOPIC_PREFIX"]}/6'):
        if self.client_sender:
            self.client_sender.publish(topic, message)

    def start_mqtt_client(self):
        if not self.client:
            self.client = mqtt.Client(client_id=MQTT_CONF["CLIENT_ID_R"])
            self.client.on_connect = on_connect
            self.client.on_message = on_message
            self.client.on_disconnect = on_disconnect
            # 设置用户名和密码
            self.client.username_pw_set(
                MQTT_CONF["MQTT_USERNAME"], MQTT_CONF["MQTT_PASSWORD"]
            )
            self.client.connect(
                MQTT_CONF["MQTT_BROKER_PUBLIC"],
                MQTT_CONF["MQTT_PORT"],
                MQTT_CONF["MQTT_KEEPALIVE_INTERVAL"],
            )
            self.client.loop_start()
            print(
                f'connect to {MQTT_CONF["MQTT_BROKER_PUBLIC"]} with {MQTT_CONF["CLIENT_ID_R"]}'
            )

        ## client_sender
        if not self.client_sender:
            self.client_sender = mqtt.Client(client_id=MQTT_CONF["CLIENT_ID_S"])
            self.client_sender.on_disconnect = on_disconnect
            self.client_sender.username_pw_set(
                MQTT_CONF["MQTT_USERNAME"], MQTT_CONF["MQTT_PASSWORD"]
            )
            self.client_sender.connect(
                MQTT_CONF["MQTT_BROKER_PUBLIC"],
                MQTT_CONF["MQTT_PORT"],
                MQTT_CONF["MQTT_KEEPALIVE_INTERVAL"],
            )
            self.client_sender.loop_start()
            print(
                f'connect to {MQTT_CONF["MQTT_BROKER_PUBLIC"]} with {MQTT_CONF["CLIENT_ID_S"]}'
            )

mqtt_client = MqttClient()