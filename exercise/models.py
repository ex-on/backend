from django.db import models
# Create your models here


class Exercise(models.Model):
    name = models.CharField(max_length=20)
    target_muscle = models.IntegerField()
    exercise_method = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'exercise'


class ExerciseDetails(models.Model):
    exercise = models.ForeignKey(Exercise, models.DO_NOTHING)
    recommended_duration = models.IntegerField()
    info_text = models.CharField(max_length=500)

    class Meta:
        managed = True
        db_table = 'exercise_details'


class ExercisePlanAerobic(models.Model):
    user = models.ForeignKey('users.User', models.DO_NOTHING)
    exercise = models.ForeignKey(Exercise, models.DO_NOTHING)
    date = models.DateField()
    target_distance = models.FloatField()
    target_duration = models.TimeField()

    class Meta:
        managed = True
        db_table = 'exercise_plan_aerobic'


class ExercisePlanWeight(models.Model):
    user = models.ForeignKey('users.User', models.DO_NOTHING)
    exercise = models.ForeignKey(Exercise, models.DO_NOTHING)
    date = models.DateField(auto_now_add=True)
    num_sets = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'exercise_plan_weight'


class ExercisePlanWeightSet(models.Model):
    exercise_plan_weight = models.ForeignKey(
        ExercisePlanWeight, models.DO_NOTHING)
    set_num = models.IntegerField()
    target_weight = models.FloatField()
    target_reps = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'exercise_plan_weight_set'


class ExerciseRecordAerobic(models.Model):
    user = models.ForeignKey('users.User', models.DO_NOTHING)
    exercise_plan_aerobic = models.ForeignKey(
        ExercisePlanAerobic, models.DO_NOTHING)
    record_distance = models.FloatField()
    record_duration = models.FloatField()
    date = models.DateField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'exercise_record_aerobic'


class ExerciseRecordAerobicRest(models.Model):
    exercise_record_aerobic = models.ForeignKey(
        ExerciseRecordAerobic, models.DO_NOTHING)
    start_time = models.IntegerField()
    end_time = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'exercise_record_aerobic_rest'


class ExerciseRecordWeight(models.Model):
    user = models.ForeignKey('users.User', models.DO_NOTHING)
    exercise = models.ForeignKey(Exercise, models.DO_NOTHING)
    exercise_plan_weight = models.ForeignKey(
        ExercisePlanWeight, models.DO_NOTHING)
    total_sets = models.IntegerField()
    date = models.DateField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'exercise_record_weight'


class ExerciseRecordWeightSet(models.Model):
    exercise_record_weight = models.ForeignKey(
        ExerciseRecordWeight, models.DO_NOTHING)
    record_weight = models.FloatField()
    record_reps = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    set_num = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'exercise_record_weight_set'
