from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.db.models.fields import DateTimeField
from django.db.models.fields.related import ForeignKey

from core.models import AbstractBaseModel

# Create your models here.


class Post(AbstractBaseModel):
    user = models.ForeignKey('users.User', on_delete=CASCADE)
    title = models.CharField(max_length=30)
    content = models.CharField(max_length=500)
    modified = models.BooleanField(default=False)
    hot = models.BooleanField(default=False)
    type = models.IntegerField()
    # 1: 자유, 2: 정보

    class Meta:
        managed = True
        db_table = 'post'


class PostComment(AbstractBaseModel):
    user = models.ForeignKey('users.User', on_delete=CASCADE)
    post = models.ForeignKey(Post, on_delete=CASCADE)
    content = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'post_comment'


class PostCommentCount(models.Model):
    post_comment = models.ForeignKey(PostComment, on_delete=CASCADE)
    count_likes = models.IntegerField(default=0)
    count_reports = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'post_comment_count'


class PostCommentReply(models.Model):
    user = models.ForeignKey('users.User', on_delete=CASCADE)
    post = models.ForeignKey(Post, on_delete=CASCADE)
    post_comment = models.ForeignKey(PostComment, on_delete=CASCADE)
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'post_comment_reply'


class PostCount(models.Model):
    post = models.OneToOneField(Post, on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    count_likes = models.IntegerField()
    count_comments = models.IntegerField(default=0)
    count_saved = models.IntegerField(default=0)
    count_reports = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'post_count'


class PostCommentReplyCount(models.Model):
    post_comment_reply = models.ForeignKey(PostCommentReply, on_delete=CASCADE)
    count_likes = models.IntegerField(default=0)
    count_reports = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'post_comment_reply_count'


class Qna(AbstractBaseModel):
    user = models.ForeignKey('users.User', on_delete=CASCADE)
    title = models.CharField(max_length=30)
    content = models.CharField(max_length=500)
    modified = models.BooleanField(default=False)
    solved = models.BooleanField(default=False)
    hot = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'qna'


class QnaAnswer(AbstractBaseModel):
    user = models.ForeignKey('users.User', on_delete=CASCADE)
    qna = models.ForeignKey(Qna, on_delete=CASCADE)
    content = models.CharField(max_length=500)
    # 1: 질문자 채택, 2: Best (채택 시점에서 좋아요 최다), 3: 질문자 채택 & Best
    selected_type = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'qna_answer'


class QnaAnswerComment(AbstractBaseModel):
    qna_answer = models.ForeignKey(QnaAnswer, on_delete=CASCADE)
    user = models.ForeignKey('users.User', on_delete=CASCADE)
    content = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'qna_answer_comment'


class QnaAnswerCommentReply(models.Model):
    qna_answer = models.ForeignKey(QnaAnswer, on_delete=CASCADE)
    qna_answer_comment = models.ForeignKey(QnaAnswerComment, on_delete=CASCADE)
    user = models.ForeignKey('users.User', on_delete=CASCADE)
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'qna_answer_comment_reply'


# class QnaPreview(models.Model):
#     user = models.ForeignKey('users.User', on_delete=CASCADE)
#     post = models.ForeignKey(Qna, on_delete=CASCADE)
#     title = models.CharField(max_length=30)
#     created_at = models.DateTimeField()
#     solved = models.BooleanField()
#     type = models.IntegerField()

#     class Meta:
#         managed = True
#         db_table = 'qna_preview'


class QnaCount(models.Model):
    qna = models.ForeignKey(Qna, on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    count_likes = models.IntegerField(default=0)
    count_answers = models.IntegerField(default=0)
    count_saved = models.IntegerField(default=0)
    count_comments = models.IntegerField(default=0)
    count_reports = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'qna_count'


class QnaAnswerCount(models.Model):
    qna_answer = models.ForeignKey(QnaAnswer, on_delete=CASCADE)
    count_likes = models.IntegerField(default=0)
    count_comments = models.IntegerField(default=0)
    count_reports = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'qna_answer_count'


class QnaAnswerCommentCount(models.Model):
    qna_answer_comment = models.ForeignKey(QnaAnswerComment, on_delete=CASCADE)
    count_likes = models.IntegerField(default=0)
    count_reports = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'qna_answer_comment_count'

class QnaAnswerCommentReplyCount(models.Model):
    qna_answer_comment_reply = models.ForeignKey(QnaAnswerCommentReply, on_delete=CASCADE)
    count_reports = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'qna_answer_comment_reply_count'

class UsersReportedPosts(models.Model):
    user = models.ForeignKey('users.User', on_delete=CASCADE)
    post = models.ForeignKey(Post, on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'post'), )
        managed = True
        db_table = 'users_reported_posts'


class UsersReportedPostComments(models.Model):
    user = models.ForeignKey('users.User', on_delete=CASCADE)
    post_comment = models.ForeignKey(PostComment, on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'post_comment'), )
        managed = True
        db_table = 'users_reported_post_comments'


class UsersReportedPostCommentReplies(models.Model):
    user = models.ForeignKey('users.User', on_delete=CASCADE)
    post_comment_reply = models.ForeignKey(PostCommentReply, on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'post_comment_reply'), )
        managed = True
        db_table = 'users_reported_post_comment_replies'


class UsersReportedQnas(models.Model):
    user = models.ForeignKey('users.User', on_delete=CASCADE)
    qna = models.ForeignKey(Qna, on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'qna'), )
        managed = True
        db_table = 'users_reported_qna'


class UsersReportedQnaAnswers(models.Model):
    user = models.ForeignKey('users.User', on_delete=CASCADE)
    qna_answer = models.ForeignKey(QnaAnswer, on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'qna_answer'), )
        managed = True
        db_table = 'users_reported_qna_answer'


class UsersReportedQnaAnswerComments(models.Model):
    user = models.ForeignKey('users.User', on_delete=CASCADE)
    qna_answer_comment = models.ForeignKey(QnaAnswerComment, on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'qna_answer_comment'), )
        managed = True
        db_table = 'users_reported_qna_answer_comments'


class UsersReportedQnaAnswerCommentReplies(models.Model):
    user = models.ForeignKey('users.User', on_delete=CASCADE)
    qna_answer_comment_reply = models.ForeignKey(QnaAnswerCommentReply, on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'qna_answer_comment_reply'), )
        managed = True
        db_table = 'users_reported_qna_answer_comment_replies'
