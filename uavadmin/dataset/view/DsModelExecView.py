# -*- coding: utf-8 -*-
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import parsers, renderers, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from uavadmin.dataset.models import DsDataset, DsModel, DsModelExec
from uavadmin.dataset.module import model_wrapper
from uavadmin.utils.json_response import DetailResponse, ErrorResponse, SuccessResponse
from uavadmin.utils.serializers import CustomModelSerializer
from uavadmin.utils.viewset import CustomModelViewSet


class DsModelExecSerializer(CustomModelSerializer):
    """
    不良反应库-序列化器
    """

    model_name = serializers.SerializerMethodField()
    dataset_name = serializers.SerializerMethodField()
    out_dataset_name = serializers.SerializerMethodField()

    def get_model_name(self, obj: DsModelExec):
        return DsModel.objects.get(id=obj.model_id).name

    def get_dataset_name(self, obj: DsModelExec):
        return DsDataset.objects.get(id=obj.dataset_id).name

    def get_out_dataset_name(self, obj: DsModelExec):
        try:
            if obj.out_dataset_id:
                return DsDataset.objects.get(id=obj.out_dataset_id).name
            elif obj.status_exec:
                return DsDataset.objects.get(id=obj.dataset_id).name
        except Exception as e:
            print(f"error")
        return ""

    class Meta:
        model = DsModelExec
        fields = "__all__"
        read_only_fields = ["id"]


class DsModelExecViewSet(CustomModelViewSet):
    """
    不良反应药品接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = DsModelExec.objects.all()
    serializer_class = DsModelExecSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["id", "out_type"],
            properties={
                "id": openapi.Schema(
                    description="模型执行记录ID",
                    type=openapi.TYPE_INTEGER,
                ),
            },
        ),
        operation_summary="执行任务",
    )
    @action(
        methods=["POST"],
        detail=False,
        permission_classes=[IsAuthenticated],
        extra_filter_class=[],
    )
    def do_exec(self, request, *args, **kwargs):
        id = request.data.get("id", None)
        out_type = request.data.get("out_type", None)

        model_exec = DsModelExec.objects.get(id=id)
        if not model_exec:
            return ErrorResponse(msg="no such task")
        if model_exec.status == 3:
            return ErrorResponse(msg="deleted")
        if model_exec.status_exec != 0:
            return ErrorResponse(msg=f"run status={model_exec.status_exec}")

        # 检查输入数据集是否符合in_require
        flag_check_dataset, msg = model_wrapper.check_dataset(model_exec)
        if not flag_check_dataset:
            logger.error(msg)
            return ErrorResponse(msg=f"数据格式问题={msg}")

        model_exec.status_exec = 10
        model_exec.exec_start_time = datetime.now()
        model_exec.save()

        status_exec, msg = model_wrapper.exec_model(model_exec)
        # TODO celery
        model_exec.status_exec = status_exec
        model_exec.exec_end_time = datetime.now()
        model_exec.save()
        if status_exec == 1:
            return SuccessResponse()
        else:
            logger.error(msg)
            return ErrorResponse(msg=msg)

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
