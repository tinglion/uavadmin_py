import json
import logging
import os
import sys

logger = logging.getLogger(__name__)

# 设置环境变量，指向您的 Django 项目目录
sys.path.append(".")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "appuav.settings")
# 初始化 Django
import django

django.setup()
from uavadmin.adverse.modules import load_wrapper


def test_load():
    fn = r"data/CTCAE5cn-v2.xlsx"
    load_wrapper.load_CTCAE5cn(fn)


#   2 中耳炎
#   2 多毛症
#   2 气管瘘
#   2 眩晕
#   2 脊髓炎
#   2 重症肌无力

if __name__ == "__main__":
    test_load()
