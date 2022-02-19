from itertools import chain
from django.http.response import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from exercise.models import ExercisePlanCardio, ExercisePlanWeight, ExerciseRecordCardio, ExerciseRecordWeight
from exon_backend.settings import COGNITO_POOL_DOMAIN, COGNITO_AWS_REGION
from stats.models import PhysicalDataRecord
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
        userInfoExists = (user.username is not None) & (
            userDetailsStatic.birth_date is not None) & (userDetailsStatic.gender is not None)
    else:
        userInfoExists = False
    return Response(userInfoExists)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserInfo(request):
    uuid = request.user.uuid
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
    height = data['height']
    weight = data['weight']
    muscleMass = data['muscle_mass']
    bodyFatPercentage = data['body_fat_percentage']
    userPhysicalData = PhysicalDataRecord(
        user_id=uuid, weight=weight, muscle_mass=muscleMass, body_fat_percentage=bodyFatPercentage)
    userPhysicalData.save()
    userDetailsStatic = UserDetailsStatic.objects.get(user_id=uuid)
    userDetailsStatic.height = height
    userDetailsStatic.save()

    return HttpResponse(status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfileStats(request):
    uuid = request.user.uuid

    staticData = UserDetailsStatic.objects.get(user_id=uuid)
    countData = UserDetailsCount.objects.get(user_id=uuid)
    monthlyExerciseData, communityData, physicalData = ({} for i in range(3))
    exercisePlans = chain(ExercisePlanWeight.objects.filter(
        user_id=uuid), ExercisePlanCardio.objects.filter(user_id=uuid))

    for plan in exercisePlans:
        if isinstance(plan, ExercisePlanWeight):
            date = datetime.datetime.strftime(
                plan.date, '%Y-%m-%d')
            record = ExerciseRecordWeight.objects.filter(
                exercise_plan_weight_id=plan.id)
            if date in monthlyExerciseData:
                if record.exists() and monthlyExerciseData[date] == 1:
                    monthlyExerciseData[date] = 2
            else:
                if record.exists():
                    monthlyExerciseData[date] = 3
                else:
                    monthlyExerciseData[date] = 1
        else:
            date = datetime.datetime.strftime(
                plan.date, '%Y-%m-%d')
            record = ExerciseRecordCardio.objects.filter(
                exercise_plan_cardio_id=plan.id)
            if date in monthlyExerciseData:
                if record.exists() and monthlyExerciseData[date] == 1:
                    monthlyExerciseData[date] = 2
            else:
                if record.exists():
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
