# Generated by Django 3.2.8 on 2022-02-09 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0003_auto_20220208_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='physicaldatarecord',
            name='bmi',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='physicaldatarecord',
            name='inBodyScore',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='physicaldatarecord',
            name='body_fat_percentage',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='physicaldatarecord',
            name='muscle_mass',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='physicaldatarecord',
            name='weight',
            field=models.FloatField(null=True),
        ),
    ]
