# Generated by Django 3.2.8 on 2022-02-20 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0008_remove_dailyexercisestats_total_reps'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyexercisestats',
            name='total_calories',
            field=models.FloatField(default=0),
        ),
    ]
