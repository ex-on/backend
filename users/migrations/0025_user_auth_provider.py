# Generated by Django 3.2.8 on 2022-04-15 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_remove_userdetailscount_answer_acception_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='auth_provider',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
