import datetime
import os

from appuav.settings import BASE_DIR

# ================================================= #
# *************** mysql数据库 配置  *************** #
# ================================================= #
# 数据库 ENGINE ，默认演示使用 sqlite3 数据库，正式环境建议使用 mysql 数据库
# sqlite3 设置
# DATABASE_ENGINE = "django.db.backends.sqlite3"
# DATABASE_NAME = os.path.join(BASE_DIR, "db.sqlite3")

# 使用mysql时，改为此配置
DATABASE_ENGINE = "django.db.backends.mysql"
DATABASE_NAME = "as_uav"  # mysql 时使用

# 数据库地址 改为自己数据库地址
DATABASE_HOST = "mysql_my"
# DATABASE_HOST = "127.0.0.1"
# # 数据库端口
DATABASE_PORT = 3306
# # 数据库用户名
DATABASE_USER = "root"
# # 数据库密码
DATABASE_PASSWORD = ""

# 表前缀
TABLE_PREFIX = "dv_"
# ================================================= #
# ******** redis配置，无redis 可不进行配置  ******** #
# ================================================= #
# REDIS_PASSWORD = ''
# REDIS_HOST = '127.0.0.1'
# REDIS_URL = f'redis://:{REDIS_PASSWORD or ""}@{REDIS_HOST}:6380'
# ================================================= #
# ****************** 功能 启停  ******************* #
# ================================================= #
DEBUG = True
# 启动登录详细概略获取(通过调用api获取ip详细地址。如果是内网，关闭即可)
ENABLE_LOGIN_ANALYSIS_LOG = True
# 登录接口 /api/token/ 是否需要验证码认证，用于测试，正式环境建议取消
LOGIN_NO_CAPTCHA_AUTH = True
# ================================================= #
# ****************** 其他 配置  ******************* #
# ================================================= #

ALLOWED_HOSTS = ["*"]
# 列权限中排除App应用
COLUMN_EXCLUDE_APPS = []

# DB
DB_CONF = {}

MQTT_CONF = dict(
    MQTT_BROKER_PUBLIC="123.56.127.200",
    MQTT_BROKER="10.19.53.207",
    MQTT_PORT=1883,
    MQTT_KEEPALIVE_INTERVAL=60,
    MQTT_TOPIC="asmote/drone/data/#",
    MQTT_USERNAME="asmote",  # MQTT用户名
    MQTT_PASSWORD="",  # MQTT密码
    CLIENT_ID_S="asmote_p_s",
    CLIENT_ID_R="asmote_p_r",
)


TEMP_DIR = "/tmp/uav"
