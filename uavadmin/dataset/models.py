from datetime import datetime

from django.db import models

from appuav import dispatch
from uavadmin.utils.models import CoreModel, get_custom_app_models, table_prefix


class DsDataset(CoreModel):
    name = models.CharField(max_length=255, verbose_name="名称")
    stage = models.IntegerField(verbose_name="阶段", default=0, null=True)

    status = models.IntegerField(
        verbose_name="状态", default=0, help_text="[0default，3-已删除]"
    )

    class Meta:
        db_table = "ds_dataset"
        verbose_name = "数据集"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)
        app_label = "dataset"

    def __str__(self):
        return f"{self.name}"


class DsPatient(CoreModel):
    dataset_id = models.BigIntegerField(verbose_name="数据集ID")
    uid = models.CharField(max_length=255, verbose_name="唯一ID")

    disease_type = models.CharField(max_length=255, verbose_name="识别的疾病")
    crf_result = models.JSONField(default=None)
    crf_result_custom = models.JSONField(default=None)

    status = models.IntegerField(
        verbose_name="状态", default=0, help_text="[0default，3-已删除]"
    )

    class Meta:
        db_table = "ds_patient"
        verbose_name = "数据集患者"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)
        app_label = "dataset"

    def __str__(self):
        return f"{self.name}"


class DsImage(CoreModel):
    patient_id = models.BigIntegerField(verbose_name="患者ID")
    url = models.CharField(max_length=255, verbose_name="URL")
    url_origin = models.CharField(max_length=255, verbose_name="url_origin")

    url_desensitive = models.CharField(max_length=255, verbose_name="url_desensitive")
    scale_factor = models.FloatField(default=1)

    ocr_result = models.TextField(default=None, null=True, blank=True)
    ocr_raw = models.JSONField(default=None, null=True, blank=True)

    category = models.CharField(max_length=64, verbose_name="category")
    preprocess = models.TextField(default=None, null=True, blank=True)
    native_result = models.JSONField(default=None, null=True, blank=True)
    native_result_custom = models.JSONField(default=None, null=True, blank=True)
    pic_result = models.JSONField(default=None, null=True, blank=True)
    pic_result_custom = models.JSONField(default=None, null=True, blank=True)

    status = models.IntegerField(
        verbose_name="状态", default=0, help_text="[0default，3-已删除]"
    )

    class Meta:
        db_table = "ds_image"
        verbose_name = "数据集图片"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)

    def __str__(self):
        return f"{self.name}"


class DsModel(CoreModel):
    name = models.CharField(max_length=255, verbose_name="名称")

    api = models.CharField(max_length=255, verbose_name="API")
    api_data = models.TextField(verbose_name="API的post json格式，不包括最外侧大括号")
    api_level = models.CharField(
        max_length=64, verbose_name="api操作数据级别：image，patient"
    )

    in_stage = models.IntegerField(verbose_name="输入阶段")
    in_require = models.TextField(verbose_name="输入参数要求")

    out_stage = models.IntegerField(verbose_name="输出阶段")
    out_require = models.TextField(verbose_name="输出参数要求")

    status = models.IntegerField(
        verbose_name="状态", default=0, help_text="[0default，3-已删除]"
    )

    class Meta:
        db_table = "ds_model"
        verbose_name = "模型"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)
        app_label = "dataset"

    def __str__(self):
        return f"{self.name}"


class DsModelExec(CoreModel):
    model_id = models.BigIntegerField(verbose_name="model.id")
    dataset_id = models.BigIntegerField(verbose_name="dataset.id")
    out_dataset_id = models.BigIntegerField(verbose_name="null, as in", null=True)
    out_type = models.CharField(
        max_length=255,
        verbose_name="输出类型，默认原数据集，new新建数据集",
        default=None,
    )
    status_exec = models.IntegerField(
        verbose_name="执行状态：0,创建；1成功；2失败；10执行中"
    )
    exec_start_time = models.DateTimeField(default=None)
    exec_end_time = models.DateTimeField(default=None)

    status = models.IntegerField(
        verbose_name="状态", default=0, help_text="[0default，3-已删除]"
    )

    class Meta:
        db_table = "ds_model_exec"
        verbose_name = "模型执行记录"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)
        app_label = "dataset"

    def __str__(self):
        return f"{self.name}"
