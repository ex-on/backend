from itertools import chain
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
@permission_classes([IsAuthenticated])
def getExerciseByTargetMuscle(request):
    _target_muscle = request.GET['target_muscle']
    exerciseList = Exercise.objects.filter(target_muscle=_target_muscle)
    serializer = ExerciseSerializer(exerciseList, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getExerciseByExerciseMethod(request):
    _exercise_method = request.GET['exercise_method']
    exerciseList = Exercise.objects.filter(exercise_method=_exercise_method)
    serializer = ExerciseSerializer(exerciseList, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getExerciseByTargetMuscleExerciseMethod(request):
    _target_muscle = request.GET['target_muscle']
    _exercise_method = request.GET['exercise_method']
    exerciseList = Exercise.objects.filter(
        target_muscle=_target_muscle, exercise_method=_exercise_method)
    serializer = ExerciseSerializer(exerciseList, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getExerciseDetails(request):
    _exercise_id = request.GET['exercise_id']
    details = ExerciseDetails.objects.filter(exercise_id=_exercise_id)
    serializer = ExerciseDetailsSerializer(details, many=True)
    return Response(serializer.data)

########### 운동 계획 조회 #############################


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getExerciseStatusDate(request):
    uuid = request.user.uuid
    _date = request.GET['date']
    date = datetime.datetime.strptime(_date, '%Y-%m-%d')
    weightPlans = ExercisePlanWeight.objects.filter(user_id=uuid, date=date, completed=False)
    aerobicPlans = ExercisePlanAerobic.objects.filter(user_id=uuid, date=date, completed=False)
    weightRecords = ExerciseRecordWeight.objects.filter(
        user_id=uuid, date=date)
    aerobicRecords = ExerciseRecordAerobic.objects.filter(
        user_id=uuid, date=date)
    plans = chain(weightPlans, aerobicPlans)
    records = chain(weightRecords, aerobicRecords)
    planDataList = []
    recordDataList = []
    totalExerciseTime = 0
    for plan in plans:
        if isinstance(plan, ExercisePlanWeight):
            planData = ExercisePlanWeightSerializer(plan).data
            exerciseData = ExerciseSerializer(
                Exercise.objects.get(id=plan.exercise_id)).data
        else:
            planData = ExercisePlanAerobicSerializer(plan).data
            exerciseData = ExerciseSerializer(
                Exercise.objects.get(id=plan.exercise_id)).data
        data = {
            'exercise_data': exerciseData,
            'plan_data': planData,
        }
        planDataList.append(data)
    for record in records:
        exerciseTime = int((record.end_time - record.start_time).total_seconds())
        totalExerciseTime += exerciseTime
        if isinstance(record, ExerciseRecordWeight):
            recordData = {
                'total_sets': record.total_sets,
                'total_volume': record.total_volume,
            }
            exerciseData = ExerciseSerializer(
                Exercise.objects.get(id=record.exercise_id)).data
        # else:
        data = {
            'exercise_data': exerciseData,
            'record_data': recordData,
        }
        recordDataList.append(data)
    returnData = {
        'plans': planDataList,
        'records': recordDataList,
        'total_exercise_time': totalExerciseTime,
    }

    return Response(returnData)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getExercisePlanWeightSets(request):
    _exercise_plan_weight_id = request.GET['exercise_plan_weight_id']
    sets = ExercisePlanWeightSet.objects.filter(
        exercise_plan_weight_id=_exercise_plan_weight_id)
    serializer = ExercisePlanWeightSetSerializer(sets, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserPlanAerobicDate(request):
    _user_id = request.GET['user_id']
    _date = request.GET['date']
    _date = datetime.datetime.strptime(_date, '%Y/%m/%d')
    plans = ExercisePlanAerobic.objects.filter(user_id=_user_id, date=_date)
    serializer = ExercisePlanAerobicSerializer(plans, many=True)
    return Response(serializer.data)

########### 운동 기록 조회 #############################


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserRecordWeight(request):
    _user_id = request.GET['user_id']
    record = ExerciseRecordWeight.objects.filter(
        user_id=_user_id).order_by('-date')
    serializer = ExerciseRecordWeightSerializer(record, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserRecordWeightDate(request):
    _user_id = request.GET['user_id']
    _date = request.GET['date']
    _date = datetime.datetime.strptime(_date, '%Y/%m/%d')
    record = ExerciseRecordWeight.objects.filter(user_id=_user_id, date=_date)
    serializer = ExerciseRecordWeightSerializer(record, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserRecordWeightTargetMuscle(request):
    _user_id = request.GET['user_id']
    _target_muscle = request.GET['target_muscle']
    record = ExerciseRecordWeight.objects.filter(
        user_id=_user_id, target_muscle=_target_muscle).order_by('-date')
    serializer = ExerciseRecordWeightSerializer(record, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserRecordWeightSets(request):
    record_id = request.GET['exercise_record_weight_id']
    record_sets = ExerciseRecordWeightSet.objects.filter(
        exercise_record_weight=record_id)
    serializer = ExerciseRecordWeightSetSerializer(record_sets, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserRecordAerobic(request):
    _user_id = request.GET['user_id']
    record = ExerciseRecordAerobic.objects.filter(user_id=_user_id)
    serializer = ExerciseRecordAerobicSerializer(record, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserRecordAerobicDate(request):
    _user_id = request.GET['user_id']
    _date = request.GET['date']
    _date = datetime.datetime.strptime(_date, '%Y/%m/%d')
    record = ExerciseRecordAerobic.objects.filter(user_id=_user_id, date=_date)
    serializer = ExerciseRecordAerobicSerializer(record, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def postExercisePlanAerobic(request):
    request = json.loads(request.body)
    record = ExercisePlanAerobic(user_id=request['user_id'], exercise_id=request['exercise_id'], date=request['date'],
                                 target_distance=request['target_distance'], target_duration=request['target_duration'])
    record.save()
    return HttpResponse(status=200)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def exerciseRecordWeight(request):
    uuid = request.user.uuid
    if request.method == 'POST':
        request = json.loads(request.body)
        sets = request['sets']
        totalVolume = 0
        maxOneRm = 0
        for set in sets:
            totalVolume += float(set['record_weight']) * \
                int(set['record_reps'])
            oneRm = float(set['record_weight']) * \
                (1 + int(set['record_reps']) * 0.025)
            if oneRm > maxOneRm:
                maxOneRm = oneRm

        plan = ExercisePlanWeight.objects.get(id=request['exercise_plan_weight_id'])
        plan.completed = True
        plan.save()

        record = ExerciseRecordWeight(user_id=uuid, exercise_plan_weight_id=request['exercise_plan_weight_id'],
                                      exercise_id=request['exercise_id'],
                                      total_sets=len(sets), start_time=request['start_time'], end_time=request['end_time'], total_volume=totalVolume, max_one_rm=maxOneRm)
        record.save()

        for idx, set in enumerate(sets):
            data = ExerciseRecordWeightSet(exercise_record_weight_id=record.id, record_weight=set['record_weight'],
                                           record_reps=set['record_reps'], start_time=set['start_time'],
                                           end_time=set['end_time'], set_num=idx + 1, one_rm=float(set['record_weight']) * (1 + int(set['record_reps']) * 0.025))
            data.save()
        return Response(status=200, data=record.id)
    else:
        exerciseRecordWeightId = int(request.GET['id'])
        record = ExerciseRecordWeight.objects.get(id=exerciseRecordWeightId)
        exercise = Exercise.objects.get(id=record.exercise_id)
        data = {
            'exercise_name': exercise.name,
            'record_data': ExerciseRecordWeightSerializer(record).data
        }
        return Response(data=data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def exerciseRecordAerobic(request):
    request = json.loads(request.body)
    record = ExerciseRecordAerobic(user_id=request['user_id'], exercise_id=request['exercise_id'], exercise_plan_aerobic_id=request['exercise_plan_aerobic_id'],
                                   date=request['date'], record_distance=request['record_distance'], record_duration=request['record_duration'],
                                   start_time=request['start_time'], end_time=request['end_time'])
    record.save()
    return HttpResponse(status=200)
