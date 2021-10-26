from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import datetime
import json
from .models import *
from .serializers import ExerciseDetailsSerializer, ExercisePlanWeightSerializer, ExerciseRecordWeightSerializer, ExerciseSerializer, TodayExerciseTimeSerializer, UserAllExerciseRecordWeightSerializer, UserExercisePlanWeightSerializer, UserExercisePlanWeightSetSerializer, UserExercisePlanWeightSetsSerializer, UserExerciseRecordWeightSerializer, UserExerciseRecordWeightSetsSerializer
# Create your views here.


@api_view(['GET'])
def getExercise(request):
    targetMuscle = request.GET['target_muscle']
    exerciseMethod = request.GET['exercise_method']
    exerciseList = Exercise.objects.filter(
        target_muscle=targetMuscle, exercise_method=exerciseMethod)
    serializer = ExerciseSerializer(exerciseList, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getTodayExerciseTime(request):
    date = request.GET['date']
    userId = request.GET['user_id']
    duration = datetime.timedelta
    parsedDate = datetime.datetime.strptime(date, '%m/%d/%Y')
    exerciseRecords = ExerciseRecordAerobic.objects.filter(date=parsedDate, user_id=userId).extend(
        ExerciseRecordWeight.objects.filter(date=parsedDate, user_id=userId))
    for record in exerciseRecords:
        diff = record.end_time - record.start_time
        duration += diff
    serializer = TodayExerciseTimeSerializer(duration)
    return Response(serializer.data)

@api_view(['GET'])
def getExerciseDetails(request):
    exercise_id = request.GET['exercise_id']
    details = ExerciseDetails.objects.filter(exercise = exercise_id)
    serializer = ExerciseDetailsSerializer(details)
    return Response(serializer.data)

@api_view(['GET'])
def getUserExercisePlanWeight(request):
    userId = request.GET('user_id')
    exerciseId = request.GET('exercise_id')
    plan = ExercisePlanWeight.objects.filter(user = userId, exercise = exerciseId)
    serializer = UserExercisePlanWeightSerializer(plan, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def getUserExercisePlanWeightSets(request):
    planId = request.GET('exercise_plan_weight_id')
    plan_sets = ExercisePlanWeightSet.objects.filter(exercise_plan_weight = planId)
    serializer = UserExercisePlanWeightSetsSerializer(plan_sets, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def getUserAllExerciseRecordWeight(request):
    userId = request.GET('user_id')
    record = ExerciseRecordWeight.objects.filter(user = userId)
    serializer = UserExerciseRecordWeightSerializer(record, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def getUserExerciseRecordWeight(request):
    userId = request.GET('user_id')
    date = request.GET('date')
    parsedDate = datetime.datetime.strptime(date, '%m/%d/%Y')
    record = ExerciseRecordWeight(user = userId, date = parsedDate)
    serializer = UserExerciseRecordWeightSerializer(record, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def getUserExerciseRecordWeightSets(request):
    record_id = request.GET('exercise_record_weight_id')
    record_sets = ExerciseRecordWeightSet.objects.filter(exercise_record_weight = record_id)
    serializer = UserExerciseRecordWeightSetsSerializer(record_sets, many = True)
    return Response(serializer.data)

@api_view(['POST'])
def postUserExercisePlanWeight(request):
    request = json.loads(request.body)
    plan = ExercisePlanWeight(user = request['user'], exercise = request['exercise'], date = request['date'], set_num = request['set_num'])
    plan.save()

    sets = request['sets']
    for set in sets:
        data = ExercisePlanWeightSet(exercise_plan_weight = set[''], set_num = set['set_num'], target_weight = set['target_weight'], target_reps = set['target_reps'])
        data.save()
    return HttpResponse(status = 200)