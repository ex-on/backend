from django.db import models
# Create your models here.
class User(models.Model):
    password = models.CharField(max_length=30)
    username = models.CharField(max_length=15)
    email = models.CharField(max_length=45)
    phone_number = models.CharField(max_length=11)

    class Meta:
        managed = False
        db_table = 'user'


class UserDetailsCount(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    count_liked_posts = models.IntegerField()
    count_saved_posts = models.IntegerField()
    count_uploaded_posts = models.IntegerField()
    count_uploaded_qna_posts = models.IntegerField()
    count_uploaded_answers = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_details_count'


class UserDetailsStatic(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    gender = models.IntegerField()
    activity_level = models.IntegerField()
    physical_level = models.IntegerField(blank=True, null=True)
    intro_text = models.CharField(max_length=30, blank=True, null=True)
    profile_icon = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_details_static'


class UserPhysicalData(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    date = models.DateField()
    weight = models.FloatField(blank=True, null=True)
    skeletal_muscle_mass = models.FloatField(blank=True, null=True)
    body_fat_percentage = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_physical_data'


class UsersLikedPosts(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    post = models.ForeignKey('community.Post', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users_liked_posts'


class UsersLikedQnaPosts(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    qna_post = models.ForeignKey('community.QnaPost', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users_liked_qna_posts'


class UsersSavedPosts(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    post = models.ForeignKey('community.Post', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_saved_posts'


class UsersSavedQnaPosts(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    qna_post = models.ForeignKey('community.QnaPost', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users_saved_qna_posts'