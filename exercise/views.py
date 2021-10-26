from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import datetime
from .models import *
from .serializers import ExerciseDetailsSerializer, ExercisePlanWeightSerializer, ExerciseRecordWeightSerializer, ExerciseSerializer, TodayExerciseTimeSerializer
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
def getExercisePlanWeight(request):
    userId = request.GET('user_id')
    exerciseId = request.GET('exercise_id')
    plan = ExercisePlanWeight.objects.filter(user = userId, exercise = exerciseId)
    serializer = ExercisePlanWeightSerializer(plan, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def getExerciseRecordWeight(request):
    userId = request.GET('user_id')
    record = ExerciseRecordWeight.objects.filter(user = userId)
    serializer = ExerciseRecordWeightSerializer(record, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def getExerciseRecordWeightDate(request):
    userId = request.GET('user_id')
    date = request.GET('date')
    parsedDate = datetime.datetime.strptime(date, '%m/%d/%Y')
    record = ExerciseRecordWeight(user = userId, date = parsedDate)
    serializer = ExerciseRecordWeightSerializer(record, many = True)
    return Response(serializer.data)