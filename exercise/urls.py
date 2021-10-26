from django.urls import path
from .views import getExercise, getExerciseDetails,  getTodayExerciseTime, getUserAllExerciseRecordWeight, getUserExercisePlanWeight, getUserExercisePlanWeightSets, getUserExerciseRecordWeight, getUserExerciseRecordWeightSets, postUserExercisePlanWeight


urlpatterns = [
    path("list", getExercise), #target_muscle & exercise_method
    path("time", getTodayExerciseTime), #date & user_id
    path("details", getExerciseDetails), #exercise_id
    path("plan_weight", getUserExercisePlanWeight), #user_id & exercise_id
    path('plan_weight_sets', getUserExercisePlanWeightSets), #exercise_plan_weight_id
    path('record_weight', getUserAllExerciseRecordWeight), #user_id
    path('record_weight_date', getUserExerciseRecordWeight), #user_id & date
    path('record_weight_sets', getUserExerciseRecordWeightSets), #exercise_record_weight_id
    path('test', postUserExercisePlanWeight),
]