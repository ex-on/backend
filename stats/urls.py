from django.urls import path
from .views import *

urlpatterns = [
    path('daily', dailyExerciseStats),
    path('daily_memo', dailyExerciseStatsMemo),
    path('weekly', weeklyExerciseStats),
    path('monthly', monthlyExerciseStats),
    path('monthly_date', monthlyExerciseDates),
]
