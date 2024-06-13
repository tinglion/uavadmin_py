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

from uavadmin.dataset.models import DsDataset, DsImage, DsPatient
from uavadmin.dataset.module import port_wrapper
from uavadmin.dataset.serializers import DsDatasetSerializer
from uavadmin.utils.json_response import DetailResponse, ErrorResponse, SuccessResponse
from uavadmin.utils.viewset import CustomModelViewSet


class DsDatasetViewSet(CustomModelViewSet):
    """
    不良反应药品接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = DsDataset.objects.all()
    serializer_class = DsDatasetSerializer

    def get_queryset(self):
        name = self.request.GET.get("name__icontains", "")  # 获取关键字参数
        if name:
            # 使用 "icontains" 表示不区分大小写的包含查询
            self.queryset = self.queryset.filter(name__icontains=name)

        return self.queryset

    def create(self, request, *args, **kwargs):
        """
        {
            "name": "kickoff dataset v0.1",
            "stage": 0,
            "description": "test",
            "patients": [
                {
                    "uid": 1132,
                    "image_url": [
                        "https://files.833.team/upload/2023/09/65cd3b33-bdc4-473f-980e-07bd9b9eb89e",
                        "https://files.833.team/upload/2023/09/3d377883-a1a4-431d-b49e-a5337f8d7f38",
                        "https://files.833.team/upload/2023/09/d85e1549-e0f6-46b5-b3c6-70e37c8544df"
                    ]
                }
            ]
        }
        """
        data = request.data
        dataset_name = data.get("name", None)
        if not dataset_name:
            return ErrorResponse(msg="wrong format")

        old_dataset_list = DsDataset.objects.filter(name=dataset_name)
        if len(old_dataset_list) > 0:
            return ErrorResponse(msg="dataset existed")

        n_patient = 0
        n_image = 0
        with transaction.atomic():
            # 添加dataset
            new_dataset = DsDataset.objects.create(
                name=dataset_name,
                description=data.get("description", None),
                stage=data.get("stage", None),
            )
            if not new_dataset:
                return ErrorResponse(msg="fail in create dataset")

            # 添加patient
            for patient in data.get("patients", list()):
                new_patient = DsPatient.objects.create(
                    dataset_id=new_dataset.id,
                    uid=patient.get("uid", None),
                )
                n_patient += 1
                for image_url in patient.get("image_url", list()):
                    new_image = DsImage.objects.create(
                        patient_id=new_patient.id,
                        url=image_url,
                        url_origin=image_url,
                    )
                    n_image += 1

        msg = (
            f"loaded dataset={new_dataset.name}, patients={n_patient}, images={n_image}"
        )
        print(f"@sting {msg}")
        return DetailResponse(msg=msg, data=new_dataset.id)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 3
        instance.save()
        return DetailResponse(data=[], msg="删除成功")

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["id"],
            properties={
                "id": openapi.Schema(
                    description="导出数据集ID",
                    type=openapi.TYPE_INTEGER,
                ),
            },
        ),
        operation_summary="导出数据集",
    )
    @action(
        methods=["POST"],
        detail=False,
        permission_classes=[IsAuthenticated],
        extra_filter_class=[],
    )
    def export_xls(self, request, *args, **kwargs):
        id = self.request.data.get("id", None)
        if not id:
            return ErrorResponse(msg="need id")

        fn = port_wrapper.export_dataset(id=id)
        if not fn:
            return ErrorResponse(msg="export failed")

        with open(fn, "rb") as zip_file:
            response = HttpResponse(zip_file.read(), content_type="application/zip")
            response["Content-Disposition"] = f'attachment; filename="{fn}"'
            zip_file.close()

            # os.remove(fn)
            return response
        return ErrorResponse(msg="download failed")
