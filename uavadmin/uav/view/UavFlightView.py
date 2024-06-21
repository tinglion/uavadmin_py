# -*- coding: utf-8 -*-
import json
import logging
import os
import traceback
import time

from django.db import transaction
from django.http import HttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import parsers, renderers, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from uavadmin.uav import mqtt_client
from uavadmin.uav.models import UavFlight
from uavadmin.uav.serializers import UavFlightSerializer
from uavadmin.utils.json_response import DetailResponse, ErrorResponse, SuccessResponse
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
                time.sleep(1)
            return SuccessResponse()
        except Exception as e:
            logger.error(f"ERROR {id} {e}")
            traceback.print_exc()
        return ErrorResponse(msg="error")
