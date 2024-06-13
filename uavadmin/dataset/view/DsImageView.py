# -*- coding: utf-8 -*-
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import parsers, renderers, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from uavadmin.dataset.models import DsDataset, DsImage, DsPatient
from uavadmin.dataset.serializers import DsImageSerializer
from uavadmin.utils.json_response import DetailResponse, ErrorResponse, SuccessResponse
from uavadmin.utils.serializers import CustomModelSerializer
from uavadmin.utils.viewset import CustomModelViewSet


class DsImageViewSet(CustomModelViewSet):
    """
    不良反应药品接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = DsImage.objects.all()
    serializer_class = DsImageSerializer

    def get_queryset(self):
        dataset_id = self.request.GET.get("dataset_id", "")
        if dataset_id:
            patient_list = DsPatient.objects.filter(dataset_id=dataset_id)
            self.queryset = self.queryset.filter(
                patient_id__in=[item.id for item in patient_list]
            )

        return self.queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 3
        instance.save()
        return DetailResponse(data=[], msg="删除成功")

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "dataset_id",
                openapi.IN_QUERY,
                description="dataset_id",
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, request=request)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, request=request)
        return SuccessResponse(data=serializer.data, msg="获取成功")

    # TODO 