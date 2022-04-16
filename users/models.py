from django.db import models

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db.models.deletion import CASCADE
from users.validators import UsernameValidator
from core.models import AbstractBaseModel, AbstractBaseUserModel


class User(PermissionsMixin, AbstractBaseUser, AbstractBaseUserModel):
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
        'Username', max_length=20, unique=True, validators=[username_validator])
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
    user = models.ForeignKey(User, on_delete = CASCADE)
    count_protein = models.IntegerField(default=0)
    count_liked_posts = models.IntegerField(default=0)
    count_saved_posts = models.IntegerField(default=0)
    count_uploaded_posts = models.IntegerField(default=0)
    count_uploaded_qnas = models.IntegerField(default=0)
    count_uploaded_answers = models.IntegerField(default=0)
    count_accepted_answers = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'user_details_count'


class UserDetailsStatic(models.Model):
    user = models.ForeignKey(User, on_delete = CASCADE)
    gender = models.IntegerField()
    birth_date = models.DateField()
    activity_level = models.IntegerField(default=0)
    physical_level = models.IntegerField(blank=True, null=True)
    height = models.FloatField(null=True)
    profile_privacy = models.IntegerField(default=0)
    # 0: 전체 공개, 1: 커뮤니티 활동만 공개, 2: 신체 기록만 공개, 3: 모두 비공개
    fcm_token = models.CharField(max_length=200, null=True)
    intro_text = models.CharField(max_length=30, blank=True, null=True)
    auth_provider = models.IntegerField()
    # 0: Manual, 1: Kakao, 2: Google, 3: Facebook

    class Meta:
        managed = True
        db_table = 'user_details_static'

class UsersLikedPosts(models.Model):
    user = models.ForeignKey(User, on_delete = CASCADE)
    post = models.ForeignKey(
        'community.Post', on_delete = CASCADE)

    class Meta:
        managed = True
        db_table = 'users_liked_posts'

class UsersLikedPostComments(models.Model):
    user = models.ForeignKey(User, on_delete = CASCADE)
    post_comment = models.ForeignKey('community.PostComment', on_delete = CASCADE)

    class Meta:
        managed = True
        db_table = 'users_liked_post_comments'

class UsersLikedPostCommentReplies(models.Model):
    user = models.ForeignKey(User, on_delete = CASCADE)
    post_comment_reply = models.ForeignKey('community.PostCommentReply', on_delete = CASCADE)

    class Meta:
        managed = True
        db_table = 'users_liked_post_comment_replies'

class UsersLikedQnaAnswers(models.Model):
    user = models.ForeignKey(User, on_delete = CASCADE)
    qna_answer = models.ForeignKey('community.QnaAnswer', on_delete = CASCADE)

    class Meta:
        managed = True
        db_table = 'users_liked_qna_answers'

class UsersLikedQnaAnswerComments(models.Model):
    user = models.ForeignKey(User, on_delete = CASCADE)
    qna_answer_comment = models.ForeignKey('community.QnaAnswerComment', on_delete = CASCADE)

    class Meta:
        managed = True
        db_table = 'users_liked_qna_answer_comments'

class UsersBookmarkedPosts(models.Model):
    user = models.ForeignKey(User, on_delete = CASCADE)
    post = models.ForeignKey('community.Post', on_delete = CASCADE)

    class Meta:
        managed = True
        db_table = 'users_bookmarked_posts'


class UsersBookmarkedQnas(models.Model):
    user = models.ForeignKey(User, on_delete = CASCADE)
    qna = models.ForeignKey('community.Qna', on_delete = CASCADE)

    class Meta:
        managed = True
        db_table = 'users_bookmarked_qnas'
