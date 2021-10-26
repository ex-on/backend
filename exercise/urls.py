from django.urls import path
from .views import getExercise, getExerciseDetails, getExercisePlanWeight, getExerciseRecordWeight, getExerciseRecordWeightDate, getTodayExerciseTime


urlpatterns = [
    path("list", getExercise), #target_muscle & exercise_method
    path("time", getTodayExerciseTime), #date & user_id
    path("details", getExerciseDetails), #exercise_id
    path("plan_weight", getExercisePlanWeight), #user_id & exercise_id
    path('record_weight', getExerciseRecordWeight), #user_id
    path('record_weight_date', getExerciseRecordWeightDate), #user_id & date
]