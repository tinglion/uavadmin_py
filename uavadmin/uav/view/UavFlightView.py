# -*- coding: utf-8 -*-
import os

from django.db import transaction
from django.http import HttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import parsers, renderers, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from uavadmin.uav.models import UavFlight
from uavadmin.uav.serializers import UavFlightSerializer
from uavadmin.utils.json_response import DetailResponse, ErrorResponse, SuccessResponse
from uavadmin.utils.viewset import CustomModelViewSet


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
