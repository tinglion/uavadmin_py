import json
import logging
import re

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from uavadmin.system.models import Users
from uavadmin.uav.models import UavTrack
from uavadmin.utils import coord_transform

logger = logging.getLogger(__name__)


def websocket_push(user_id, message):
    """
    主动推送消息
    """
    username = "user_" + str(user_id)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        username, {"type": "push.message", "json": message}
    )


# # 收到消息，保存，换算坐标，发送给前端
def do_message(content, topic=""):
    if not content:
        return
    msg = json.loads(content)

    # all users
    # TODO 后台配置需要通知的用户
    all_user_ids = list(Users.objects.all().values_list("id", flat=True))
    logger.info(f"users={len(all_user_ids)}")

    n = 0
    for item in msg["participants"]:
        item["time"] = msg["time"]

        # save
        UavTrack.objects.create(topic=item["id"], pos=item)

        # WGS84转GCJ02(火星坐标系)
        xy = coord_transform.wgs84_to_gcj02(
            item["location"]["longitude"], item["location"]["latitude"]
        )
        item["location"]["longitude"] = xy[0]
        item["location"]["latitude"] = xy[1]

        # 发送给前端 websocket
        item["contentType"] = "radar2"
        for id in all_user_ids:
            websocket_push(id, message=item)
            # logger.info(f"Sent id={id} message={item}")

        n += 1
    logger.info(f"msg={n}")
    return n
