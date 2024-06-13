## task: query，change，cron，cancel
from uavadmin.system.model import task_model
from uavadmin.system.modules import task_manager


# TODO add celery
def new_task(src_name, src_id, celery_id=None, params=dict(), is_async=False):
    return task_model.TaskLog.objects.create(
        src_name=src_name, src_id=src_id, celery_id=None
    )


def get_task(src_name, src_id):
    try:
        dlist = task_model.TaskLog.objects.filter(src_name=src_name, src_id=src_id)
        if len(dlist) > 0:
            return dlist[0]
    except Exception as e:
        logger.error(f"ERROR {e}")
    return None

def get_task(src_name, src_id):
    try:
        dlist = task_model.TaskLog.objects.filter(src_name=src_name, src_id=src_id)
        if len(dlist) > 0:
            return dlist[0]
    except Exception as e:
        logger.error(f"ERROR {e}")
    return None
