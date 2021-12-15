from django.urls import path
from .views import getAllExercise, getExerciseByExerciseMethod, getExerciseByTargetMuscle, getExerciseByTargetMuscleExerciseMethod, getExerciseDetails, getExerciseTime, getUserPlanAerobicDate, getExercisePlanWeightDate, getExercisePlanWeightSets, getUserRecordAerobic, getUserRecordAerobicDate, getUserRecordWeight, getUserRecordWeightDate, getUserRecordWeightSets, getUserRecordWeightTargetMuscle, postExercisePlanAerobic, postExercisePlanWeight, postExerciseRecordAerobic, postExerciseRecordWeight

urlpatterns = [
    ####### 운동 종류 및 세부 정보 조회 #######
    path("list", getAllExercise), #전체 운동 종류
    path("list_target_muscle", getExerciseByTargetMuscle), #특정 부위 운동 종류
    path("list_exercise_method", getExerciseByExerciseMethod), #특정 운동 방법 운동 종류
    path("list_target_muscle_exercise_method", getExerciseByTargetMuscleExerciseMethod), #특정 부위 & 특정 운동 방법 운동 종류
    path("details", getExerciseDetails), #특정 운동의 세부 정보
    ####### 운동 계획 조회 ###################
    path("plan_weight_date", getExercisePlanWeightDate), #weight 운동 계획 날짜별 조회
    path('plan_weight_sets', getExercisePlanWeightSets), #exercise_plan_weight_id -> plan의 세부 계획
    path('plan_aerobic_date', getUserPlanAerobicDate), #exercise_plan_weight_id
    ####### 운동 기록 조회 ###################
    path('record_weight', getUserRecordWeight), #user_id -> user의 전체 운동 기록
    path('record_weight_date', getUserRecordWeightDate), #user_id & date -> user 특정 날짜의 운동 기록
    path('record_weight_target_muscle', getUserRecordWeightTargetMuscle),
    path('record_weight_sets', getUserRecordWeightSets), #exercise_record_weight_id -> 특정 운동 기록의 세부 
    path('record_aerobic', getUserRecordAerobic),
    path('record_aerobic_date', getUserRecordAerobicDate),
    path("exercise_time", getExerciseTime), #date & user_id -> 해당 날짜 동안 user가 운동한 시간
    ####### 운동 계획 및 기록 등록 ###########
    path('post_exercise_plan_weight', postExercisePlanWeight), #user_id & exercise_id & date & num_sets & sets
    path('post_exercise_plan_aerobic', postExercisePlanAerobic),
    path('post_exercise_record_weight', postExerciseRecordWeight),
    path('post_exercise_record_aerobic', postExerciseRecordAerobic),
]