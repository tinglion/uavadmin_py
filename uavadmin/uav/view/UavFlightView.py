# -*- coding: utf-8 -*-
import json
import logging
import os
import time
import traceback
from datetime import datetime

from django.db import transaction
from django.http import HttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import parsers, renderers, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from uavadmin.uav.mqtt_client import mqtt_client
from uavadmin.uav.models import UavFlight
from uavadmin.uav.module import datafile_wrapper
from uavadmin.uav.serializers import UavFlightSerializer
from uavadmin.utils.json_response import DetailResponse, ErrorResponse, SuccessResponse
from uavadmin.utils.time_utils import time_str_to_millis
from uavadmin.utils.viewset import CustomModelViewSet

logger = logging.getLogger(__name__)


class UavFlightViewSet(CustomModelViewSet):
    """
    不良反应药品接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = UavFlight.objects.all()
    serializer_class = UavFlightSerializer

    def get_queryset(self):

        return self.queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 3
        instance.save()
        return DetailResponse(data=[], msg="删除成功")

    # mock
    @swagger_auto_schema(
        operation_summary="init mqtt client",
    )
    @action(
        methods=["GET"],
        detail=False,
        permission_classes=[IsAuthenticated],
        extra_filter_class=[],
    )
    def start_mqtt(self, request):
        try:
            mqtt_client.start_mqtt_client()
            return SuccessResponse()
        except Exception as e:
            logger.error(f"ERROR {id} {e}")
            traceback.print_exc()
        return ErrorResponse(msg="error")

    # mock
    @swagger_auto_schema(
        operation_summary="do it",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["id"],
            example={"id": 5},
            properties={
                "id": openapi.Schema(
                    description="flight id to mock up",
                    type=openapi.TYPE_INTEGER,
                ),
            },
        ),
    )
    @action(
        methods=["POST"],
        detail=False,
        permission_classes=[IsAuthenticated],
        extra_filter_class=[],
    )
    def mockup(self, request):
        id = request.data.get("id")
        if not id:
            return ErrorResponse(msg="id needead")

        try:
            flight = UavFlight.objects.get(id=id)
            for position in flight.trace:
                mqtt_client.publish_message(json.dumps(position))
                # time.sleep(1)
            return SuccessResponse()
        except Exception as e:
            logger.error(f"ERROR {id} {e}")
            traceback.print_exc()
        return ErrorResponse(msg="error")

    # mock
    @swagger_auto_schema(operation_summary="radar", example="{}")
    @action(
        methods=["GET"],
        detail=False,
        permission_classes=[IsAuthenticated],
        extra_filter_class=[],
    )
    def mock_radar(self, request):
        try:
            # rlist = json.load("./data/flight.json")
            pos_list = datafile_wrapper.load_flight_from_xls()
            # for position in pos_list:
            #     mqtt_client.publish_message(
            #         json.dumps(position["pos"]), topic=position["topic"]
            #     )

            # different topic
            pre_map = {}
            topic_map = {}
            for item in pos_list:
                topic = item["topic"]

                cur_time = time_str_to_millis(item["pos"]["time"])
                if topic in pre_map:
                    pre_time = pre_map[topic]
                    if pre_time and cur_time > pre_time:
                        time.sleep((cur_time - pre_time) / 1000)
                pre_map[topic] = cur_time

                if topic not in topic_map:
                    topic_map[topic] = 0
                topic_map[topic] += 1

                mqtt_client.publish_message(json.dumps(item["pos"]), topic=topic)

            return SuccessResponse(msg=f"{topic_map}")
        except Exception as e:
            logger.error(f"ERROR {e}")
            traceback.print_exc()
        return ErrorResponse(msg="error")
