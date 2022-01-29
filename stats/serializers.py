from rest_framework import serializers
from .models import *


class DailyExerciseStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyExerciseStats
        fields = ('total_exercise_time', 'total_sets', 'max_one_rm',
                  'total_volume', 'total_distance', 'memo',)
