from django.http.response import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from exon_backend.settings import COGNITO_POOL_DOMAIN, COGNITO_AWS_REGION
from .models import *
import json
import datetime
import requests
from core.utils.jwt import cognito_jwt_decode_handler
# Create your views here.


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def checkAvailableEmail(request):
    email = request.GET['email']
    isEmailAvailable = not User.objects.filter(email=email).exists()
    return Response(isEmailAvailable)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def checkAvailableUsername(request):
    username = request.GET['username']
    isUsernameAvailable = not User.objects.filter(username=username).exists()
    return Response(isUsernameAvailable)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def checkUserInfo(request):
    uuid = request.user.uuid
    user = User.objects.get(uuid=uuid)
    if (UserDetailsStatic.objects.filter(user_id=uuid).exists()):
        userDetailsStatic = UserDetailsStatic.objects.get(user_id=uuid)
        userInfoExists = (user.username is not None) & (userDetailsStatic.birth_date is not None) & (userDetailsStatic.gender is not None)
    else:
        userInfoExists = False
    return Response(userInfoExists)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserInfo(request):
    uuid = request.user.uuid
    userInfo = {
        'username': User.objects.get(uuid=uuid).username,
        'profile_icon': UserDetailsStatic.objects.get(user_id=uuid).profile_icon,
        'created_at': User.objects.get(uuid=uuid).created_at
    }
    return Response(userInfo)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def registerCognitoUserInfo(request):
    uuid = request.user.uuid
    data = json.loads(request.body)
    auth_provider = data['auth_provider']
    birth_date = datetime.datetime.strptime(data['birth_date'], '%Y-%m-%d')
    gender = data['gender']
    username = data['username']
    user = User.objects.get(uuid=uuid)
    print(request.META)

    if auth_provider == 'Social':
        endpoint = f"https://{COGNITO_POOL_DOMAIN}.auth.{COGNITO_AWS_REGION}.amazoncognito.com/oauth2/userInfo"
        userInfo = requests.get(
            endpoint, headers={'Authorization': 'Bearer ' + str(request.auth)})
        print(json.loads(userInfo.content))
        email = json.loads(userInfo.content)['email']
    elif auth_provider == 'Kakao':
        email = data['email']
        user.email = email
    else:
        email = data['email']
        phone_number = data['phone_number']
        user.phone_number = phone_number

    user.email = email
    user.username = username

    if UserDetailsStatic.objects.filter(user_id=uuid).exists():
        userDetailsStatic = UserDetailsStatic.objects.get(user_id=uuid)
        userDetailsStatic.birth_date = birth_date
        userDetailsStatic.gender = gender
    else:
        userDetailsStatic = UserDetailsStatic(
            user_id=uuid, birth_date=birth_date, gender=gender)

    user.save()
    userDetailsStatic.save()

    return HttpResponse(status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cognitoUserPhysicalInfo(request):
    uuid = request.user.uuid
    data = json.loads(request.body)
    height = data['height']
    weight = data['weight']
    muscleMass = data['muscle_mass']
    bodyFatPercentage = data['body_fat_percentage']
    userPhysicalData = UserPhysicalData(
        user_id=uuid, height=height, weight=weight, muscle_mass=muscleMass, body_fat_percentage=bodyFatPercentage)
    userPhysicalData.save()

    return HttpResponse(status=status.HTTP_201_CREATED)
