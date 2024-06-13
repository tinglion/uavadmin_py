import json
import logging
import os
import re
import traceback

import requests

from appuav.settings import AI_CONF
from uavadmin.dataset.models import DsDataset, DsImage, DsModel, DsModelExec, DsPatient
from uavadmin.dataset.module import dataset_wrapper

logger = logging.getLogger(__name__)
threshold_check_none = 1


def check_dataset(model_task: DsModelExec):
    try:
        model = DsModel.objects.get(id=model_task.model_id)
        if not model:
            return False, "no model"
        dataset_in = DsDataset.objects.get(id=model_task.dataset_id)
        if not dataset_in:
            return False, "no dataset"

        requires_in = split_require(model.in_require)

        patient_list = DsPatient.objects.filter(dataset_id=dataset_in.id)
        for index, r in enumerate(requires_in):
            if model.api_level == "patient":
                # patient层执行
                n_none = 0
                if r[0] == "ds_patient":
                    if r[1] == "ds_image":
                        for patient in patient_list:
                            image_list = DsImage.objects.filter(patient_id=patient.id)
                            for image in image_list:
                                if not getattr(image, r[2]):
                                    n_none += 1
                            if n_none >= threshold_check_none:
                                return False, f"患者图片参数缺值{r} image={image.id}"
                    elif r[0] == "ds_patient":
                        for patient in patient_list:
                            if not get_attr_str(patient, r[1]):
                                n_none += 1
                            if n_none >= threshold_check_none:
                                return False, f"患者参数缺值{r} patient={patient.id}"
                    else:
                        return False, f"格式错误{r} "
                elif len(r) == 1:
                    logger.info(f"using const={r[0]}")
                else:
                    return False, f"格式错误{r} "
            elif model.api_level == "image":
                # image 层
                n_none = 0
                if r[0] == "ds_patient":
                    for patient in patient_list:
                        if not getattr(patient, r[1]):
                            n_none += 1
                        if n_none >= threshold_check_none:
                            return False, f"患者参数缺值{r} patient={patient.id}"
                elif r[0] == "ds_image":
                    for patient in patient_list:
                        image_list = DsImage.objects.filter(patient_id=patient.id)
                        for image in image_list:
                            if not getattr(image, r[1]):
                                n_none += 1
                        if n_none >= threshold_check_none:
                            return False, f"图片参数缺值{r} image={image.id}"
                elif len(r) == 1:
                    logger.info(f"using const={r[0]}")
                else:
                    return False, f"格式错误{r} "
            else:
                return False, "api_level error"
        return True, ""
    except Exception as e:
        logger.error(f"ERROR {model_task.id} {e}")
        traceback.print_exc()
    return False, "error"


def exec_model(model_task: DsModelExec):
    n_patient = 0
    n_image = 0
    try:
        model = DsModel.objects.get(id=model_task.model_id)
        if not model:
            return 2, "no model"
        dataset_in = DsDataset.objects.get(id=model_task.dataset_id)
        if not dataset_in:
            return 2, "no dataset"

        dataset_out = dataset_in
        if model_task.out_type == "new":
            dataset_out = dataset_wrapper.clone_dataset(dataset_in)
            if dataset_out:
                model_task.out_dataset_id = dataset_out.id

        #
        patient_list = DsPatient.objects.filter(dataset_id=dataset_in.id)
        for patient in patient_list:
            logger.info(f"try patient={patient.id}")
            patient_out = DsPatient.objects.get(
                dataset_id=dataset_out.id, uid=patient.uid
            )

            if model.api_level == "patient":
                # patient层执行
                if exec_patient(model, patient, patient_out):
                    n_patient += 1
            else:
                # image层执行
                image_list = DsImage.objects.filter(patient_id=patient.id)
                for image in image_list:
                    if model.api_level == "image":
                        logger.info(f"try image={image.id}")
                        image_out = DsImage.objects.get(
                            patient_id=patient_out.id, url_origin=image.url_origin
                        )
                        if exec_image(
                            model,
                            image_in=image,
                            image_out=image_out,
                            patient_in=patient,
                        ):
                            n_image += 1
        msg = f"SUCC n_patient={n_patient} n_image={n_image}"
        logger.info(msg)
        return 1, msg
    except Exception as e:
        logger.info(f"ERROR {model_task.id} {e}")
    return 2, "error"


