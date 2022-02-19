from django.urls import path
from .views import *

urlpatterns = [
    path('daily', dailyExerciseStats),
    path('daily_memo', dailyExerciseStatsMemo),
    path('weekly', weeklyExerciseStats),
    path('monthly', monthlyExerciseStats),
    path('monthly_date', monthlyExerciseDates),
    path('cumulative_time', cumulativeTimeStats),
    path('cumulative_exercise', cumulativeExerciseStats),
    path('exercise', exerciseStats),
    path('physical_data', physicalData),
]
