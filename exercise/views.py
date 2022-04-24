from itertools import chain
from tkinter import E
from django.http.response import HttpResponse
from django.shortcuts import render
from django.utils import tree
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import datetime
import json
from django.utils.dateparse import parse_datetime

from notifications.fcm_notification import exercise_attendance_fcm
from .models import *
from stats.models import DailyExerciseStats, PhysicalDataRecord
from .serializers import ExerciseDetailsSerializer, ExercisePlanCardioSerializer, ExercisePlanWeightSerializer, ExercisePlanWeightSetSerializer, ExerciseRecordBodyWeightSerializer, ExerciseRecordCardioSerializer, ExerciseRecordWeightSerializer, ExerciseSerializer, ExerciseTimeSerializer, ExerciseRecordWeightSetSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllExercise(request):
    exerciseListWeight = Exercise.objects.filter(type=0)
    exerciseListCardio = Exercise.objects.filter(type=1)
    data = {
        'weight': ExerciseSerializer(exerciseListWeight, many=True).data,
        'cardio': ExerciseSerializer(exerciseListCardio, many=True).data,
    }
    return Response(data)


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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getExerciseStatusWeek(request):
    uuid = request.user.uuid
    firstDate = datetime.datetime.strptime(
        request.GET['first_date'], '%Y-%m-%d')
    todayDate = datetime.datetime.now()
    weekStatus = {}
    weekWeightPlans = ExercisePlanWeight.objects.filter(
        user_id=uuid, date__range=[firstDate, todayDate], completed=False)
    weekCardioPlans = ExercisePlanCardio.objects.filter(
        user_id=uuid, date__range=[firstDate, todayDate], completed=False)
    weekWeightRecords = ExerciseRecordWeight.objects.filter(
        user_id=uuid, date__range=[firstDate, todayDate])
    weekCardioRecords = ExerciseRecordCardio.objects.filter(
        user_id=uuid, date__range=[firstDate, todayDate])

    for i in range((todayDate - firstDate).days + 1):

        indexDate = firstDate + datetime.timedelta(days=i)
        weightPlans = weekWeightPlans.filter(date=indexDate)
        cardioPlans = weekCardioPlans.filter(date=indexDate)
        weightRecords = weekWeightRecords.filter(date=indexDate)
        cardioRecords = weekCardioRecords.filter(date=indexDate)

        plans = chain(weightPlans, cardioPlans)
        records = chain(weightRecords, cardioRecords)
        planDataList = []
        recordDataList = []
        totalExerciseTime = 0
        for plan in plans:
            if isinstance(plan, ExercisePlanWeight):
                planData = ExercisePlanWeightSerializer(plan).data
                exerciseData = ExerciseSerializer(
                    Exercise.objects.get(id=plan.exercise_id)).data
            else:
                planData = ExercisePlanCardioSerializer(plan).data
                exerciseData = ExerciseSerializer(
                    Exercise.objects.get(id=plan.exercise_id)).data
            data = {
                'exercise_data': exerciseData,
                'plan_data': planData,
            }
            planDataList.append(data)

        for record in records:
            exerciseTime = int(
                (record.end_time - record.start_time).total_seconds())
            totalExerciseTime += exerciseTime
            if isinstance(record, ExerciseRecordWeight):
                recordData = {
                    'total_sets': record.total_sets,
                    'total_volume': record.total_volume,
                    'total_reps': record.total_reps,
                }
            else:
                recordData = {
                    'record_duration': record.record_duration,
                    'record_distance': record.record_distance,
                }

            exerciseData = ExerciseSerializer(
                Exercise.objects.get(id=record.exercise_id)).data

            data = {
                'exercise_data': exerciseData,
                'record_data': recordData,
            }
            recordDataList.append(data)

        if indexDate.date() == todayDate.date():
            weekStatus[indexDate.strftime('%Y/%m/%d')] = {
                'plans': planDataList,
                'records': recordDataList,
                'total_exercise_time': totalExerciseTime,
            }
        else:
            weekStatus[indexDate.strftime('%Y/%m/%d')] = {
                'plans': planDataList,
                'records': recordDataList,
            }
    return Response(weekStatus)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getExerciseStatusDate(request):
    uuid = request.user.uuid
    _date = request.GET['date']
    date = datetime.datetime.strptime(_date, '%Y-%m-%d')
    weightPlans = ExercisePlanWeight.objects.filter(
        user_id=uuid, date=date, completed=False)
    aerobicPlans = ExercisePlanCardio.objects.filter(
        user_id=uuid, date=date, completed=False)
    weightRecords = ExerciseRecordWeight.objects.filter(
        user_id=uuid, date=date)
    aerobicRecords = ExerciseRecordCardio.objects.filter(
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
            planData = ExercisePlanCardioSerializer(plan).data
            exerciseData = ExerciseSerializer(
                Exercise.objects.get(id=plan.exercise_id)).data
        data = {
            'exercise_data': exerciseData,
            'plan_data': planData,
        }
        planDataList.append(data)

    for record in records:
        exerciseTime = int(
            (record.end_time - record.start_time).total_seconds())
        totalExerciseTime += exerciseTime
        if isinstance(record, ExerciseRecordWeight):
            recordData = {
                'total_sets': record.total_sets,
                'total_volume': record.total_volume,
                'total_reps': record.total_reps,
            }
        else:
            recordData = {
                'record_duration': record.record_duration,
                'record_distance': record.record_distance,
            }

        exerciseData = ExerciseSerializer(
            Exercise.objects.get(id=record.exercise_id)).data

        data = {
            'exercise_data': exerciseData,
            'record_data': recordData,
        }
        recordDataList.append(data)
    if date.date() == datetime.datetime.now().date():
        returnData = {
            'plans': planDataList,
            'records': recordDataList,
            'total_exercise_time': totalExerciseTime,
        }
    else:
        returnData = {
            'plans': planDataList,
            'records': recordDataList,
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
def getExercisePlanCardio(request):
    _exercise_plan_cardio_id = request.GET['exercise_plan_cardio_id']
    sets = ExercisePlanCardio.objects.filter(
        exercise_plan_cardio_id=_exercise_plan_cardio_id)
    serializer = ExercisePlanWeightSetSerializer(sets, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserPlanCardioDate(request):
    _user_id = request.GET['user_id']
    _date = request.GET['date']
    _date = datetime.datetime.strptime(_date, '%Y/%m/%d')
    plans = ExercisePlanCardio.objects.filter(user_id=_user_id, date=_date)
    serializer = ExercisePlanCardioSerializer(plans, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserRecordWeight(request):
    uuid = request.user.uuid
    record = ExerciseRecordWeight.objects.filter(
        user_id=uuid).order_by('-date')
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
def getUserRecordCardio(request):
    _user_id = request.GET['user_id']
    record = ExerciseRecordCardio.objects.filter(user_id=_user_id)
    serializer = ExerciseRecordCardioSerializer(record, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserRecordCardioDate(request):
    _user_id = request.GET['user_id']
    _date = request.GET['date']
    _date = datetime.datetime.strptime(_date, '%Y/%m/%d')
    record = ExerciseRecordCardio.objects.filter(user_id=_user_id, date=_date)
    serializer = ExerciseRecordCardioSerializer(record, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getExerciseTime(request):
    date = request.GET['date']
    userId = request.GET['user_id']
    parsedDate = datetime.datetime.strptime(date, '%Y/%m/%d')
    aerobic_record = ExerciseRecordCardio.objects.filter(
        date=parsedDate, user_id=userId)
    weight_record = ExerciseRecordWeight.objects.filter(
        date=parsedDate, user_id=userId)
    duration = datetime.timedelta(hours=0, minutes=0, seconds=0)
    for record in aerobic_record:
        recordStartTime = record.start_time
        recordEndTime = record.end_Time
        diff = recordEndTime - recordStartTime
        duration = duration + diff
    for record in weight_record:
        diff = recordEndTime - recordStartTime
        duration = duration + diff
    duration = {'duration': duration}
    serializer = ExerciseTimeSerializer(duration)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recentExercisePlan(request):
    uuid = request.user.uuid
    exercise = Exercise.objects.get(id=request.GET['id'])
    data = {}
    if exercise.type == 0:
        plans = ExercisePlanWeight.objects.filter(
            user_id=uuid, exercise_id=exercise.id)
        if plans.exists():
            plan = ExercisePlanWeight.objects.filter(
                user_id=uuid, exercise_id=exercise.id).latest()
            sets = ExercisePlanWeightSet.objects.filter(
                exercise_plan_weight_id=plan.id)
            setData = []

            for set in sets:
                setData.append(ExercisePlanWeightSetSerializer(set).data)

            data['sets'] = setData
        else:
            data['sets'] = []
    else:
        plans = ExercisePlanCardio.objects.filter(
            user_id=uuid, exercise_id=exercise.id)
        if plans.exists():
            plan = ExercisePlanCardio.objects.filter(
                user_id=uuid, exercise_id=exercise.id).latest()
            data = ExercisePlanCardioSerializer(plan).data
        else:
            data = {}

    return Response(data=data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def postExercisePlanWeight(request):
    user_id = request.user.uuid
    data = json.loads(request.body)
    sets = data['sets']
    plan = ExercisePlanWeight(
        user_id=user_id, exercise_id=data['exercise_id'], num_sets=len(sets))
    plan.save()

    for set in sets:
        data = ExercisePlanWeightSet(exercise_plan_weight_id=plan.id,
                                     set_num=set['set_num'], target_weight=set['target_weight'], target_reps=set['target_reps'])
        data.save()
    return HttpResponse(status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def postExercisePlanCardio(request):
    uuid = request.user.uuid
    data = json.loads(request.body)
    record = ExercisePlanCardio(user_id=uuid, exercise_id=data['exercise_id'],
                                target_distance=data['target_distance'], target_duration=data['target_duration'])
    record.save()
    return HttpResponse(status=200)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def exerciseRecordWeight(request):
    uuid = request.user.uuid
    if request.method == 'POST':
        data = json.loads(request.body)
        sets = data['sets']
        maxOneRm = totalVolume = totalReps = 0
        for set in sets:
            totalVolume += float(set['record_weight']) * \
                int(set['record_reps'])
            totalReps += int(set['record_reps'])
            oneRm = float(set['record_weight']) * \
                (1 + int(set['record_reps']) * 0.025)
            if oneRm > maxOneRm:
                maxOneRm = oneRm

        plan = ExercisePlanWeight.objects.get(
            id=data['exercise_plan_weight_id'])
        plan.completed = True
        plan.save()

        record = ExerciseRecordWeight(user_id=uuid, exercise_plan_weight_id=data['exercise_plan_weight_id'],
                                      exercise_id=data['exercise_id'],
                                      total_sets=len(sets), total_reps=totalReps, exercise_time=int((parse_datetime(data['end_time'])-parse_datetime(data['start_time'])).total_seconds()), start_time=data['start_time'], end_time=data['end_time'], total_volume=totalVolume, max_one_rm=maxOneRm)
        record.save()

        for idx, set in enumerate(sets):
            recordSet = ExerciseRecordWeightSet(exercise_record_weight_id=record.id, record_weight=set['record_weight'],
                                                record_reps=set['record_reps'],
                                                set_num=idx + 1, one_rm=float(set['record_weight']) * (1 + int(set['record_reps']) * 0.025))
            recordSet.save()

        if DailyExerciseStats.objects.filter(user_id=uuid, day=record.date).exists():
            dailyRecord = DailyExerciseStats.objects.get(
                user_id=uuid, day=record.date)
            dailyRecord.total_exercise_time += record.exercise_time
            dailyRecord.total_volume += totalVolume
            dailyRecord.total_sets += len(sets)
            dailyRecord.max_one_rm = max(dailyRecord.max_one_rm, maxOneRm)
            dailyRecord.save()
        else:
            dailyRecord = DailyExerciseStats(day=record.date, user_id=uuid, total_exercise_time=record.exercise_time,
                                             total_volume=totalVolume, total_sets=len(sets), max_one_rm=maxOneRm)
            dailyRecord.save()
            exercise_attendance_fcm(uuid)

        return Response(status=200, data=record.id)

    else:
        exerciseRecordWeightId = int(request.GET['id'])
        record = ExerciseRecordWeight.objects.get(id=exerciseRecordWeightId)
        exercise = Exercise.objects.get(id=record.exercise_id)
        data = {
            'exercise_name': exercise.name,
            'record_data': ExerciseRecordWeightSerializer(record).data if exercise.exercise_method != 1 else ExerciseRecordBodyWeightSerializer(record).data,
        }
        return Response(data=data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def exerciseRecordCardio(request):
    uuid = request.user.uuid
    if request.method == 'POST':
        data = json.loads(request.body)
        record = ExerciseRecordCardio(user_id=uuid, exercise_id=data['exercise_id'], exercise_plan_cardio_id=data['exercise_plan_cardio_id'],
                                      record_duration=data['record_duration'],
                                      start_time=data['start_time'], end_time=data['end_time'])
        if 'record_distance' in data:
            record.record_distance = data['record_distance']
        exercise = Exercise.objects.get(id=record.exercise_id)
        calories = record.record_duration / 60 * exercise.cardio_met * 3.5 * 0.001 * \
            PhysicalDataRecord.objects.filter(user_id=uuid).order_by(
                '-created_at').first().weight * 5
        record.record_calories = calories
        record.save()
        plan = ExercisePlanCardio.objects.get(
            id=data['exercise_plan_cardio_id'])
        plan.completed = 1
        plan.save()

        if DailyExerciseStats.objects.filter(user_id=uuid, day=record.date).exists():
            dailyRecord = DailyExerciseStats.objects.get(
                user_id=uuid, day=record.date)
            dailyRecord.total_exercise_time += record.record_duration
            if record.record_distance is not None:
                dailyRecord.total_distance += record.record_distance
            dailyRecord.total_calories += record.record_calories
            dailyRecord.save()
        else:
            dailyRecord = DailyExerciseStats(day=record.date, user_id=uuid, total_exercise_time=record.record_duration,
                                             total_calories=record.record_calories)
            if record.record_distance is not None:
                dailyRecord.total_distance += record.record_distance
            dailyRecord.save()
            exercise_attendance_fcm(uuid)

        return Response(status=200, data=record.id)
    else:
        exerciseRecordCardioId = int(request.GET['id'])
        record = ExerciseRecordCardio.objects.get(id=exerciseRecordCardioId)
        exercise = Exercise.objects.get(id=record.exercise_id)
        data = {
            'exercise_name': exercise.name,
            'record_data': {
                'record_duration': record.record_duration,
                'record_distance': record.record_distance,
                'record_calories': record.record_calories,
            },
        }
        return Response(data=data)
