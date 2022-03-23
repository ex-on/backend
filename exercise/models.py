from django.db import models
from django.db.models.query_utils import Q
# Create your models here


class Exercise(models.Model):
    name = models.CharField(max_length=20)
    type = models.IntegerField()
    target_muscle = models.IntegerField(null=True)
    exercise_method = models.IntegerField()
    cardio_met = models.FloatField(null=True)

    class Meta:
        managed = True
        db_table = 'exercise'


class ExerciseDetails(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    recommended_duration = models.IntegerField()
    info_text = models.CharField(max_length=500)

    class Meta:
        managed = True
        db_table = 'exercise_details'


class ExercisePlanCardio(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    target_distance = models.FloatField(null=True)
    target_duration = models.IntegerField(null=True)
    completed = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'exercise_plan_cardio'
        constraints = [
            models.CheckConstraint(
                check=Q(target_distance__isnull=False) | Q(target_duration__isnull=False),
                name='not_both_null'
            )
        ]


class ExercisePlanWeight(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    num_sets = models.IntegerField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'exercise_plan_weight'


class ExercisePlanWeightSet(models.Model):
    exercise_plan_weight = models.ForeignKey(
        ExercisePlanWeight, on_delete=models.CASCADE)
    set_num = models.IntegerField()
    target_weight = models.FloatField()
    target_reps = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'exercise_plan_weight_set'


class ExerciseRecordCardio(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    exercise_plan_cardio = models.ForeignKey(
        ExercisePlanCardio, on_delete=models.CASCADE)
    record_distance = models.FloatField(null=True)
    record_duration = models.IntegerField()
    record_calories = models.FloatField()
    date = models.DateField(auto_now_add=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'exercise_record_cardio'

class ExerciseRecordWeight(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    exercise_plan_weight = models.ForeignKey(
        ExercisePlanWeight, on_delete=models.CASCADE)
    total_sets = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    exercise_time = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_volume = models.FloatField()
    max_one_rm = models.FloatField()
    total_reps = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'exercise_record_weight'


class ExerciseRecordWeightSet(models.Model):
    exercise_record_weight = models.ForeignKey(
        ExerciseRecordWeight, on_delete=models.CASCADE)
    record_weight = models.FloatField()
    record_reps = models.IntegerField()
    set_num = models.IntegerField(blank=True, null=True)
    one_rm = models.FloatField()

    class Meta:
        managed = True
        db_table = 'exercise_record_weight_set'
