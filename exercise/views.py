from django.http.response import HttpResponse
from django.shortcuts import render
from django.utils import tree
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import datetime
import json

from .models import *
from .serializers import ExerciseDetailsSerializer, ExercisePlanAerobicSerializer, ExercisePlanWeightSerializer, ExercisePlanWeightSetSerializer, ExerciseRecordAerobicSerializer, ExerciseRecordWeightSerializer, ExerciseSerializer, ExerciseTimeSerializer, ExerciseRecordWeightSetSerializer
# Create your views here.

########### 운동 종류 및 세부 정보 조회 #############################
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllExercise(request):
    exerciseList = Exercise.objects.all()
    serializer = ExerciseSerializer(exerciseList, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getExerciseByTargetMuscle(request):
    _target_muscle = request.GET['target_muscle']
    exerciseList = Exercise.objects.filter(target_muscle=_target_muscle)
    serializer = ExerciseSerializer(exerciseList, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getExerciseByExerciseMethod(request):
    _exercise_method = request.GET['exercise_method']
    exerciseList = Exercise.objects.filter(exercise_method=_exercise_method)
    serializer = ExerciseSerializer(exerciseList, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getExerciseByTargetMuscleExerciseMethod(request):
    _target_muscle = request.GET['target_muscle']
    _exercise_method = request.GET['exercise_method']
    exerciseList = Exercise.objects.filter(
        target_muscle=_target_muscle, exercise_method=_exercise_method)
    serializer = ExerciseSerializer(exerciseList, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getExerciseDetails(request):
    _exercise_id = request.GET['exercise_id']
    details = ExerciseDetails.objects.filter(exercise_id=_exercise_id)
    serializer = ExerciseDetailsSerializer(details, many=True)
    return Response(serializer.data)

########### 운동 계획 조회 #############################
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getExercisePlanWeightDate(request):
    _user_id = request.user.uuid
    _date = request.GET['date']
    _date = datetime.datetime.strptime(_date, '%Y-%m-%d')
    plans = ExercisePlanWeight.objects.filter(user_id=_user_id, date=_date)
    resData = []
    for plan in plans:
        planData = ExercisePlanWeightSerializer(plan).data
        exerciseData = ExerciseSerializer(
            Exercise.objects.get(id=plan.exercise_id)).data
        data = {
            'exercise_data': exerciseData,
            'plan_data': planData,
        }
        resData.append(data)

    return Response(resData)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getExercisePlanWeightSets(request):
    _exercise_plan_weight_id = request.GET['exercise_plan_weight_id']
    sets = ExercisePlanWeightSet.objects.filter(
        exercise_plan_weight_id=_exercise_plan_weight_id)
    serializer = ExercisePlanWeightSetSerializer(sets, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getUserPlanAerobicDate(request):
    _user_id = request.GET['user_id']
    _date = request.GET['date']
    _date = datetime.datetime.strptime(_date, '%Y/%m/%d')
    plans = ExercisePlanAerobic.objects.filter(user_id=_user_id, date=_date)
    serializer = ExercisePlanAerobicSerializer(plans, many=True)
    return Response(serializer.data)

########### 운동 기록 조회 #############################
@api_view(['GET'])
def getUserRecordWeight(request):
    _user_id = request.GET['user_id']
    record = ExerciseRecordWeight.objects.filter(
        user_id=_user_id).order_by('-date')
    serializer = ExerciseRecordWeightSerializer(record, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getUserRecordWeightDate(request):
    _user_id = request.GET['user_id']
    _date = request.GET['date']
    _date = datetime.datetime.strptime(_date, '%Y/%m/%d')
    record = ExerciseRecordWeight.objects.filter(user_id=_user_id, date=_date)
    serializer = ExerciseRecordWeightSerializer(record, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getUserRecordWeightTargetMuscle(request):
    _user_id = request.GET['user_id']
    _target_muscle = request.GET['target_muscle']
    record = ExerciseRecordWeight.objects.filter(
        user_id=_user_id, target_muscle=_target_muscle).order_by('-date')
    serializer = ExerciseRecordWeightSerializer(record, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getUserRecordWeightSets(request):
    record_id = request.GET['exercise_record_weight_id']
    record_sets = ExerciseRecordWeightSet.objects.filter(
        exercise_record_weight=record_id)
    serializer = ExerciseRecordWeightSetSerializer(record_sets, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getUserRecordAerobic(request):
    _user_id = request.GET['user_id']
    record = ExerciseRecordAerobic.objects.filter(user_id=_user_id)
    serializer = ExerciseRecordAerobicSerializer(record, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getUserRecordAerobicDate(request):
    _user_id = request.GET['user_id']
    _date = request.GET['date']
    _date = datetime.datetime.strptime(_date, '%Y/%m/%d')
    record = ExerciseRecordAerobic.objects.filter(user_id=_user_id, date=_date)
    serializer = ExerciseRecordAerobicSerializer(record, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getExerciseTime(request):
    date = request.GET['date']
    userId = request.GET['user_id']
    parsedDate = datetime.datetime.strptime(date, '%Y/%m/%d')
    aerobic_record = ExerciseRecordAerobic.objects.filter(
        date=parsedDate, user_id=userId)
    weight_record = ExerciseRecordWeight.objects.filter(
        date=parsedDate, user_id=userId)
    duration = datetime.timedelta(hours=0, minutes=0, seconds=0)
    for record in aerobic_record:
        diff = record.end_time - record.start_time
        duration = duration + diff
    for record in weight_record:
        diff = record.end_time - record.start_time
        duration = duration + diff
    duration = {'duration': duration}
    serializer = ExerciseTimeSerializer(duration)
    return Response(serializer.data)

########## 운동 계획 및 기록 등록 ###########
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def postExercisePlanWeight(request):
    user_id = request.user.uuid
    request = json.loads(request.body)
    sets = request['sets']
    plan = ExercisePlanWeight(
        user_id=user_id, exercise_id=request['exercise_id'], num_sets=len(sets))
    plan.save()

    for set in sets:
        data = ExercisePlanWeightSet(exercise_plan_weight_id=plan.id,
                                     set_num=set['set_num'], target_weight=set['target_weight'], target_reps=set['target_reps'])
        data.save()
    return HttpResponse(status=200)


@api_view(['POST'])
def postExercisePlanAerobic(request):
    request = json.loads(request.body)
    record = ExercisePlanAerobic(user_id=request['user_id'], exercise_id=request['exercise_id'], date=request['date'],
                                 target_distance=request['target_distance'], target_duration=request['target_duration'])
    record.save()
    return HttpResponse(status=200)


@api_view(['POST'])
def postExerciseRecordWeight(request):
    request = json.loads(request.body)
    record = ExerciseRecordWeight(user_id=request['user_id'], exercise_plan_weight_id=request['exercise_plan_weight_id'],
                                  date=request['date'], exercise_id=request['exercise_id'], target_muscle=request['target_muscle'],
                                  total_sets=request['total_sets'], start_time=request['start_time'], end_time=request['end_time'])
    record.save()

    sets = request['sets']
    for set in sets:
        data = ExerciseRecordWeightSet(exercise_record_weight_id=record.id, record_weight=set['record_weight'],
                                       record_reps=set['record_reps'], start_time=set['start_time'],
                                       end_time=set['end_time'], set_num=set['set_num'])
        data.save()
    return HttpResponse(status=200)


@api_view(['POST'])
def postExerciseRecordAerobic(request):
    request = json.loads(request.body)
    record = ExerciseRecordAerobic(user_id=request['user_id'], exercise_id=request['exercise_id'], exercise_plan_aerobic_id=request['exercise_plan_aerobic_id'],
                                   date=request['date'], record_distance=request['record_distance'], record_duration=request['record_duration'],
                                   start_time=request['start_time'], end_time=request['end_time'])
    record.save()
    return HttpResponse(status=200)
