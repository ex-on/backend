from http import HTTPStatus
from itertools import chain
from math import ceil
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from dateutil.relativedelta import relativedelta
import datetime
import json
from stats.constants import getStandardBmi, getStandardBodyFatPercentage

from users.models import UserDetailsStatic
from .uxCopy import *

from exercise.models import *
from .models import *

from exercise.serializers import ExercisePlanCardioSerializer, ExerciseRecordBodyWeightSerializer, ExerciseRecordCardioSerializer, ExerciseRecordWeightSerializer, ExerciseRecordWeightSetSerializer, ExerciseSerializer
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
            if recordWeights.count() > 0:
                avgExerciseVolume += dailyStats.total_volume/recordWeights.count()
            else:
                avgExerciseVolume = 0
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
        recordsWeight = ExerciseRecordWeight.objects.filter(
            user_id=uuid, start_time__date=searchDate)
        recordsCardio = ExerciseRecordCardio.objects.filter(
            user_id=uuid, start_time__date=searchDate)
        recordData = []

        for index, record in enumerate(recordsWeight):
            weightData = ExerciseRecordWeightSerializer(record).data
            recordSets = ExerciseRecordWeightSet.objects.filter(
                exercise_record_weight_id=record.id)
            setDataList = []
            for set in recordSets:
                setDataList.append(ExerciseRecordWeightSetSerializer(set).data)
            weightData['sets'] = setDataList
            exercise = Exercise.objects.get(id=record.exercise_id)
            weightData['exercise_data'] = {
                'name': exercise.name,
                'target_muscle': exercise.target_muscle,
                'exercise_method': exercise.exercise_method,
            }
            recordData.append(weightData)

        for index, record in enumerate(recordsCardio):
            cardioData = ExerciseRecordCardioSerializer(record).data
            plan = ExercisePlanCardio.objects.get(
                id=record.exercise_plan_cardio_id)
            exercise = Exercise.objects.get(id=record.exercise_id)
            cardioData['target_duration'] = plan.target_duration
            cardioData['target_distance'] = plan.target_distance
            cardioData['exercise_data'] = {
                'name': exercise.name,
                'exercise_method': exercise.exercise_method,
            }
            recordData.append(cardioData)

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
            if recordWeights.count() > 0:
                avgExerciseVolume += dailyStats.total_volume/recordWeights.count()
            else:
                avgExerciseVolume = 0
            maxOneRm = max(maxOneRm, dailyStats.max_one_rm)
            avgDistance += dailyStats.total_distance/exerciseDays
            weeklyExerciseTimeList[dailyStats.day.weekday(
            )] = dailyStats.total_exercise_time
            totalExerciseTimeCompared[1] += dailyStats.total_exercise_time

        for previousDailyStats in previousWeekDailyStats:
            previousAvgExerciseTime += previousDailyStats.total_exercise_time
            recordWeights = ExerciseRecordWeight.objects.filter(
                user_id=uuid, start_time__date=previousDailyStats.day)
            if recordWeights.count() > 0:
                previousAvgExerciseVolume += previousDailyStats.total_volume/recordWeights.count()
            else:
                previousAvgExerciseVolume = 0
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
            if recordWeights.count() > 0:
                avgExerciseVolume += dailyStats.total_volume/recordWeights.count()
            else:
                avgExerciseVolume = 0
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
            if recordWeights.count() > 0:
                previousAvgExerciseVolume += previousDailyStats.total_volume/recordWeights.count()
            else:
                previousAvgExerciseVolume = 0
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
                # record.date.strftime("%m/%d/%Y"), 0
                record.date, 0
            ])

    return Response(data=data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cumulativeTimeStats(request):
    uuid = request.user.uuid
    exerciseStats = DailyExerciseStats.objects.filter(
        user_id=uuid).order_by('day')

    recordCount = exerciseStats.count()
    if recordCount > 1:
        numWeeks = ceil((exerciseStats.last().day -
                         exerciseStats.first().day).days/7)
    elif recordCount == 1:
        numWeeks = 1
    else:
        numWeeks = 0

    exerciseTimeStat = {}
    if exerciseStats.exists():
        firstStatDate = exerciseStats.first().day
        sumExerciseTime = avgWeekExerciseNum = avgExerciseTime = 0
        avgWeekExerciseNum = round(recordCount / numWeeks, 1)
        physicalStat = []
        for stat in exerciseStats:
            sumExerciseTime += stat.total_exercise_time
            exerciseTimeStat[datetime.datetime.strftime(
                stat.day, '%Y-%m-%d')] = stat.total_exercise_time
        avgExerciseTime = round(sumExerciseTime / recordCount)
        cumulativeStats = {
            'first_stat_date': datetime.datetime.strftime(firstStatDate, '%Y년 %m월 %d일'),
            'num_stats': recordCount,
            'sum_time': sumExerciseTime,
            'avg_exercise_week': avgWeekExerciseNum,
            'avg_time': avgExerciseTime,
        }
    else:
        cumulativeStats = {
            'num_stats': recordCount,
        }

    physicalStatList = PhysicalDataRecord.objects.filter(
        user_id=uuid).order_by('created_at')
    latestPhysicalStat = physicalStatList.last()
    physicalStat = [physicalStatList.count(
    ), PhysicalDataRecordSerializer(latestPhysicalStat).data]

    data = {
        'cumulative_stat': cumulativeStats,
        'exercise_time_stat': exerciseTimeStat,
        'physical_stat': physicalStat,
    }

    return Response(data=data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cumulativeExerciseStats(request):
    uuid = request.user.uuid
    exerciseStatData = {}
    exerciseStats = []
    weightTimeDict = {}
    cardioTime = 0
    maxTimeList = [0, 0]
    data = {}

    exerciseRecords = chain(ExerciseRecordCardio.objects.filter(
        user_id=uuid), ExerciseRecordWeight.objects.filter(user_id=uuid))

    for record in exerciseRecords:
        if record.exercise_id in exerciseStatData:
            exerciseStatData[record.exercise_id]['count'] += 1
            exerciseStatData[record.exercise_id]['time'] += round(
                (record.end_time - record.start_time).total_seconds())
        else:
            exerciseStatData[record.exercise_id] = {
                'count': 1,
                'time': round((record.end_time - record.start_time).total_seconds()),
            }

    for key, val in exerciseStatData.items():
        exerciseStat = {
            'exercise': ExerciseSerializer(Exercise.objects.get(id=key)).data,
            'count': val['count'],
            'time': val['time'],
        }
        exerciseStats.append(exerciseStat)

    exerciseStats = sorted(
        exerciseStats, key=lambda stat: stat['count'], reverse=True)

    if DailyExerciseStats.objects.filter(user_id=uuid):
        dailyStats = DailyExerciseStats.objects.filter(
            user_id=uuid)
        for stat in dailyStats:
            recordWeights = ExerciseRecordWeight.objects.filter(
                user_id=uuid, start_time__date=stat.day)
            recordCardio = ExerciseRecordCardio.objects.filter(
                user_id=uuid, start_time__date=stat.day)
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

            data = {
                'exercise_stats': exerciseStats,
                'category_stats': {
                    'weight': weightTimeDict,
                    'cardio': cardioTime,
                    'copy': categoryStatsCopy,
                },
            }
    else:
        print('man')
        data = {
            'exercise_stats': exerciseStats,
            'category_stats': {
                'weight': weightTimeDict,
                'cardio': cardioTime,
            },
        }

    return Response(data=data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def physicalData(request):
    uuid = request.user.uuid
    if request.method == 'POST':
        data = json.loads(request.body)
        height = UserDetailsStatic.objects.get(user_id=uuid).height / 100
        gender = UserDetailsStatic.objects.get(user_id=uuid).gender

        weight = data['weight']
        muscleMass = data['muscle_mass']
        bodyFatPercentage = data['body_fat_percentage']
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
        return HttpResponse(status=HTTPStatus.OK)

    elif request.method == 'GET':
        physicalDataRecords = PhysicalDataRecord.objects.filter(
            user_id=uuid).order_by('-created_at')
        currentPhysicalDataRecord = physicalDataRecords.first()
        weightStat, muscleMassStat, bodyFatPercentageStat, bmiStat, inbodyScoreStat = (
            {} for i in range(5))

        for record in physicalDataRecords:
            weightStat[datetime.datetime.strftime(
                record.created_at, '%Y-%m-%d')] = record.weight
            muscleMassStat[datetime.datetime.strftime(
                record.created_at, '%Y-%m-%d')] = record.muscle_mass
            bodyFatPercentageStat[datetime.datetime.strftime(
                record.created_at, '%Y-%m-%d')] = record.body_fat_percentage
            bmiStat[datetime.datetime.strftime(
                record.created_at, '%Y-%m-%d')] = record.bmi
            inbodyScoreStat[datetime.datetime.strftime(
                record.created_at, '%Y-%m-%d')] = record.inbody_score

        data = {
            'current_stat': {
                'height': UserDetailsStatic.objects.get(user_id=uuid).height,
                'weight': currentPhysicalDataRecord.weight,
                'muscle_mass': currentPhysicalDataRecord.muscle_mass,
                'body_fat_percentage': currentPhysicalDataRecord.body_fat_percentage,
                'bmi': currentPhysicalDataRecord.bmi,
                'inbody_score': currentPhysicalDataRecord.inbody_score,
            },
            'cumulative_stat': {
                'weight': weightStat,
                'muscle_mass': muscleMassStat,
                'body_fat_percentage': bodyFatPercentageStat,
                'bmi': bmiStat,
                'inbody_score': inbodyScoreStat,
            },
        }

        return Response(data=data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def exerciseStats(request):
    uuid = request.user.uuid
    exercise = Exercise.objects.get(id=request.GET['id'])
    data = {}
    if exercise.type == 0:
        if exercise.exercise_method == 1:
            count = 0
            records = ExerciseRecordWeight.objects.filter(
                user_id=uuid, exercise_id=exercise.id).order_by('-date')
            maxSetReps = maxTotalReps = 0
            bestSetRecordData, bestSessionRecordData = ([] for i in range(2))
            maxRepsStat, totalRepsStat = ({} for i in range(2))
            currentRecords = []

            for record in records:
                _sets = ExerciseRecordWeightSet.objects.filter(
                    exercise_record_weight_id=record.id)
                totalReps = 0
                maxReps = 0
                setData = []

                for _set in _sets:
                    totalReps += _set.record_reps
                    if maxReps < _set.record_reps:
                        maxReps = _set.record_reps
                    if count < 5:
                        setData.append(_set.record_reps)

                if maxSetReps < maxReps:
                    maxSetReps = maxReps
                    maxRepsSetRecordId = record.id
                if maxTotalReps < totalReps:
                    maxTotalReps = totalReps
                    maxTotalRepsRecordId = record.id

                maxRepsStat[datetime.datetime.strftime(
                    record.date, '%Y-%m-%d')] = maxReps
                totalRepsStat[datetime.datetime.strftime(
                    record.date, '%Y-%m-%d')] = totalReps

                if count < 5:
                    _recordData = ExerciseRecordBodyWeightSerializer(
                        record).data
                    _recordData['date'] = record.date
                    _recordData['sets'] = setData
                    currentRecords.append(_recordData)

            maxRepsSetRecord = records.get(id=maxRepsSetRecordId)
            _sets = ExerciseRecordWeightSet.objects.filter(
                exercise_record_weight_id=maxRepsSetRecord.id)
            for _set in _sets:
                bestSetRecordData.append(_set.record_reps)

            maxTotalRepsRecord = records.get(id=maxTotalRepsRecordId)
            _sets = ExerciseRecordWeightSet.objects.filter(
                exercise_record_weight_id=maxTotalRepsRecord.id)
            for _set in _sets:
                bestSessionRecordData.append(_set.record_reps)

            data = {
                'best_set': {
                    'reps': maxSetReps,
                    'record_data': bestSetRecordData,
                    'date': ExerciseRecordWeight.objects.get(id=maxRepsSetRecordId).date,
                },
                'best_session': {
                    'total_reps': maxTotalReps,
                    'record_data': bestSessionRecordData,
                    'date': ExerciseRecordWeight.objects.get(id=maxTotalRepsRecordId).date,
                },
                'max_reps_stat': maxRepsStat,
                'total_reps_stat': totalRepsStat,
                'current_records': currentRecords,
            }
        else:
            count = 0
            records = ExerciseRecordWeight.objects.filter(
                user_id=uuid, exercise_id=exercise.id).order_by('-date')
            best_one_rm = best_volume = 0
            maxOneRmStat, totalVolumeStat = ({} for i in range(2))
            currentRecords = []

            for record in records:
                _sets = ExerciseRecordWeightSet.objects.filter(
                    exercise_record_weight_id=record.id)

                setData = []

                if best_one_rm < record.max_one_rm:
                    best_one_rm = record.max_one_rm
                    maxOneRmRecordId = record.id
                if best_volume < record.total_volume:
                    best_volume = record.total_volume
                    maxTotalVolumeRecordId = record.id

                maxOneRmStat[datetime.datetime.strftime(
                    record.date, '%Y-%m-%d')] = record.max_one_rm
                totalVolumeStat[datetime.datetime.strftime(
                    record.date, '%Y-%m-%d')] = record.total_volume

                if count < 5:
                    for _set in _sets:
                        setData.append({
                            'record_weight': _set.record_weight,
                            'record_reps': _set.record_reps,
                        })
                    _recordData = ExerciseRecordWeightSerializer(
                        record).data
                    _recordData['date'] = record.date
                    _recordData['sets'] = setData
                    currentRecords.append(_recordData)

            maxOneRmRecord = records.get(id=maxOneRmRecordId)
            _sets = ExerciseRecordWeightSet.objects.filter(
                exercise_record_weight_id=maxOneRmRecord.id)
            for _set in _sets:
                if _set.one_rm == best_one_rm:
                    bestOneRmSetData = {
                        'one_rm': best_one_rm,
                        'date': maxOneRmRecord.date,
                        'set_num': _set.set_num,
                        'record_weight': _set.record_weight,
                        'record_reps': _set.record_reps,
                    }
                    break

            maxVolumeRecord = records.get(id=maxTotalVolumeRecordId)
            _sets = ExerciseRecordWeightSet.objects.filter(
                exercise_record_weight_id=maxVolumeRecord.id)
            bestVolumeRecordData = {
                'total_volume': best_volume,
                'date': maxVolumeRecord.date,
                'sets': [],
            }
            for _set in _sets:
                bestVolumeRecordData['sets'].append({
                    'record_weight': _set.record_weight,
                    'record_reps': _set.record_reps,
                })

            data = {
                'best_one_rm': bestOneRmSetData,
                'best_volume': bestVolumeRecordData,
                'max_one_rm_stat': maxOneRmStat,
                'total_volume_stat': totalVolumeStat,
                'current_records': currentRecords,
            }

    else:
        count = 0
        records = ExerciseRecordCardio.objects.filter(
            user_id=uuid, exercise_id=exercise.id).order_by('-date')
        maxCalories = 0
        distanceStat, durationStat, caloriesStat = ({} for i in range(3))
        currentRecords = []

        for record in records:
            if maxCalories < record.record_calories:
                maxCalories = record.record_calories
                maxCaloriesRecordId = record.id

            if datetime.datetime.strftime(record.date, '%Y-%m-%d') not in distanceStat:
                distanceStat[datetime.datetime.strftime(
                    record.date, '%Y-%m-%d')] = record.record_distance
            else:
                distanceStat[datetime.datetime.strftime(
                    record.date, '%Y-%m-%d')] += record.record_distance
            if datetime.datetime.strftime(record.date, '%Y-%m-%d') not in durationStat:
                durationStat[datetime.datetime.strftime(
                    record.date, '%Y-%m-%d')] = record.record_duration
            else:
                durationStat[datetime.datetime.strftime(
                    record.date, '%Y-%m-%d')] += record.record_duration
            if datetime.datetime.strftime(record.date, '%Y-%m-%d') not in caloriesStat:
                caloriesStat[datetime.datetime.strftime(
                    record.date, '%Y-%m-%d')] = record.record_calories
            else:
                caloriesStat[datetime.datetime.strftime(
                    record.date, '%Y-%m-%d')] += record.record_calories

            if count < 5:
                _recordData = ExerciseRecordCardioSerializer(record).data
                _plan = ExercisePlanCardio.objects.get(id=record.exercise_plan_cardio_id)
                _recordData['date'] = record.date
                _recordData['target_duration'] = _plan.target_duration
                _recordData['target_distance'] = _plan.target_distance
                currentRecords.append(_recordData)

        maxCaloriesRecord = records.get(id=maxCaloriesRecordId)
        maxCaloriesData = ExerciseRecordCardioSerializer(
            maxCaloriesRecord).data
        maxCaloriesData['date'] = maxCaloriesRecord.date

        data = {
            'max_calories': maxCaloriesData,
            'record_distance_stat': distanceStat,
            'record_duration_stat': durationStat,
            'record_calories_stat': caloriesStat,
            'current_records': currentRecords,
        }

    return Response(data=data)
