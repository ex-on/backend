import datetime
from itertools import chain
import random
from turtle import title
from urllib import response
from firebase_admin import messaging
from exercise.models import ExercisePlanCardio, ExercisePlanWeight
from notifications.models import Notification
from stats.models import DailyExerciseStats

from users.models import UserDetailsCount, UserDetailsStatic


def send_fcm(uuid, title, body):
    staticData = UserDetailsStatic.objects.get(user_id=uuid)
    registration_token = staticData.fcm_token

    if registration_token:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=registration_token,
        )

        response = messaging.send(message)
        print('Successfully sent message:', response)


def hot_post_fcm(uuid, postId):
    title = '⚡️50 프로틴 획득'
    body = '게시물이 HOT 게시물로 선정되었어요'

    notification = Notification(user_id=uuid, title=title, body=body, type=2, link_id=postId)
    notification.save()

    countData = UserDetailsCount.objects.get(user_id=uuid)
    countData.count_protein += 50
    countData.save()
    
    send_fcm(uuid, title, body)


def hot_qna_fcm(uuid, qnaId):
    title = '⚡️50 프로틴 획득'
    body = '게시물이 HOT Q&A로 선정되었어요'

    notification = Notification(user_id=uuid, title=title, body=body, type=3, link_id=qnaId)
    notification.save()

    countData = UserDetailsCount.objects.get(user_id=uuid)
    countData.count_protein += 50
    countData.save()

    send_fcm(uuid, title, body)


def qna_selected_answer_fcm(uuid, qnaId):
    title = '⚡️30 프로틴 획득'
    body = 'Q&A 답변이 질문자에게 채택되었어요'

    notification = Notification(user_id=uuid, title=title, body=body, type=3, link_id=qnaId)
    notification.save()

    countData = UserDetailsCount.objects.get(user_id=uuid)
    countData.count_protein += 30
    countData.save()
    
    send_fcm(uuid, title, body)


def qna_best_answer_fcm(uuid, qnaId):
    title = '⚡️20 프로틴 획득'
    body = 'Q&A 답변이 인기 답변으로 선택되었어요'
    
    notification = Notification(user_id=uuid, title=title, body=body, type=3, link_id=qnaId)
    notification.save()

    countData = UserDetailsCount.objects.get(user_id=uuid)
    countData.count_protein += 20
    countData.save()

    send_fcm(uuid, title, body)



def exercise_attendance_fcm(uuid):
    title = '⚡️5 프로틴 획득'
    body = random.choice(['오늘의 첫 운동을 완료하셨어요',
                          '운동하는 첫 번째 발걸음이 가볍네요~',
                          '상쾌한 운동 시작 🥗',
                          ])

    notification = Notification(user_id=uuid, title=title, body=body, type=1)
    notification.save()

    countData = UserDetailsCount.objects.get(user_id=uuid)
    countData.count_protein += 5
    countData.save()

    send_fcm(uuid, title, body)


def daily_exercise_complete_fcm(uuid):
    # yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday = datetime.datetime.now()
    exercisePlans = chain(ExercisePlanCardio.objects.values('user_id','date', 'completed').filter(date=yesterday.date(), user_id=uuid), ExercisePlanWeight.objects.values('user_id', 'date', 'completed').filter(date=yesterday.date(), user_id=uuid))

    if sum(1 for e in exercisePlans) > 0:
        if all(plan.completed for plan in exercisePlans):
            title = '⚡️10 프로틴 획득'
            body = random.choice([
                '오늘도 운동 완료!! 짝짝 대단해요',
                '오늘의 운동 끝! 오늘 하루도 고생하셨어요',
                '오늘도 운동 끝! 내일도 화이팅!',
                '운동 완료! 휴..칼로리 불태웠다..🔥',
            ])

            notification = Notification(user_id=uuid, title=title, body=body, type=1)
            notification.save()

            countData = UserDetailsCount.objects.get(user_id=uuid)
            countData.count_protein += 10
            countData.save()

            send_fcm(uuid, title, body)


def weekly_exercise_protein_fcm(uuid):
    today = datetime.datetime.now()
    start = today - datetime.timedelta(days=today.weekday())
    end = start + datetime.timedelta(days=6)
    days = DailyExerciseStats.objects.filter(day__range=(start,end)).count()

    if days > 0:
        title = '⚡️' + str(days * 10) + ' 프로틴 획득'
        body = '지난주에 ' + str(days) + '일 운동하셨네요! 이번주도 힘내봅시다🔥'

        notification = Notification(user_id=uuid, title=title, body=body, type=1)
        notification.save()

        countData = UserDetailsCount.objects.get(user_id=uuid)
        countData.count_protein += days*10
        countData.save()

        send_fcm(uuid, title, body)

