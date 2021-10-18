from django.db import models
# Create your models here.
class Excercise(models.Model):
    name = models.CharField(max_length=15)
    target_muscle = models.IntegerField()
    excercise_method = models.IntegerField()
    difficulty = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'excercise'

class ExcerciseDetails(models.Model):
    excercise = models.ForeignKey(Excercise, models.DO_NOTHING)
    recommended_duration = models.IntegerField()
    info_text = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'excercise_details'


class ExcercisePlanAerobic(models.Model):
    user = models.ForeignKey('users.User', models.DO_NOTHING)
    excercise = models.ForeignKey(Excercise, models.DO_NOTHING)
    date = models.DateField()
    target_distance = models.FloatField()
    target_duration = models.TimeField()

    class Meta:
        managed = False
        db_table = 'excercise_plan_aerobic'


class ExcercisePlanWeight(models.Model):
    user = models.ForeignKey('users.User', models.DO_NOTHING)
    excercise = models.ForeignKey(Excercise, models.DO_NOTHING)
    date = models.DateField()
    num_sets = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'excercise_plan_weight'


class ExcercisePlanWeightSet(models.Model):
    excercise_plan_weight = models.ForeignKey(ExcercisePlanWeight, models.DO_NOTHING)
    set_num = models.IntegerField()
    target_weight = models.FloatField()
    target_reps = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'excercise_plan_weight_set'


class ExcerciseRecordAerobic(models.Model):
    excercise_plan_aerobic = models.ForeignKey(ExcercisePlanAerobic, models.DO_NOTHING)
    record_distance = models.FloatField()
    record_duration = models.FloatField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'excercise_record_aerobic'


class ExcerciseRecordAerobicRest(models.Model):
    excercise_record_aerobic = models.ForeignKey(ExcerciseRecordAerobic, models.DO_NOTHING)
    start_time = models.IntegerField()
    end_time = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'excercise_record_aerobic_rest'


class ExcerciseRecordWeight(models.Model):
    excercise_plan_weight_id = models.IntegerField()
    total_sets = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'excercise_record_weight'


class ExcerciseRecordWeightSet(models.Model):
    excercise_record_weight = models.ForeignKey(ExcerciseRecordWeight, models.DO_NOTHING)
    record_weight = models.FloatField()
    record_reps = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    set_num = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'excercise_record_weight_set'