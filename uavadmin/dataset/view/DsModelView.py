# -*- coding: utf-8 -*-
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import parsers, renderers, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from uavadmin.dataset.models import DsModel
from uavadmin.utils.json_response import DetailResponse, ErrorResponse, SuccessResponse
from uavadmin.utils.serializers import CustomModelSerializer
from uavadmin.utils.viewset import CustomModelViewSet


class DsModelSerializer(CustomModelSerializer):
    """
    不良反应库-序列化器
    """

    class Meta:
        model = DsModel
        fields = "__all__"
        read_only_fields = ["id"]


class DsModelViewSet(CustomModelViewSet):
    """
    不良反应药品接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = DsModel.objects.all()
    serializer_class = DsModelSerializer

    def create(self, request, *args, **kwargs):
        """
        {
          "name": "脱敏2",
          "api": "/lc/sub2/desensitive",
          "api_data": "\"value\":\"{}\"",
          "api_level": "image",
          "in_stage": 0,
          "in_require": "ds_image.url_origin",
          "out_stage": 1,
          "out_require": "ds_image.url_desensitive, ds_image.scale_factor"
        }
        """
        return super().create(request, args, kwargs)

    def get_queryset(self):
        name = self.request.GET.get("name__icontains", "")  # 获取关键字参数
        if name:
            # 使用 "icontains" 表示不区分大小写的包含查询
            self.queryset = self.queryset.filter(name__icontains=name)

        return self.queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 3
        instance.save()
        return DetailResponse(data=[], msg="删除成功")
