import json
import logging
import os
import re
import shutil
import sys
import time
import urllib.parse

import requests
from bs4 import BeautifulSoup

from appuav.settings import AI_CONF
from uavadmin.utils import file_utils, image_utils

from .consts import *

logger = logging.getLogger(__name__)

# 搜索页/详情页通用
# 说明书验证码限制
# 1. 说明书页：https://drugs.medlive.cn/drugref/drug_info.do?detailId=be9bf346e82ea2c2cfc10ca5108e70f0
# 2. 302 验证码页：https://drugs.medlive.cn/initCaptcha.do?orginUrl=https%3A%2F%2Fdrugs.medlive.cn%2Fdrugref%2Fdrug_info.do%3FdetailId%3Dbe9bf346e82ea2c2cfc10ca5108e70f0
# 3. get 验证码：https://drugs.medlive.cn/captchaAction.do
# 4. post 验证码：https://drugs.medlive.cn/validCaptcha.do orginUrl=https%3A%2F%2Fdrugs.medlive.cn%2Fdrugref%2Fdrug_info.do%3FdetailId%3Dbe9bf346e82ea2c2cfc10ca5108e70f0&captcha=9248
# 5. 跳 目说明书页


# return response/None
def crawl_drug_search(search_url, headers, retry=0):
    parsed_url = urllib.parse.urlparse(search_url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    orgin_url = query_params.get("orginUrl", [None])[0]
    logger.info(
        f"crawl_drug_search retry={retry} orginUrl={orgin_url} url={search_url} headers={headers}"
    )

    # 打开验证码页面
    response_captcha = requests.get(
        search_url, headers=headers, timeout=5, allow_redirects=False
    )
    # if response_captcha.status_code == 200:
    #     file_utils.write_bytes(response_captcha.content, fn=f"./temp/captcha.html")

    # 获得验证码
    response_captcha = requests.get(
        URL_MEDLIVE_DRUG_CAPTCHA, headers=headers, timeout=5, allow_redirects=False
    )
    if response_captcha.status_code == 200:
        # 识别验证码
        code = ocr_captcha(response_captcha.content, tmp_dir="/tmp/captcha")
        if code:
            # 提交验证码前需要等一下
            time.sleep(2)

            # 提交验证码
            url_valid = (
                f"{URL_MEDLIVE_DRUG_CAPTCHA_VALID}?orginUrl={orgin_url}&captcha={code}"
            )
            response_valid = requests.post(
                url_valid, headers=headers, allow_redirects=False
            )
            # file_utils.write_bytes(response_valid.content, fn=f"./temp/valid_res.html")
            logger.info(
                f"captcha_valid_response {response_valid.status_code} headers={response_valid.headers}"
            )
            if response_valid.status_code == 302:
                valid_location = response_valid.headers.get("Location", orgin_url)
                logger.info(f"valid_location {valid_location}")
                if not valid_location:
                    return None
                elif valid_location.find("initCaptcha.do") > 0:
                    # 有需要重复提交验证码的情况
                    return crawl_drug_search(
                        f"{URL_MEDLIVE_CONTENT_PREFIX}/{valid_location}",
                        headers=headers,
                        retry=retry + 1,
                    )
                else:
                    logger.info(f"captcha valid succ url_valid {url_valid}")
                    response = requests.get(valid_location, headers=headers)
                    logger.info(f"captcha valid valid_location {valid_location}")
                    logger.info(
                        f"captcha valid succ {response.status_code} {response.headers} {response.text}"
                    )
                    return response
            elif response_valid.status_code == 200:
                if retry >= URL_MEDLIVE_DRUG_CAPTCHA_RETRY:
                    return None
                # 验证码验证失败，再试一次
                return crawl_drug_search(search_url, headers=headers, retry=retry + 1)
    return None


def ocr_captcha(image_content, tmp_dir="./temp"):
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    randname = file_utils.getRandomStringByMode()

    fn_origin = f"{tmp_dir}/captcha_{randname}_origin.png"
    file_utils.write_bytes(image_content, fn=fn_origin)

    # 识别原因，需要放大
    fn_captcha = f"{tmp_dir}/captcha_{randname}.png"
    image_utils.resize_img(fn_src=fn_origin, fn_dst=fn_captcha, scale_factor=4)

    # 识别验证码
    # {
    #   "code": 200,
    #   "msg": "",
    #   "data": {
    #     "ocr_align": "  8926"
    #   }
    # }
    response_ocr = requests.post(
        f"{AI_CONF['ocr_local']}?ocr_engine=paddle&rtype=align_text",
        files={"infile": open(fn_captcha, "rb")},
    )
    os.remove(fn_origin)
    os.remove(fn_captcha)
    if response_ocr.status_code == 200:
        code = response_ocr.json()["data"]["ocr_align"].strip()
        logger.info(f"captcha code={code} fn={fn_captcha}")
        return code
    return None
