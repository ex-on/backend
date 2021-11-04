# Generated by Django 3.2.8 on 2021-11-04 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=30)),
                ('username', models.CharField(max_length=15)),
                ('email', models.CharField(max_length=45)),
                ('phone_number', models.CharField(max_length=11)),
            ],
            options={
                'db_table': 'user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserDetailsCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_liked_posts', models.IntegerField()),
                ('count_saved_posts', models.IntegerField()),
                ('count_uploaded_posts', models.IntegerField()),
                ('count_uploaded_qna_posts', models.IntegerField()),
                ('count_uploaded_answers', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'user_details_count',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserDetailsStatic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.IntegerField()),
                ('activity_level', models.IntegerField()),
                ('physical_level', models.IntegerField(blank=True, null=True)),
                ('intro_text', models.CharField(blank=True, max_length=30, null=True)),
                ('profile_icon', models.IntegerField()),
            ],
            options={
                'db_table': 'user_details_static',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserPhysicalData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('weight', models.FloatField(blank=True, null=True)),
                ('skeletal_muscle_mass', models.FloatField(blank=True, null=True)),
                ('body_fat_percentage', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'user_physical_data',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UsersLikedPosts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'users_liked_posts',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UsersLikedQnaPosts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'users_liked_qna_posts',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UsersSavedPosts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'users_saved_posts',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UsersSavedQnaPosts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'users_saved_qna_posts',
                'managed': False,
            },
        ),
    ]
