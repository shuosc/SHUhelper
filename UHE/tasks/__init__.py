# 创建任务
from UHE.extensions import celery


@celery.task(name='printy',expires=10)
def printy():
    print("hahahahaha")


# def create_task(name, task, task_args, crontab_time):
#     '''
#     name # 任务名字
#     task # 执行的任务 "myapp.tasks.add"
#     task_args # 任务参数 {"x":1, "Y":1}

#     crontab_time # 定时任务时间 格式：
#     {
#         'month_of_year': 9 # 月份
#         'day_of_month': 5 # 日期
#         'hour': 01 # 小时
#         'minute':05 # 分钟
#     }
#     '''

#     # task任务， created是否定时创建
#     task, created = celery_models.PeriodicTask.objects.get_or_create(
#         name=name, task=task)
#     # 获取 crontab
#     crontab = celery_models.CrontabSchedule.objects.filter(
#         **crontab_time).first()
#     if crontab is None:
#         # 如果没有就创建，有的话就继续复用之前的crontab
#         crontab = celery_models.CrontabSchedule.objects.create(**crontab_time)
#     task.crontab = crontab  # 设置crontab
#     task.enabled = True  # 开启task
#     task.kwargs = json.dumps(task_args)  # 传入task参数
#     expiration = timezone.now() + datetime.timedelta(day=1)
#     task.expires = expiration  # 设置任务过期时间为现在时间的一天以后
#     task.save()
#     return True


# def disable_task(name):


# '''
# 关闭任务
# '''
#     try:
#         task = celery_models.PeriodicTask.objects.get(name=name)
#         task.enabled = False  # 设置关闭
#         task.save()
#         return True
#     except celery_models.PeriodicTask.DoesNotExist:
#         return True
