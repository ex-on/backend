# Generated by Django 3.2.8 on 2022-02-18 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0006_auto_20220209_2337'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyexercisestats',
            name='total_reps',
            field=models.IntegerField(default=0),
        ),
    ]
