from rest_framework import serializers
from .models import ExercisePlanWeight, ExercisePlanWeightSet, Exercise, ExerciseDetails, ExercisePlanCardio, ExerciseRecordWeight, ExerciseRecordWeightSet, ExerciseRecordCardio


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


class ExercisePlanCardioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExercisePlanCardio
        fields = ('id',
                  'target_distance', 'target_duration')

############ 운동 기록 조회 ################


class ExerciseRecordWeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseRecordWeight
        fields = ('total_sets', 'exercise_time',
                  'total_volume', 'max_one_rm', 'total_reps',)


class ExerciseRecordBodyWeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseRecordWeight
        fields = ('total_sets', 'exercise_time',
                  'total_reps',)


class ExerciseRecordWeightSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseRecordWeightSet
        fields = ('record_weight',
                  'record_reps', 'set_num')


class ExerciseRecordCardioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseRecordCardio
        fields = ('record_distance',
                  'record_duration',
                  'record_calories')


class ExerciseTimeSerializer(serializers.Serializer):
    duration = serializers.DurationField()
