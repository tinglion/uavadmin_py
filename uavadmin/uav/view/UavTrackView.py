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

from uavadmin.uav import mqtt_client
from uavadmin.uav.models import UavTrack
from uavadmin.uav.module import datafile_wrapper
from uavadmin.uav.serializers import UavTrackSerializer
from uavadmin.utils.json_response import DetailResponse, ErrorResponse, SuccessResponse
from uavadmin.utils.time_utils import time_str_to_millis
from uavadmin.utils.viewset import CustomModelViewSet

logger = logging.getLogger(__name__)


class UavTrackViewSet(CustomModelViewSet):
    """
    不良反应药品接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = UavTrack.objects.all()
    serializer_class = UavTrackSerializer

    def get_queryset(self):
        create_from = self.request.GET.get("create_from", "")
        create_to = self.request.GET.get("create_to", "")
        if create_from and create_to:
            self.queryset = self.queryset.filter(
                create_datetime__range=(create_from, create_to)
            )
        return self.queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 3
        instance.save()
        return DetailResponse(data=[], msg="删除成功")
