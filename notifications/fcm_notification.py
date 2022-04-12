import datetime
from itertools import chain
import random
from turtle import title
from urllib import response
from firebase_admin import messaging
from community.models import Post, PostComment, Qna, QnaAnswer
from exercise.models import ExercisePlanCardio, ExercisePlanWeight
from notifications.models import Notification
from stats.models import DailyExerciseStats
from core.utils.transformers import getLevelRequiredProtein, postTypeIntToStr, activityLevelIntToStr

from users.models import User, UserDetailsCount, UserDetailsStatic


def send_fcm(uuid, title, body, data=None):
    staticData = UserDetailsStatic.objects.get(user_id=uuid)
    registration_token = staticData.fcm_token

    if registration_token:
        if data:
            if data['type'] == '2':
                data['post_type'] = str(Post.objects.get(id=data['link_id']).type)
            elif data['type'] == '3':
              data['qna_solved'] = str(Qna.objects.get(id=data['link_id']).solved)

        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data={
                'type': '0',
            } if data == None else data,
            android=messaging.AndroidConfig(
                notification=messaging.AndroidNotification(
                    click_action="FCM_OPEN_ACTIVITY",
                ),
            ),
            apns=messaging.APNSConfig(
                headers={
                    "apns-priority": "5",
                },
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(
                        category="FCM_OPEN_CATEGORY",
                    ),
                ),
            ),
            token=registration_token,
        )

        response = messaging.send(message)
        print('Successfully sent message:', response)


def activity_level_up_fcm(uuid, addedProtein):
    staticData = UserDetailsStatic.objects.get(user_id=uuid)
    countData = UserDetailsCount.objects.get(user_id=uuid)

    if staticData.activity_level < 6:
        if 0 <= (countData.count_protein - getLevelRequiredProtein(staticData.activity_level+1)) < addedProtein:
            title = '🎉프로틴 등급 업🔥'
            body = '축하드려요!! ' + User.objects.get(uuid=uuid).username + '님은 이제 ' + \
                activityLevelIntToStr[staticData.activity_level+1] + ' 등급이에요!'

            staticData.activity_level += 1
            staticData.save()

            notification = Notification(
                user_id=uuid, title=title, body=body, type=4)
            notification.save()

            data = {
                'type': '4',
                'id': str(notification.id),
            }

            send_fcm(uuid, title, body, data)


def hot_post_fcm(uuid, postId):
    title = '⚡️50 프로틴 획득'
    body = '게시물이 HOT 게시물로 선정되었어요'

    notification = Notification(
        user_id=uuid, title=title, body=body, type=2, link_id=postId)
    notification.save()

    countData = UserDetailsCount.objects.get(user_id=uuid)
    countData.count_protein += 50
    countData.save()

    data = {
        'type': '2',
        'id': str(notification.id),
        'link_id': str(postId),
    }

    activity_level_up_fcm(uuid, 50)

    send_fcm(uuid, title, body, data)


def hot_qna_fcm(uuid, qnaId):
    title = '⚡️50 프로틴 획득'
    body = '게시물이 HOT Q&A로 선정되었어요'

    notification = Notification(
        user_id=uuid, title=title, body=body, type=3, link_id=qnaId)
    notification.save()

    countData = UserDetailsCount.objects.get(user_id=uuid)
    countData.count_protein += 50
    countData.save()

    data = {
        'type': '3',
        'id': str(notification.id),
        'link_id': str(qnaId),
    }

    activity_level_up_fcm(uuid, 50)

    send_fcm(uuid, title, body, data)


def qna_selected_answer_fcm(userId, qnaId):
    title = '⚡️30 프로틴 획득'
    body = 'Q&A 답변이 질문자에게 채택되었어요'

    notification = Notification(
        user_id=userId, title=title, body=body, type=3, link_id=qnaId)
    notification.save()

    countData = UserDetailsCount.objects.get(user_id=userId)
    countData.count_protein += 30
    countData.save()

    data = {
        'type': '3',
        'id': str(notification.id),
        'link_id': str(qnaId),
    }

    activity_level_up_fcm(userId, 30)

    send_fcm(userId, title, body, data)


def qna_best_answer_fcm(userId, qnaId):
    title = '⚡️20 프로틴 획득'
    body = 'Q&A 답변이 인기 답변으로 선택되었어요'

    notification = Notification(
        user_id=userId, title=title, body=body, type=3, link_id=qnaId)
    notification.save()

    countData = UserDetailsCount.objects.get(user_id=userId)
    countData.count_protein += 20
    countData.save()

    data = {
        'type': '3',
        'id': str(notification.id),
        'link_id': str(qnaId),
    }

    activity_level_up_fcm(userId, 20)

    send_fcm(userId, title, body, data)


