# Generated by Django 3.2.8 on 2021-12-10 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercise', '0003_remove_exercise_difficulty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='name',
            field=models.CharField(max_length=20),
        ),
    ]