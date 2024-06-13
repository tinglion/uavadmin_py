import hashlib
import os

from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models

from appuav import dispatch
from uavadmin.utils.models import CoreModel, get_custom_app_models, table_prefix


class TaskLog(CoreModel):
    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id")

    src_name = models.CharField(max_length=255, verbose_name="来源表名", null=True)
    src_id = models.IntegerField(verbose_name="来源表ID", null=True)
    task_logo = models.CharField(max_length=255, verbose_name="长时间任务标识")
    # task_logo = models.TextField(verbose_name="", null=True)

    celery_id = models.CharField(max_length=255, verbose_name="med.id", unique=True)
    status = models.IntegerField(
        verbose_name="状态",
        default=0,
        help_text="task.status（0.队列中未执行；1.执行中；2.执行成功；3.执行失败；）",
    )
    task_msg = models.TextField(verbose_name="长时间任务返回信息", null=True)

    class Meta:
        db_table = "task_log"
        verbose_name = "长时间任务记录"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)  # 注意这里的逗号
        app_label = "utils"

    def __str__(self):
        return f"{self.src_name}_{self.src_id}"
