# Generated by Django 3.2.8 on 2022-01-21 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercise', '0009_dailyexerciserecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyexerciserecord',
            name='memo',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
