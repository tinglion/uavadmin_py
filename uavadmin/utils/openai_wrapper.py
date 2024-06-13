import logging
import os
import re
import sys

from openai import OpenAI

from appuav.settings import OPENAI_CONF
from uavadmin.utils.TokenAndCost import TokenCalculate

logger = logging.getLogger(__name__)


def chat_complete(q: str):
    client = OpenAI(
        base_url=OPENAI_CONF["OPENAI_API_BASE"],
        api_key=OPENAI_CONF["OPENAI_API_KEY"],
    )
    completion = client.chat.completions.create(
        model=OPENAI_CONF["GPT_MODEL"],
        messages=[
            {
                "role": "system",
                "content": "你是一个医学专家，根据提供的内容提取重要信息，并且不能修改原文",
            },
            {"role": "user", "content": q},
        ],
    )
    logger.info(f"模型返回结果:^{completion.choices[0].message}$")
    segs = completion.choices[0].message.content.split("output:")
    return segs[-1].strip()
