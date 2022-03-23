from itertools import chain
from django.http.response import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from exercise.models import ExercisePlanCardio, ExercisePlanWeight, ExerciseRecordCardio, ExerciseRecordWeight
from exon_backend.settings import COGNITO_POOL_DOMAIN, COGNITO_AWS_REGION
from stats.models import DailyExerciseStats, PhysicalDataRecord
from .models import *
import json
import datetime
import requests
from core.utils.jwt import cognito_jwt_decode_handler
from stats.constants import getStandardBmi, getStandardBodyFatPercentage


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def checkAvailableEmail(request):
    email = request.GET['email']
    isEmailAvailable = not User.objects.filter(email=email).exists()
    return Response(isEmailAvailable)


@api_view(['GET'])
@permission_classes([])
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
        userInfoExists = (user.username is not None) and (
            userDetailsStatic.birth_date is not None) and (userDetailsStatic.gender is not None)
    else:
        userInfoExists = False
    return Response(userInfoExists)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserInfo(request):
    uuid = request.user.uuid
    userInfo = {}
    if not UserDetailsStatic.objects.filter(user_id=uuid).exists():
        return Response(status=status.HTTP_303_SEE_OTHER)
    else:
        if User.objects.filter(uuid=uuid):
            userInfo = {
                'username': User.objects.get(uuid=uuid).username,
                'activity_level': UserDetailsStatic.objects.get(user_id=uuid).activity_level,
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

    userDetailsCount = UserDetailsCount(user_id=uuid)

    user.save()
    userDetailsStatic.save()
    userDetailsCount.save()

    return HttpResponse(status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cognitoUserPhysicalInfo(request):
    uuid = request.user.uuid
    data = json.loads(request.body)

    height = float(data['height']) / 100
    weight = float(data['weight'])
    muscleMass = float(data['muscle_mass']) if data['muscle_mass'] is not None else None
    bodyFatPercentage = float(data['body_fat_percentage']) if data['body_fat_percentage'] is not None else None

    userDetailsStatic = UserDetailsStatic.objects.get(user_id=uuid)
    userDetailsStatic.height = float(data['height'])
    userDetailsStatic.save()

    gender = UserDetailsStatic.objects.get(user_id=uuid).gender

    bmi = weight / height ** 2
    standardWeight = (height ** 2) * getStandardBmi(gender)
    if bodyFatPercentage:
        inbodyScore = 80 - (standardWeight * (100 - getStandardBodyFatPercentage(gender))/100 - weight * (
            100 - bodyFatPercentage)/100) + (standardWeight * getStandardBodyFatPercentage(gender)/100 - weight * bodyFatPercentage/100)
    else:
        inbodyScore = None

    physicalDataRecord = PhysicalDataRecord(
        user_id=uuid, weight=weight, muscle_mass=muscleMass, body_fat_percentage=bodyFatPercentage, bmi=bmi, inbody_score=inbodyScore)
    physicalDataRecord.save()

    return HttpResponse(status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profileStats(request):
    uuid = request.user.uuid
    staticData = UserDetailsStatic.objects.get(user_id=uuid)
    countData = UserDetailsCount.objects.get(user_id=uuid)
    monthlyExerciseData, communityData, physicalData = ({} for i in range(3))
    exercisePlans = chain(ExercisePlanWeight.objects.filter(
        user_id=uuid), ExercisePlanCardio.objects.filter(user_id=uuid))

    for plan in exercisePlans:
        date = datetime.datetime.strftime(
            plan.date, '%Y-%m-%d')
        completed = plan.completed
        if date in monthlyExerciseData:
            if completed and monthlyExerciseData[date] == 1:
                monthlyExerciseData[date] = 2
            elif not completed and monthlyExerciseData[date] == 3:
                monthlyExerciseData[date] = 2
        else:
            if completed:
                monthlyExerciseData[date] = 3
            else:
                monthlyExerciseData[date] = 1

    if staticData.profile_community_privacy:
        communityData = {
            'privacy': True,
        }
    else:
        communityData = {
            'posts': countData.count_uploaded_posts,
            'qnas': countData.count_uploaded_qnas,
            'answers': countData.count_uploaded_answers,
            'accepted_answers': countData.count_accepted_answers,
            'acception_rate': countData.answer_acception_rate,
            'privacy': False,
        }

    if staticData.profile_physical_data_privacy:
        physicalData = {
            'privacy': True,
        }
    else:
        physicalDataRecord = PhysicalDataRecord.objects.filter(
            user_id=uuid).order_by('-created_at').first()

        physicalData = {
            'height': staticData.height,
            'weight': physicalDataRecord.weight,
            'muscle_mass': physicalDataRecord.muscle_mass,
            'body_fat_percentage': physicalDataRecord.body_fat_percentage,
            'bmi': physicalDataRecord.bmi,
            'inbody_score': physicalDataRecord.inbody_score,
            'privacy': False,
        }

    data = {
        'activity_level': {
            'level': staticData.activity_level,
            'protein': countData.count_protein,

        },
        'monthly_exercise': monthlyExerciseData,
        'community': communityData,
        'physical_data': physicalData,
    }

    return Response(data=data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rankProtein(request):
    uuid = request.user.uuid
    userStatic = UserDetailsStatic.objects.get(user_id=uuid)
    count = UserDetailsCount.objects.get(user_id=uuid)
    proteinRank = UserDetailsCount.objects.order_by('-count_protein')
    rankList = []
    rank = 0

    for e in proteinRank:
        static = UserDetailsStatic.objects.get(user_id=e.user_id)
        if e.user_id == uuid:
            rank = len(rankList) + 1
        rankList.append({
            'activity_level': static.activity_level,
            'username': User.objects.get(uuid=e.user_id).username,
            'protein': e.count_protein,
        })

    data = {
        'protein': count.count_protein,
        'rank': rank,
        'activity_level': userStatic.activity_level,
        'rank_list': rankList,
    }

    return Response(data=data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rankCardio(request):
    uuid = request.user.uuid
    month = request.GET['month']

    monthlyStats = DailyExerciseStats.objects.filter(day__month=month)
    userCalories = avgCalories = 0
    rankDict = {}
    rank = 0

    for stat in monthlyStats:
        if (stat.user_id == uuid):
            userCalories += stat.total_calories
        if stat.user_id in rankDict:
            rankDict[stat.user_id] += stat.total_calories
        else:
            rankDict[stat.user_id] = stat.total_calories

    rankList = sorted(rankDict.items(), key=lambda e: e[1], reverse=True)
    rankDictList = []

    for index, item in enumerate(rankList):
        if item[0] == uuid:
            rank = index + 1
        avgCalories += item[1] / len(rankList)
        rankDictList.append({
            'activity_level': UserDetailsStatic.objects.get(user_id=item[0]).activity_level,
            'username': User.objects.get(uuid=item[0]).username,
            'calories': item[1]
        })

    data = {
        'calories': userCalories,
        'avg_calories': avgCalories,
        'rank': rank,
        'rank_list': rankDictList,
    }

    return Response(data=data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rankWeight(request):
    uuid = request.user.uuid
    month = request.GET['month']

    monthlyStats = DailyExerciseStats.objects.filter(day__month=month)
    userVolume = avgVolume = 0
    rankDict = {}
    rank = 0

    for stat in monthlyStats:
        if (stat.user_id == uuid):
            userVolume += stat.total_volume
        if stat.user_id in rankDict:
            rankDict[stat.user_id] += stat.total_volume
        else:
            rankDict[stat.user_id] = stat.total_volume

    rankList = sorted(rankDict.items(), key=lambda e: e[1], reverse=True)
    rankDictList = []

    for index, item in enumerate(rankList):
        if item[0] == uuid:
            rank = index + 1
        avgVolume += item[1] / len(rankList)
        rankDictList.append({
            'activity_level': UserDetailsStatic.objects.get(user_id=item[0]).activity_level,
            'username': User.objects.get(uuid=item[0]).username,
            'volume': item[1]
        })

    data = {
        'volume': userVolume,
        'avg_volume': avgVolume,
        'rank': rank,
        'rank_list': rankDictList,
    }

    return Response(data=data)
