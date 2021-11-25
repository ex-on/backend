from django.db.models import fields
from rest_framework import serializers
from .models import ExercisePlanAerobic, ExercisePlanWeightSet, Exercise, ExerciseDetails, ExercisePlanWeight, ExercisePlanWeightSets, ExerciseRecordAerobic, ExerciseRecordWeight, ExerciseRecordWeightSet

########## 운동 종류 및 세부 정보 조회 ###########
class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ('name', 'target_muscle', 'exercise_method', 'difficulty')
class ExerciseDetailsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ExerciseDetails
        fields = ('exercise_id', 'recommended_duration', 'info_text')

######### 운동 계획 조회 ################
class ExercisePlanWeightSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ExercisePlanWeight
        fields = ('user', 'exercise', 'date', 'num_sets')
class ExercisePlanWeightSetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExercisePlanWeightSets
        fields = ('exercise_plan_weight', 'set_num', 'target_weight', 'target_reps')

class ExercisePlanAerobicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExercisePlanAerobic
        fields = ('user', 'exercise', 'date', 'target_distance', 'target_duration')

############ 운동 기록 조회 ################
class ExerciseRecordWeightSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ExerciseRecordWeight
        fields = ('user', 'exercise_plan_weight_id', 'total_sets', 'date', 'start_time', 'end_time', 'target_muscle')
class UserExerciseRecordWeightSetsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExerciseRecordWeightSet
        fields = ('exercise_record_weight', 'record_weight', 'record_reps', 'start_time', 'end_time', 'set_num')
class ExerciseRecordAerobicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseRecordAerobic
        fields = ('user', 'exercise_plan_aerobic', 'record_distance', 'record_duration', 'date', 'start_time', 'end_time')
class ExerciseTimeSerializer(serializers.Serializer):
    duration = serializers.DurationField()