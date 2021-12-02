# Generated by Django 3.2.8 on 2021-12-01 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('target_muscle', models.IntegerField()),
                ('exercise_method', models.IntegerField()),
                ('difficulty', models.IntegerField()),
            ],
            options={
                'db_table': 'exercise',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ExerciseDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recommended_duration', models.IntegerField()),
                ('info_text', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'exercise_details',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ExercisePlanAerobic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('target_distance', models.FloatField()),
                ('target_duration', models.TimeField()),
            ],
            options={
                'db_table': 'exercise_plan_aerobic',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ExercisePlanWeight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('num_sets', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'exercise_plan_weight',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ExercisePlanWeightSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('set_num', models.IntegerField()),
                ('target_weight', models.FloatField()),
                ('target_reps', models.IntegerField()),
            ],
            options={
                'db_table': 'exercise_plan_weight_set',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ExerciseRecordAerobic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_distance', models.FloatField()),
                ('record_duration', models.FloatField()),
                ('date', models.DateField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'exercise_record_aerobic',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ExerciseRecordAerobicRest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.IntegerField()),
                ('end_time', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'exercise_record_aerobic_rest',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ExerciseRecordWeight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_sets', models.IntegerField()),
                ('date', models.DateField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='exercise.exercise')),
                ('exercise_plan_weight', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='exercise.exerciseplanweight')),
            ],
            options={
                'db_table': 'exercise_record_weight',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ExerciseRecordWeightSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_weight', models.FloatField()),
                ('record_reps', models.IntegerField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('set_num', models.IntegerField(blank=True, null=True)),
                ('exercise_record_weight', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='exercise.exerciserecordweight')),
            ],
            options={
                'db_table': 'exercise_record_weight_set',
                'managed': True,
            },
        ),
    ]
