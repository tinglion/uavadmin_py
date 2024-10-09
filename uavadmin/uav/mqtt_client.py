# mqtt_client.py
import logging

import paho.mqtt.client as mqtt

from appuav.settings import MQTT_CONF
from uavadmin.uav.models import UavTrack
from uavadmin.uav.module import radar2_wrapper
from uavadmin.utils import string_util

logger = logging.getLogger(__name__)


pending_messages = []


# 回调函数：连接时
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info(f"Connected {client._client_id}")
        client.subscribe(MQTT_CONF["MQTT_TOPIC_RADAR"])
        client.subscribe(MQTT_CONF["MQTT_TOPIC_UAV"])

        # old
        for id in range(50):
            client.subscribe(f'{MQTT_CONF["MQTT_TOPIC_PREFIX"]}/{id}')

        for topic, payload in pending_messages:
            client.publish(topic, payload)
        pending_messages.clear()
    elif rc == 5:
        print("Connection refused: Not authorized (Check your username and password)")
    else:
        print(f"Connection failed with rc={rc}")


# test
def on_connect2(client, userdata, flags, rc):
    logger.info("Connected with code=" + str(rc))
    for id in range(50):
        client.subscribe(f'{MQTT_CONF["MQTT_TOPIC_PREFIX"]}/{id}')


# mqtt_client.py (添加断开连接处理)
def on_disconnect(client, userdata, rc):
    if rc != 0:
        logger.info(f"Unexpected disconnection. {client._client_id} {userdata} {rc}")
        client.reconnect()


# test
def on_disconnect2(client, userdata, rc):
    if rc != 0:
        logger.info("Unexpected disconnection!")
        client.reconnect()


# 回调函数：接收消息时
def on_message(client, userdata, msg):
    content = msg.payload.decode()
    logger.info(f"Received topic={msg.topic} message={content}")
    if (
        msg.topic == MQTT_CONF["MQTT_TOPIC_RADAR"]
        or msg.topic == MQTT_CONF["MQTT_TOPIC_UAV"]
    ):
        #
        radar2_wrapper.do_message(content=content, topic=msg.topic)
    else:
        # 保存历史轨迹
        UavTrack.objects.create(topic=msg.topic, pos=content)


class MqttClient:
    def __init__(self):
        self.client = None
        self.client_sender = None
        logger.info("init")

    def publish_message(self, message, topic):
        if not self.client_sender:
            self.start_mqtt_client()
        if self.client_sender:
            if self.client_sender.is_connected():
                self.client_sender.publish(topic, message)
            else:
                pending_messages.append((topic, message))

    def _start_receiver(self):
        if not self.client:
            self.client = mqtt.Client(
                client_id=f'{MQTT_CONF["CLIENT_ID_R"]}_{string_util.random_str(4)}'
            )  # random
            self.client.on_connect = on_connect
            self.client.on_message = on_message
            self.client.on_disconnect = on_disconnect
            # 设置用户名和密码
            self.client.username_pw_set(
                MQTT_CONF["MQTT_USERNAME"], MQTT_CONF["MQTT_PASSWORD"]
            )
            self.client.connect(
                MQTT_CONF["MQTT_BROKER_PUBLIC"],
                # MQTT_CONF["MQTT_BROKER"],
                port=MQTT_CONF["MQTT_PORT"],
                keepalive=MQTT_CONF["MQTT_KEEPALIVE_INTERVAL"],
            )
            logger.info(f"connect to {self.client.host} with {self.client._client_id}")
            self.client.loop_start()  # loop_start

    def _start_sender(self):
        if not self.client_sender:
            self.client_sender = mqtt.Client(
                client_id=f'{MQTT_CONF["CLIENT_ID_S"]}_{string_util.random_str(4)}'
            )
            self.client_sender.username_pw_set(
                MQTT_CONF["MQTT_USERNAME"], MQTT_CONF["MQTT_PASSWORD"]
            )
            self.client_sender.on_connect = on_connect
            self.client_sender.on_disconnect = on_disconnect
            self.client_sender.connect(
                MQTT_CONF["MQTT_BROKER_PUBLIC"],
                # MQTT_CONF["MQTT_BROKER"],
                port=MQTT_CONF["MQTT_PORT"],
                keepalive=MQTT_CONF["MQTT_KEEPALIVE_INTERVAL"],
            )
            logger.info(
                f"connect to {self.client_sender.host} with {self.client_sender._client_id}"
            )
            self.client_sender.loop_start()  # loop_forever()

    def start_mqtt_client(self):
        logger.info(f"start")
        if not self.client:
            self._start_receiver()

        ## client_sender
        if not self.client_sender:
            self._start_sender()


mqtt_client = MqttClient()


# tclient = mqtt.Client(client_id="tclient")
# tclient.on_connect = on_connect2
# tclient.on_disconnect = on_disconnect2
# # 设置用户名和密码
# tclient.username_pw_set(MQTT_CONF["MQTT_USERNAME"], MQTT_CONF["MQTT_PASSWORD"])
# tclient.connect(
#     MQTT_CONF["MQTT_BROKER_PUBLIC"],
#     # MQTT_CONF["MQTT_BROKER"],
#     MQTT_CONF["MQTT_PORT"],
#     MQTT_CONF["MQTT_KEEPALIVE_INTERVAL"],
# )
# tclient.loop_start()
