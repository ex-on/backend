from django.urls import path, include
from .views import getExercise, getExerciseDetails, getExercisePlanWeight,  getTodayExerciseTime, getUserAllExerciseRecordWeight, getUserExercisePlanWeight, getUserExercisePlanWeightSets, getUserExerciseRecordWeight, getUserExerciseRecordWeightSets, getUserRecentRecordWeight, postUserExercisePlanWeight, postUserExerciseRecordWeight

urlpatterns = [
    path("list", getExercise), #target_muscle & exercise_method
    path("time", getTodayExerciseTime), #date & user_id
    path("details", getExerciseDetails), #exercise_id
    path("plan_weight", getUserExercisePlanWeight), #user_id & exercise_id
    path('plan_weight_sets', getUserExercisePlanWeightSets), #exercise_plan_weight_id
    path('record_weight', getUserAllExerciseRecordWeight), #user_id
    path('record_weight_date', getUserExerciseRecordWeight), #user_id & date
    path('record_weight_sets', getUserExerciseRecordWeightSets), #exercise_record_weight_id
    path('recent_record_weight', getUserRecentRecordWeight), #user_id & exercise_id
    path('post_exercise_plan_weight', postUserExercisePlanWeight), #user_id & exercise_id & date & num_sets & sets
    path('exercise_plan_weight', getExercisePlanWeight), #exercise_plan_weight_id
    path('post_exercise_record_weight', postUserExerciseRecordWeight),
]