from django.urls import path
from .views import getExercise, getExerciseByExerciseMethod, getExerciseByTargetMuscle, getExerciseByTargetMuscleExerciseMethod, getExerciseDetails, getExerciseTime, getUserPlanAerobicDate, getUserPlanWeightDate, getUserPlanWeightSets, getUserRecordAerobic, getUserRecordAerobicDate, getUserRecordWeight, getUserRecordWeightDate, getUserRecordWeightSets, getUserRecordWeightTargetMuscle, postUserExercisePlanAerobic, postUserExercisePlanWeight, postUserExerciseRecordAerobic, postUserExerciseRecordWeight

urlpatterns = [
    ####### 운동 종류 및 세부 정보 조회 #######
    path("list", getExercise),  # 전체 운동 종류
    path("list_target_muscle", getExerciseByTargetMuscle),  # 특정 부위 운동 종류
    path("list_exercise_method", getExerciseByExerciseMethod),  # 특정 운동 방법 운동 종류
    path("list_target_muscle_exercise_method",
         getExerciseByTargetMuscleExerciseMethod),  # 특정 부위 & 특정 운동 방법 운동 종류
    path("details", getExerciseDetails),  # 특정 운동의 세부 정보
    ####### 운동 계획 조회 ###################
    path("plan_weight_date", getUserPlanWeightDate),  # weight 운동 계획 날짜별 조회
    # exercise_plan_weight_id -> plan의 세부 계획
    path('plan_weight_sets', getUserPlanWeightSets),
    # exercise_plan_weight_id
    path('plan_aerobic_date', getUserPlanAerobicDate),
    ####### 운동 기록 조회 ###################
    path('record_weight', getUserRecordWeight),  # user_id -> user의 전체 운동 기록
    # user_id & date -> user 특정 날짜의 운동 기록
    path('record_weight_date', getUserRecordWeightDate),
    path('record_weight_target_muscle', getUserRecordWeightTargetMuscle),
    # exercise_record_weight_id -> 특정 운동 기록의 세부
    path('record_weight_sets', getUserRecordWeightSets),
    path('record_aerobic', getUserRecordAerobic),
    path('record_aerobic_date', getUserRecordAerobicDate),
    # date & user_id -> 해당 날짜 동안 user가 운동한 시간
    path("exercise_time", getExerciseTime),
    ####### 운동 계획 및 기록 등록 ###########
    # user_id & exercise_id & date & num_sets & sets
    path('post_exercise_plan_weight', postUserExercisePlanWeight),
    path('post_exercise_plan_aerobic', postUserExercisePlanAerobic),
    path('post_exercise_record_weight', postUserExerciseRecordWeight),
    path('post_exercise_record_aerobic', postUserExerciseRecordAerobic),
]
