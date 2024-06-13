import json
import logging
import traceback
import zipfile

from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import parsers, renderers, serializers, status
from rest_framework.decorators import action, api_view, parser_classes
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from appuav.settings import TEMP_DIR
from uavadmin.dataset.module import port_wrapper
from uavadmin.utils.json_response import DetailResponse, ErrorResponse, SuccessResponse

logger = logging.getLogger(__name__)


class multipleFileUpload(APIView):
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    @swagger_auto_schema(
        operation_summary="导入数据集",
        manual_parameters=[
            openapi.Parameter(
                name="zfile",
                in_=openapi.IN_FORM,
                required=True,
                type=openapi.TYPE_FILE,
                description="zip文件",
            ),
        ],
        consumes=["multipart/form-data"],  # 指定请求体的内容类型为 multipart/form-data
    )
    def post(self, request):
        try:
            zfile = request.FILES.get("zfile")
            print(f"@sting {len(zfile)}")

            flag, msg = port_wrapper.import_dataset(zfile)
            if flag:
                return SuccessResponse(msg=msg)
            else:
                return ErrorResponse(msg=msg)
        except Exception as e:
            print(f"ERROR {e}")
            traceback.print_exc()
            return ErrorResponse({"res": "error"})
