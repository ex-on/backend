from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import datetime
from .models import *
from .serializers import ExerciseSerializer, TodayExerciseTimeSerializer
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
