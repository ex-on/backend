from django.db import models

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from users.validators import UsernameValidator
from core.models import AbstractBaseModel

class User(PermissionsMixin, AbstractBaseUser, AbstractBaseModel):
    """
    Table contains cognito-users & django-users(admin).
    PermissionsMixin leverage built-in django model permissions system
    (which allows to limit information for staff users via Groups).
    Note: Django-admin user and app user not split in different tables because of simplicity of development.
    Some libraries assume there is only one user model, and they can't work with both.
    For example to have a history log of changes for entities - to save which user made a change of object attribute,
    perhaps, auth-related libs, and some other.
    With current implementation we don't need to fork, adapt and maintain third party packages.
    They should work out of the box.
    The disadvantage is - cognito-users will have unused fields which always empty. Not critical.
    """
    username_validator = UsernameValidator()

    ### Common fields ###
    # For cognito-users username will contain `sub` claim from jwt token
    # (unique identifier (UUID) for the authenticated user).
    # For django-users it will contain username which will be used to login into django-admin site
    username = models.CharField(
        'Username', min_length=3, max_length=20, unique=True, validators=[username_validator])
    is_active = models.BooleanField('Active', default=True)
    ### Cognito-user related fields ###
    # some additional fields which will be filled-out only for users registered via Cognito
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    
    ### Django-user related fields ###
    # password is inherited from AbstractBaseUser
    # allow non-unique emails
    email = models.EmailField('Email address', blank=True)
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.'
    )
    objects = UserManager()
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']  # used only on createsuperuser

    @property
    def is_django_user(self):
        return self.has_usable_password()


class UserDetailsCount(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    count_liked_posts = models.IntegerField()
    count_saved_posts = models.IntegerField()
    count_uploaded_posts = models.IntegerField()
    count_uploaded_qna_posts = models.IntegerField()
    count_uploaded_answers = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user_details_count'


class UserDetailsStatic(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    gender = models.IntegerField()
    activity_level = models.IntegerField()
    physical_level = models.IntegerField(blank=True, null=True)
    intro_text = models.CharField(max_length=30, blank=True, null=True)
    profile_icon = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'user_details_static'


class UserPhysicalData(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    date = models.DateField()
    weight = models.FloatField(blank=True, null=True)
    muscle_mass = models.FloatField(blank=True, null=True)
    body_fat_percentage = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user_physical_data'


class UsersLikedPosts(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    post = models.ForeignKey(
        'community.Post', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'users_liked_posts'


class UsersLikedQnaPosts(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    qna_post = models.ForeignKey('community.Qna', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'users_liked_qna_posts'


class UsersSavedPosts(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    post = models.ForeignKey('community.Post', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'users_saved_posts'


class UsersSavedQnaPosts(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    qna_post = models.ForeignKey('community.Qna', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'users_saved_qna_posts'
