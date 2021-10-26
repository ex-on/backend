from django.db.models import fields
from rest_framework import serializers
from .models import Exercise, ExerciseDetails, ExercisePlanWeight, ExerciseRecordWeight


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

class ExercisePlanWeightSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExercisePlanWeight
        fields = ('user', 'exercise', 'date', 'num_sets')

class ExerciseRecordWeightSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExerciseRecordWeight
        fields = ('user', 'exercise_pla_weight_id', 'total_sets', 'date', 'start_time', 'end_time')