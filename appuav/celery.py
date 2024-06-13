import functools
import os
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "appuav.settings")

from celery import platforms
from django.conf import settings

# 租户模式
if "django_tenants" in settings.INSTALLED_APPS:
    from tenant_schemas_celery.app import CeleryApp as TenantAwareCeleryApp

    app = TenantAwareCeleryApp()
else:
    from celery import Celery

    app = Celery(f"appuav", broker=settings.CELERY_BROKER_URL)
app.config_from_object("django.conf:settings")
app.conf.result_backend = settings.CELERY_BROKER_URL
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
platforms.C_FORCE_ROOT = True


@app.task
def test_add(x, y):
    time.sleep(2)
    return x + y


def retry_base_task_error():
    """
    celery 失败重试装饰器
    :return:
    """

    def wraps(func):
        @app.task(bind=True, retry_delay=180, max_retries=3)
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                raise self.retry(exc=exc)

        return wrapper

    return wraps


# https://zhuanlan.zhihu.com/p/369639432?utm_id=0
