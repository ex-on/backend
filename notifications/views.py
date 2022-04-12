from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from community.models import Post, Qna
from core.utils.transformers import timeCalculator
from rest_framework import status
from rest_framework.response import Response
import json

from notifications.models import Notification
from notifications.serializers import NotificationSerializer

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
