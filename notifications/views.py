from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from community.models import Post, Qna
from core.utils.transformers import timeCalculator
from rest_framework import status
from rest_framework.response import Response
import json

from notifications.models import Notification, UserNotiReception
from notifications.serializers import NotificationSerializer
from core.utils.transformers import notificationFieldIntToStr
from users.models import User
# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notificationList(request):
    uuid = request.user.uuid
    startIndex = int(request.GET['start_index'])
    notifications = Notification.objects.filter(
        user_id=uuid).order_by('-created_at')
    notificationList = notifications[startIndex:startIndex + 20]
    listData = []

    for n in notificationList:
        n.created_at = timeCalculator(n.created_at)
        dict = NotificationSerializer(n).data
        if n.type == 2:
            dict['post_type'] = Post.objects.get(id=n.link_id).type
        elif n.type == 3:
            dict['qna_solved'] = Qna.objects.get(id=n.link_id).solved

        listData.append(dict)

    data = {
        'list': listData,
        'unread': notifications.filter(read=False).count()
    }

    return Response(data=data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def notificationRead(request):
    uuid = request.user.uuid
    data = json.loads(request.body)
    notification = Notification.objects.get(id=data['id'])
    notification.read = True
    notification.save()

    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deleteNotification(request):
    uuid = request.user.uuid
    data = json.loads(request.body)
    notification = Notification.objects.get(id=data['id'])
    notification.delete()

    return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def userNotiSettings(request):
    uuid = request.user.uuid
    notiSettings = UserNotiReception.objects.get(user_id=uuid)

    if request.method == 'POST':
        data = json.loads(request.body)
        toggleIndex = int(data['toggle_index'])
        val = data['value']
        if toggleIndex >= 0:
            setattr(notiSettings, notificationFieldIntToStr[toggleIndex], val)
        elif toggleIndex == -1:
            for index in range(8):
                setattr(notiSettings, notificationFieldIntToStr[index], val)
        elif toggleIndex == -2:
            for index in range(8, 10):
                setattr(notiSettings, notificationFieldIntToStr[index], val)
        elif toggleIndex == -3:
            for index in range(10, 13):
                setattr(notiSettings, notificationFieldIntToStr[index], val)

        notiSettings.save()

        return Response(status=status.HTTP_200_OK)

    else:
        returnData = []
        for index in range(14):
            returnData.append(
                getattr(notiSettings, notificationFieldIntToStr[index]))

        return Response(data=returnData)
