import json
import traceback

import requests
from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import parsers, renderers, serializers, status
from rest_framework.decorators import action, api_view, parser_classes
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from appuav.settings import AI_CONF
from uavadmin.utils.json_response import DetailResponse, ErrorResponse, SuccessResponse

allow_path = [
    "/ss/slot/domains",
    "/prompt/queryCategoryUnits",
]


#
class dispatchView(APIView):

    @swagger_auto_schema(
        operation_summary="转发接口",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["path", "data"],
            properties={
                "path": openapi.Schema(
                    description="原接口相对路径",
                    type=openapi.TYPE_STRING,
                ),
                "data": openapi.Schema(
                    description="原接口post json参数",
                    type=openapi.TYPE_OBJECT,
                ),
            },
        ),
    )
    def post(self, request):
        """
        /ss/slot/domains
        /prompt/queryCategoryUnits
        """
        try:
            path = request.data.get("path")
            if path not in allow_path:
                return ErrorResponse(msg="not allowed")
            data = request.data.get("data")

            response = requests.post(f"{AI_CONF['url_lc_prefix']}{path}", data=data)
            print(f"@sting {response.text}")

            return SuccessResponse(data=response.json())
        except Exception as e:
            print(f"ERROR {e}")
            traceback.print_exc()
            return ErrorResponse(msg="error")
