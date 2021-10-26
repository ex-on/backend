from django.db.models import fields
from rest_framework import serializers
from .models import ExcercisePlanWeightSet, Exercise, ExerciseDetails, ExercisePlanWeight, ExerciseRecordWeight, ExerciseRecordWeightSet


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ('name', 'target_muscle', 'exercise_method', 'difficulty',)


class TodayExerciseTimeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('duration')

class ExerciseDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExerciseDetails
        fields = ('exercise', 'recommended_duration', 'info_text')

class UserExercisePlanWeightSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExercisePlanWeight
        fields = ('user', 'exercise', 'date', 'num_sets')

class UserExercisePlanWeightSetsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExcercisePlanWeightSet
        fields = ('exercise_plan_weight', 'set_num', 'target_weight', 'target_reps')

class UserExerciseRecordWeightSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExerciseRecordWeight
        fields = ('user', 'exercise_pla_weight_id', 'total_sets', 'date', 'start_time', 'end_time')

class UserExerciseRecordWeightSetsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExerciseRecordWeightSet
        fields = ('exercise_record_weight', 'record_weight', 'record_reps', 'start_time', 'end_time', 'set_num')