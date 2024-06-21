# mqtt_client.py

import paho.mqtt.client as mqtt

from appuav.settings import MQTT_CONF


# 回调函数：连接时
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    for id in range(50):
        client.subscribe(f'{MQTT_CONF["MQTT_TOPIC_PREFIX"]}/{id}')


# 回调函数：接收消息时
def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")


# mqtt_client.py (添加断开连接处理)
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")
        client.reconnect()


# 创建MQTT客户端
client = mqtt.Client(client_id=MQTT_CONF["CLIENT_ID_R"])
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
# 设置用户名和密码
client.username_pw_set(MQTT_CONF["MQTT_USERNAME"], MQTT_CONF["MQTT_PASSWORD"])


## client_sender
client_sender = mqtt.Client(client_id=MQTT_CONF["CLIENT_ID_S"])
client_sender.on_disconnect = on_disconnect
client_sender.username_pw_set(MQTT_CONF["MQTT_USERNAME"], MQTT_CONF["MQTT_PASSWORD"])


def publish_message(message):
    client_sender.publish(f'{MQTT_CONF["MQTT_TOPIC_PREFIX"]}/6', message)


def start_mqtt_client():
    client.connect(
        MQTT_CONF["MQTT_BROKER_PUBLIC"],
        MQTT_CONF["MQTT_PORT"],
        MQTT_CONF["MQTT_KEEPALIVE_INTERVAL"],
    )
    client.loop_start()

    client_sender.connect(
        MQTT_CONF["MQTT_BROKER_PUBLIC"],
        MQTT_CONF["MQTT_PORT"],
        MQTT_CONF["MQTT_KEEPALIVE_INTERVAL"],
    )
    client_sender.loop_start()
