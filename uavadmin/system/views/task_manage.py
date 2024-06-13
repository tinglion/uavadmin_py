from rest_framework import status
from rest_framework.response import Response
# from rest_framework.viewsets import ModelViewSet
from uavadmin.system.model.task_model import TaskLog
from uavadmin.utils.serializers import CustomModelSerializer
from uavadmin.utils.viewset import CustomModelViewSet


class TaskManageSerializer(CustomModelSerializer):
    """
    不良反应库-序列化器
    """

    class Meta:
        model = TaskLog
        fields = "__all__"
        read_only_fields = ["id"]



class TaskManageViewset(CustomModelViewSet):
    """
    不良反应药品接口
    list: 查询
    create: 新增
    retrieve: 单例
    update: 修改
    destroy: 删除
    """

    queryset = TaskLog.objects.all()
    serializer_class = TaskManageSerializer

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
