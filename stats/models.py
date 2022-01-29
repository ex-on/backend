from django.db import models

# Create your models here.
class DailyExerciseStats(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    total_exercise_time = models.IntegerField(default=0)
    total_sets = models.IntegerField(default=0)
    max_one_rm = models.FloatField(default=0)
    total_volume = models.FloatField(default=0)
    total_distance = models.FloatField(default=0)
    day = models.DateField(auto_now_add=True)
    memo = models.CharField(max_length=300, null=True)

    class Meta:
        managed = True
        db_table = 'daily_exercise_stats'