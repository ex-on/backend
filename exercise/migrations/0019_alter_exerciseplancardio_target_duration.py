# Generated by Django 3.2.8 on 2022-02-18 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercise', '0018_auto_20220218_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exerciseplancardio',
            name='target_duration',
            field=models.IntegerField(null=True),
        ),
    ]
