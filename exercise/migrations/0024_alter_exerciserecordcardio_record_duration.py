# Generated by Django 3.2.8 on 2022-02-19 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercise', '0023_alter_exerciserecordcardio_record_distance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exerciserecordcardio',
            name='record_duration',
            field=models.IntegerField(),
        ),
    ]
