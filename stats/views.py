from itertools import chain
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from dateutil.relativedelta import relativedelta
import datetime
import json
from .uxCopy import *

from exercise.models import *
from .models import *

from exercise.serializers import ExerciseRecordWeightSerializer, ExerciseRecordWeightSetSerializer, ExerciseSerializer
from .serializers import *
# Create your views here.


def getWeeklyExerciseStats(uuid, firstDate):
    lastDate = firstDate + datetime.timedelta(days=6)
    data = {}
    if (DailyExerciseStats.objects.filter(user_id=uuid, day__range=[firstDate, lastDate]).exists()):
        weekDailyStats = DailyExerciseStats.objects.filter(
            user_id=uuid, day__range=[firstDate, lastDate])
        exerciseDays = weekDailyStats.count()
        avgExerciseTime = avgExerciseVolume = maxOneRm = avgDistance = 0

        for dailyStats in weekDailyStats:
            avgExerciseTime += dailyStats.total_exercise_time
            recordWeights = ExerciseRecordWeight.objects.filter(
                user_id=uuid, start_time__date=dailyStats.day)
            avgExerciseVolume += dailyStats.total_volume/recordWeights.count()
            maxOneRm = max(maxOneRm, dailyStats.max_one_rm)
            avgDistance += dailyStats.total_distance/exerciseDays

        avgExerciseTime = round(avgExerciseTime/exerciseDays)

        data = {
            'exercise_days': exerciseDays,
            'avg_exercise_time': avgExerciseTime,
            'avg_exercise_volume': avgExerciseVolume,
            'max_one_rm': maxOneRm,
            'avg_distance': avgDistance,
        }

    return data


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dailyExerciseStats(request):
    uuid = request.user.uuid
    searchDate = datetime.datetime.strptime(request.GET['day'], '%Y/%m/%d')
    data = {}
    if (DailyExerciseStats.objects.filter(user_id=uuid, day=searchDate).exists()):
        dailyStats = DailyExerciseStats.objects.get(
            user_id=uuid, day=searchDate)
        recordWeights = ExerciseRecordWeight.objects.filter(
            user_id=uuid, start_time__date=searchDate)
        recordData = []

        for index, record in enumerate(recordWeights):
            recordData.append(ExerciseRecordWeightSerializer(record).data)
            recordSets = ExerciseRecordWeightSet.objects.filter(
                exercise_record_weight_id=record.id)
            setDataList = []
            for set in recordSets:
                setDataList.append(ExerciseRecordWeightSetSerializer(set).data)
            recordData[index]['sets'] = setDataList
            exercise = Exercise.objects.get(id=record.exercise_id)
            recordData[index]['exercise_data'] = {
                'name': exercise.name,
                'target_muscle': exercise.target_muscle,
                'exercise_method': exercise.exercise_method,
            }

        data = {
            'stats': DailyExerciseStatsSerializer(dailyStats).data,
            'records': recordData,
        }

    return Response(data=data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dailyExerciseStatsMemo(request):
    uuid = request.user.uuid
    data = json.loads(request.body)
    date = datetime.datetime.strptime(data['date'], '%Y/%m/%d')
    print(data['memo'])
    print(type(data['memo']))
    if (DailyExerciseStats.objects.filter(user_id=uuid, day=date).exists()):
        stats = DailyExerciseStats.objects.get(user_id=uuid, day=date)
        stats.memo = data['memo']
        stats.save()
    else:
        stats = DailyExerciseStats(user_id=uuid, day=date, memo=data['memo'])
        stats.save()

    return HttpResponse(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def weeklyExerciseStats(request):
    uuid = request.user.uuid
    firstDate = datetime.datetime.strptime(
        request.GET['first_day'], '%Y/%m/%d')
    lastDate = firstDate + datetime.timedelta(days=6)
    data = {}

    if (DailyExerciseStats.objects.filter(user_id=uuid, day__range=[firstDate, lastDate]).exists()):
        weekDailyStats = DailyExerciseStats.objects.filter(
            user_id=uuid, day__range=[firstDate, lastDate])
        previousWeekDailyStats = DailyExerciseStats.objects.filter(
            user_id=uuid, day__range=[firstDate - datetime.timedelta(days=7), lastDate - datetime.timedelta(days=7)])
        exerciseDays = weekDailyStats.count()
        previousExerciseDays = previousWeekDailyStats.count()
        avgExerciseTime = avgExerciseVolume = maxOneRm = avgDistance = 0
        previousAvgExerciseTime = previousAvgExerciseVolume = previousMaxOneRm = previousAvgDistance = 0
        weeklyExerciseTimeList = [0] * 7
        totalExerciseTimeCompared = [0] * 2

        for dailyStats in weekDailyStats:
            avgExerciseTime += dailyStats.total_exercise_time
            recordWeights = ExerciseRecordWeight.objects.filter(
                user_id=uuid, start_time__date=dailyStats.day)
            avgExerciseVolume += dailyStats.total_volume/recordWeights.count()
            maxOneRm = max(maxOneRm, dailyStats.max_one_rm)
            avgDistance += dailyStats.total_distance/exerciseDays
            weeklyExerciseTimeList[dailyStats.day.weekday(
            )] = dailyStats.total_exercise_time
            totalExerciseTimeCompared[1] += dailyStats.total_exercise_time

        for previousDailyStats in previousWeekDailyStats:
            previousAvgExerciseTime += previousDailyStats.total_exercise_time
            recordWeights = ExerciseRecordWeight.objects.filter(
                user_id=uuid, start_time__date=previousDailyStats.day)
            previousAvgExerciseVolume += previousDailyStats.total_volume/recordWeights.count()
            previousMaxOneRm = max(
                previousMaxOneRm, previousDailyStats.max_one_rm)
            previousAvgDistance += previousDailyStats.total_distance / \
                previousExerciseDays
            totalExerciseTimeCompared[0] += previousDailyStats.total_exercise_time

        avgExerciseTime = round(avgExerciseTime/exerciseDays)

        if previousWeekDailyStats.count() != 0:
            previousAvgExerciseTime = round(
                previousAvgExerciseTime/previousExerciseDays)

        data = {
            'exercise_days': {
                'current': exerciseDays,
                'diff': exerciseDays - previousExerciseDays,
            },
            'avg_exercise_time': {
                'current': avgExerciseTime,
                'diff':  avgExerciseTime - previousAvgExerciseTime,
            },
            'avg_exercise_volume': {
                'current': avgExerciseVolume,
                'diff': avgExerciseVolume - previousAvgExerciseVolume,
            },
            'max_one_rm': {
                'current': maxOneRm,
                'diff': maxOneRm - previousMaxOneRm,
            },
            'avg_distance': {
                'current': avgDistance,
                'diff': avgDistance - previousAvgDistance,
            },
            'weekly_exercise_time_list': weeklyExerciseTimeList,
            'total_exercise_time_compared': totalExerciseTimeCompared,

        }

    return Response(data=data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def monthlyExerciseStats(request):
    uuid = request.user.uuid
    month = datetime.datetime.strptime(request.GET['month'], '%Y/%m')
    previousNumWeeks = int(request.GET['previous_num_weeks'])
    previousFirstWeekStart = datetime.datetime.strptime(
        request.GET['previous_first_week_start'], '%Y/%m/%d')
    numWeeks = int(request.GET['num_weeks'])
    firstWeekStart = datetime.datetime.strptime(
        request.GET['first_week_start'], '%Y/%m/%d')
    weightTimeDict = {}
    maxTimeList = [0, 0]
    cardioTime = 0
    data = {}
    if (DailyExerciseStats.objects.filter(user_id=uuid, day__month=month.month)):
        monthDailyStats = DailyExerciseStats.objects.filter(
            user_id=uuid, day__month=month.month)
        previousMonthDailyStats = DailyExerciseStats.objects.filter(
            user_id=uuid, day__month=(month-relativedelta(months=1)).month)
        exerciseDays = monthDailyStats.count()
        previousExerciseDays = previousMonthDailyStats.count()
        avgExerciseTime = avgExerciseVolume = maxOneRm = avgDistance = 0
        previousAvgExerciseTime = previousAvgExerciseVolume = previousMaxOneRm = previousAvgDistance = 0
        for dailyStats in monthDailyStats:
            avgExerciseTime += dailyStats.total_exercise_time
            recordWeights = ExerciseRecordWeight.objects.filter(
                user_id=uuid, start_time__date=dailyStats.day)
            recordCardio = ExerciseRecordCardio.objects.filter(
                user_id=uuid, start_time__date=dailyStats.day)
            avgExerciseVolume += dailyStats.total_volume/recordWeights.count()
            maxOneRm = max(maxOneRm, dailyStats.max_one_rm)
            avgDistance += dailyStats.total_distance/exerciseDays
            for record in recordWeights:
                exercise = Exercise.objects.get(id=record.exercise_id)
                if exercise.target_muscle in weightTimeDict:
                    weightTimeDict[exercise.target_muscle] += record.exercise_time
                    if record.exercise_time > maxTimeList[1]:
                        maxTimeList[0] = exercise.target_muscle
                        maxTimeList[1] = record.exercise_time
                else:
                    weightTimeDict[exercise.target_muscle] = record.exercise_time
                    if record.exercise_time > maxTimeList[1]:
                        maxTimeList[0] = exercise.target_muscle
                        maxTimeList[1] = record.exercise_time
            for record in recordCardio:
                cardioTime += record.record_duration
                if record.record_duration > maxTimeList[1]:
                    maxTimeList[0] = -1
                    maxTimeList[1] = record.record_duration

        categoryStatsCopy = monthlyExerciseCategoryStatsCopy[maxTimeList[0]]

        for previousDailyStats in previousMonthDailyStats:
            previousAvgExerciseTime += previousDailyStats.total_exercise_time
            recordWeights = ExerciseRecordWeight.objects.filter(
                user_id=uuid, start_time__date=previousDailyStats.day)
            previousAvgExerciseVolume += previousDailyStats.total_volume/recordWeights.count()
            previousMaxOneRm = max(
                previousMaxOneRm, previousDailyStats.max_one_rm)
            previousAvgDistance += previousDailyStats.total_distance / \
                previousExerciseDays

        avgExerciseTime = round(avgExerciseTime/exerciseDays)

        if previousMonthDailyStats.count() != 0:
            previousAvgExerciseTime = round(
                previousAvgExerciseTime/previousExerciseDays)

        data = {
            'exercise_days': {
                'current': exerciseDays,
                'diff': exerciseDays - previousExerciseDays,
            },
            'avg_exercise_time': {
                'current': avgExerciseTime,
                'diff':  avgExerciseTime - previousAvgExerciseTime,
            },
            'avg_exercise_volume': {
                'current': avgExerciseVolume,
                'diff': avgExerciseVolume - previousAvgExerciseVolume,
            },
            'max_one_rm': {
                'current': maxOneRm,
                'diff': maxOneRm - previousMaxOneRm,
            },
            'avg_distance': {
                'current': avgDistance,
                'diff': avgDistance - previousAvgDistance,
            },
            'weekly_list': [],
            'previous_weekly_list': [],
            'category_stats': {
                'weight': weightTimeDict,
                'cardio': cardioTime,
                'copy': categoryStatsCopy,
            },
        }
    for i in range(numWeeks):
        weeklyStats = getWeeklyExerciseStats(
            uuid, firstWeekStart + datetime.timedelta(days=i*7))
        if 'weekly_list' in data:
            data['weekly_list'].append(weeklyStats)
    for i in range(previousNumWeeks):
        weeklyStats = getWeeklyExerciseStats(
            uuid, previousFirstWeekStart + datetime.timedelta(days=i*7))
        if 'previous_weekly_list' in data:
            data['previous_weekly_list'].append(weeklyStats)

    return Response(data=data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def monthlyExerciseDates(request):
    uuid = request.user.uuid
    searchMonth = datetime.datetime.strptime(request.GET['month'], '%Y/%m')
    data = []
    exerciseRecordWeight = ExerciseRecordWeight.objects.filter(
        user_id=uuid, date__year=searchMonth.year, date__month=searchMonth.month).order_by('date')
    exerciseRecordCardio = ExerciseRecordCardio.objects.filter(
        user_id=uuid, date__year=searchMonth.year, date__month=searchMonth.month)
    exerciseRecords = chain(exerciseRecordWeight, exerciseRecordCardio)
    for record in exerciseRecords:
        if isinstance(record, ExerciseRecordWeight):
            exercise = Exercise.objects.get(id=record.exercise_id)
            data.append([
                record.date, exercise.target_muscle
            ])
        else:
            exercise = Exercise.objects.get(id=record.exercise_id)
            data.append([
                record.date.strftime("%m/%d/%Y"), 0
            ])

    return Response(data=data)
