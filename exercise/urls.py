from django.urls import path
from .views import *

urlpatterns = [
    path("list", getAllExercise), #전체 운동 종류
    path('post_exercise_plan_weight', postExercisePlanWeight), #user_id & exercise_id & date & num_sets & sets
    path('post_exercise_plan_cardio', postExercisePlanCardio),
    path("status_week", getExerciseStatusWeek),
    path("status_date", getExerciseStatusDate), 
    path('plan_weight_sets', getExercisePlanWeightSets), #exercise_plan_weight_id -> plan의 세부 계획
    path('record_weight', exerciseRecordWeight),
    path('record_cardio', exerciseRecordCardio),
    path('recent', recentExercisePlan),
]