def post_comment_fcm(uuid, postId, comment):
    post = Post.objects.get(id=postId)
    if uuid != post.user_id:
        title = '[' + postTypeIntToStr[post.type] + '게시판]' + '\n새로운 댓글이 달렸어요'
        body = (comment[:20] + '..') if len(comment) > 20 else comment
        notification = Notification(
            user_id=post.user_id, title=title, body=body, type=2, link_id=postId)
        notification.save()

        data = {
            'type': '2',
            'id': str(notification.id),
            'link_id': str(postId),
        }

        send_fcm(post.user_id, title, body, data)


def post_reply_fcm(uuid, postId, postCommentId, reply):
    post = Post.objects.get(id=postId)
    postComment = PostComment.objects.get(id=postCommentId)
    title = '[' + postTypeIntToStr[post.type] + '게시판]' + '\n새로운 대댓글이 달렸어요'
    body = (reply[:20] + '..') if len(reply) > 20 else reply

    if uuid != postComment.user_id:
        commentNotification = Notification(
            user_id=postComment.user_id, title=title, body=body, type=2, link_id=postId)
        commentNotification.save()

        data = {
            'type': '2',
            'id': str(commentNotification.id),
            'link_id': str(postId),
        }

        send_fcm(postComment.user_id, title, body, data)

    if uuid != post.user_id:
        postNotification = Notification(
            user_id=post.user_id, title=title, body=body, type=2, link_id=postId)
        postNotification.save()

        data = {
            'type': '2',
            'id': str(postNotification.id),
            'link_id': str(postId),
        }

        send_fcm(post.user_id, title, body, data)


def qna_answer_fcm(qnaId, answer):
    qna = Qna.objects.get(id=qnaId)

    title = '[Q&A]\n새로운 답변이 달렸어요'
    body = (answer[:20] + '..') if len(answer) > 20 else answer

    notification = Notification(
        user_id=qna.user_id, title=title, body=body, type=3, link_id=qnaId)
    notification.save()

    data = {
        'type': '3',
        'id': str(notification.id),
        'link_id': str(qnaId),
    }

    send_fcm(qna.user_id, title, body, data)


def qna_answer_comment_fcm(uuid, qnaId, qnaAnswerId, comment):
    qnaAnswer = QnaAnswer.objects.get(id=qnaAnswerId)

    title = '[Q&A]\n새로운 댓글이 달렸어요'
    body = (comment[:20] + '..') if len(comment) > 20 else comment

    if uuid != qnaAnswer.user_id:
        notification = Notification(
            user_id=qnaAnswer.user_id, title=title, body=body, type=3, link_id=qnaId)
        notification.save()

        data = {
            'type': '3',
            'id': str(notification.id),
            'link_id': str(qnaId),
        }

        send_fcm(qnaAnswer.user_id, title, body, data)


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

    data = {
        'type': '1',
    }

    activity_level_up_fcm(uuid, 5)

    send_fcm(uuid, title, body, data)


def daily_exercise_complete_fcm(uuid):
    # yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday = datetime.datetime.now()
    exercisePlans = chain(ExercisePlanCardio.objects.values('user_id', 'date', 'completed').filter(date=yesterday.date(
    ), user_id=uuid), ExercisePlanWeight.objects.values('user_id', 'date', 'completed').filter(date=yesterday.date(), user_id=uuid))

    if sum(1 for e in exercisePlans) > 0:
        if all(plan.completed for plan in exercisePlans):
            title = '⚡️10 프로틴 획득'
            body = random.choice([
                '오늘도 운동 완료!! 짝짝 대단해요',
                '오늘의 운동 끝! 오늘 하루도 고생하셨어요',
                '오늘도 운동 끝! 내일도 화이팅!',
                '운동 완료! 휴..칼로리 불태웠다..🔥',
            ])

            notification = Notification(
                user_id=uuid, title=title, body=body, type=1)
            notification.save()

            countData = UserDetailsCount.objects.get(user_id=uuid)
            countData.count_protein += 10
            countData.save()

            data = {
                'type': '1',
            }

            activity_level_up_fcm(uuid, 10)

            send_fcm(uuid, title, body, data)


def weekly_exercise_protein_fcm(uuid):
    today = datetime.datetime.now()
    start = today - datetime.timedelta(days=today.weekday())
    end = start + datetime.timedelta(days=6)
    days = DailyExerciseStats.objects.filter(day__range=(start, end)).count()

    if days > 0:
        title = '⚡️' + str(days * 10) + ' 프로틴 획득'
        body = '지난주에 ' + str(days) + '일 운동하셨네요! 이번주도 힘내봅시다🔥'

        notification = Notification(
            user_id=uuid, title=title, body=body, type=1)
        notification.save()

        countData = UserDetailsCount.objects.get(user_id=uuid)
        countData.count_protein += days*10
        countData.save()

        data = {
            'type': '1',
        }

        activity_level_up_fcm(uuid, days*10)

        send_fcm(uuid, title, body, data)
