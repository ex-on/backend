from django.db.models import fields
from rest_framework import serializers
from .models import ExercisePlanWeight, ExercisePlanWeightSet, Exercise, ExerciseDetails, ExercisePlanAerobic, ExerciseRecordWeight, ExerciseRecordWeightSet, ExerciseRecordAerobic


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ('id', 'name', 'target_muscle', 'exercise_method',)


class ExerciseDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExerciseDetails
        fields = ('exercise', 'recommended_duration', 'info_text')


class ExercisePlanWeightSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExercisePlanWeight
        fields = ('id', 'num_sets')


class ExercisePlanWeightSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExercisePlanWeightSet
        fields = ('set_num',
                  'target_weight', 'target_reps')


class ExercisePlanAerobicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExercisePlanAerobic
        fields = ('user_id', 'exercise_id', 'date',
                  'target_distance', 'target_duration')

############ 운동 기록 조회 ################


class ExerciseRecordWeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseRecordWeight
        fields = ('user_id', 'exercise_id', 'exercise_plan_weight_id',
                  'total_sets', 'date', 'start_time', 'end_time', 'target_muscle')


class ExerciseRecordWeightSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseRecordWeightSet
        fields = ('exercise_record_weight_id', 'record_weight',
                  'record_reps', 'start_time', 'end_time', 'set_num')


class ExerciseRecordAerobicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseRecordAerobic
        fields = ('user_id', 'exercise_plan_aerobic_id', 'record_distance',
                  'record_duration', 'date', 'start_time', 'end_time', 'exercise_id')


class ExerciseTimeSerializer(serializers.Serializer):
    duration = serializers.DurationField()
