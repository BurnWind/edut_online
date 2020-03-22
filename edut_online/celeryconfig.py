__author__ = 'wzy'
__date__ = '2020/3/18 20:02'

from datetime import timedelta

import djcelery

djcelery.setup_loader()
CELERY_IMPORTS=(
    "apps.util.email_send",
)

CELERY_QUEUES = {
    'beat_tasks':{
        'exchange' : 'beat_tasks',
        'exchange_type' : 'direct',
        'binding_key' : 'beat_tasks'
    },
    'work_queue':{
        'exchange' : 'work_queue',
        'exchange_type' : 'direct',
        'binding_key' : 'work_queue'
    }
}

CELERY_DEFAULT_QUEUE = 'work_queue'


# 有些情况可以防止死锁
CELERYD_FORCE_EXECV=True
# 设置并发worker数量
CELERYD_CONCURRENCY=4
#允许重试
CELERY_ACKS_LATE=False
# 每个worker最多执行100个任务被销毁，可以防止内存泄漏
CELERYD_MAX_TASKS_PER_CHILD=100
# 单个任务最大执行时间
CELERYD_TASK_TIME_LIMIT=12*30


CELERYBEAT_SCHEDULE = {
    'task1' : {
        'task' : 'send_email',
        'schedule' : timedelta(seconds=10),
        'args': ('18826138192@163.com',),
        'options' : {
            'queue' : 'beat_tasks'
        }
    }
}
