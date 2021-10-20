from django.urls import path, include
from .views import getExercise, getTodayExerciseTime

urlpatterns = [
    path("list", getExercise), #target_muscle & exercise_method
    path("time", getTodayExerciseTime), #date & user_id
]