def exec_patient(model, patient_in, patient_out):
    data_json = "{}"
    try:
        url = model.api
        if url.find("http") != 0:
            url = f"{AI_CONF['url_lc_prefix']}{url}"
        logger.info(f"try api={url}")
        image_list = DsImage.objects.filter(patient_id=patient_in.id)

        requires_in = split_require(model.in_require)
        data = []
        for r in requires_in:
            if r[0] == "ds_patient":
                if r[1] == "ds_image":
                    data_tmp = []
                    for image in image_list:
                        data_tmp.append(getattr(image, r[2]))
                    data.append(json.dumps(data_tmp, ensure_ascii=False))
                else:
                    data.append(get_attr_str(image, r[1]))
            elif len(r) == 1:
                # 指定常量
                data.append(r[0])
        data_json = "{" + model.api_data.format(*data) + "}"
        # data_json = data_json.replace("'", '"')

        # logger.info(f"try {data_json}")
        response = requests.post(url, json=json.loads(data_json, strict=False))
        # logger.info(f"{response.text}")
        if response.status_code != 200:
            return False

        # parse result
        data_out = response.json()["data"]
        logger.info(data_out)
        requires_out = split_require(model.out_require)
        for r in requires_out:
            if r[0] == "ds_patient":
                if r[1] == "ds_image":
                    logger.info("todo")
                else:
                    setattr(patient_out, r[1], data_out[r[1]])

        patient_out.save()
        return True
    except Exception as e:
        logger.info(f"ERROR patient={patient_in.id} model={model.id} json={data_json}")
        traceback.print_exc()
    return False


def get_attr_str(obj, name):
    attr = getattr(obj, name)
    if isinstance(attr, list) or isinstance(attr, dict):
        attr = json.dumps(attr, ensure_ascii=False)
    elif isinstance(attr, str):
        attr = attr.replace("\\", "\\\\").replace("\n", "\\n")
    return attr


def exec_image(model, image_in, image_out, patient_in=None):
    try:
        url = model.api
        if url.find("http") != 0:
            url = f"{AI_CONF['url_lc_prefix']}{url}"
        logger.info(f"try api={url}")

        # prepare data
        data = []
        requires_in = split_require(model.in_require)
        for r in requires_in:
            if r[0] == "ds_patient":
                data.append(getattr(patient_in, r[1]))
            elif r[0] == "ds_image":
                s = get_attr_str(image_in, r[1])
                # 转义json字符
                if isinstance(s, str) and r[1] != "ocr_raw":
                    s = s.replace('"', '\\"')
                data.append(s)
            elif len(r) == 1:
                # 指定常量
                data.append(r[0])
        data_json = "{" + model.api_data.format(*data) + "}"

        # logger.info(f"{data_json}")
        data_obj = json.loads(data_json, strict=False)
        response = requests.post(url, json=data_obj)
        # logger.info(f"{response.text}")
        if response.status_code != 200:
            return False

        # parse result
        data_out = response.json()["data"]
        logger.info(data_out)
        requires_out = split_require(model.out_require)
        for r in requires_out:
            if r[0] == "ds_image":
                logger.info(r)
                setattr(image_out, r[1], data_out[r[1]])

        image_out.save()
        return True
    except Exception as e:
        logger.info(f"ERROR image={image_in.id} model={model.id} data={data_json}")
        traceback.print_exc()
    return False


def split_require(s: str):
    ret = []
    segs = s.split(",")
    for seg in segs:
        subs = seg.split(".")
        if len(subs) >= 1:
            ret.append([s.strip() for s in subs])
    return ret
