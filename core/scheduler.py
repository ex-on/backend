import logging
import datetime
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django_apscheduler.models import DjangoJobExecution
from apscheduler.schedulers.background import BackgroundScheduler
import sys

from exercise.models import ExercisePlanCardio, ExercisePlanWeight
from notifications.fcm_notification import daily_exercise_complete_fcm, weekly_exercise_protein_fcm
from users.models import User

from django.conf import settings

scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG)

# This is the function you want to schedule - add as many as you want and then register them in the start() function below


def evaluate_exercise_status():
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    # exercisePlans = chain(ExercisePlanCardio.objects.values('user_id', 'date', 'completed').filter(date=yesterday.date()), ExercisePlanWeight.objects.values('user_id', 'date', 'completed').filter(date=yesterday.date()))
    # users = defaultdict(list)
    # for plan in exercisePlans:
    #   users[plan['user_id']].append(plan['completed'])
    # for user, statusList in users:
    #   if all(status for status in statusList):
    users = User.objects.values('uuid').all()
    for user in users:
        daily_exercise_complete_fcm(user['uuid'])

    if yesterday.weekday == 6:
        for user in users:
            weekly_exercise_protein_fcm(user['uuid'])


def start():
    if settings.DEBUG:
        # Hook into the apscheduler logger
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    # run this job every day at 00:00
    # scheduler.add_job(evaluate_exercise_status, 'cron',
    #                   hour=0)
    scheduler.add_job(evaluate_exercise_status, 'cron',
                      hour=0, id="evaluate_exercise_status", replace_existing=True)
    register_events(scheduler)
    scheduler.start()
    print("Scheduler started...", file=sys.stdout)
