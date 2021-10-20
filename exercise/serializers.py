from django.db.models import fields
from rest_framework import serializers
from .models import Exercise


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ('name', 'target_muscle', 'exercise_method', 'difficulty',)


class TodayExerciseTimeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('duration')

