from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.db.models.fields import DateTimeField
from django.db.models.fields.related import ForeignKey

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey('users.User', models.DO_NOTHING)
    creation_date = models.DateTimeField()
    title = models.CharField(max_length=30)
    content = models.CharField(max_length=500)
    modified = models.BooleanField()
    type = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'post'


class PostComment(models.Model):
    user = models.ForeignKey('users.User', models.DO_NOTHING)
    post = models.ForeignKey(Post, on_delete=CASCADE)
    content = models.CharField(max_length=100)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'post_comment'


class PostCommentCount(models.Model):
    post_comment = models.ForeignKey(PostComment, on_delete = CASCADE)
    count_likes = models.IntegerField(default=0)
    count_reports = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'post_comment_count'


class PostCommentReply(models.Model):
    user = models.ForeignKey('users.User', on_delete = CASCADE)
    post = models.ForeignKey(Post, on_delete = CASCADE)
    post_comment = models.ForeignKey(PostComment, on_delete = CASCADE)
    content = models.CharField(max_length=100)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'post_comment_reply'


class PostCount(models.Model):
    post = models.OneToOneField(Post, on_delete=CASCADE)
    creation_date = models.DateTimeField()
    count_likes = models.IntegerField()
    count_comments = models.IntegerField(default=0)
    count_saved = models.IntegerField(default=0)
    count_reports = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'post_count'


class PostCommentReplyCount(models.Model):
    post_comment_reply = models.ForeignKey(PostCommentReply, on_delete = CASCADE)
    count_likes = models.IntegerField(default=0)
    count_reports = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'post_comment_reply_count'


class Qna(models.Model):
    user = models.ForeignKey('users.User', models.DO_NOTHING)
    title = models.CharField(max_length=30)
    content = models.CharField(max_length=500)
    creation_date = models.DateTimeField()
    modified = models.BooleanField()
    solved = models.BooleanField()
    type = models.IntegerField(default=1)

    class Meta:
        managed = True
        db_table = 'qna'


class QnaAnswer(models.Model):
    user = models.ForeignKey('users.User', models.DO_NOTHING)
    qna = models.ForeignKey(Qna, models.DO_NOTHING)
    content = models.CharField(max_length=500)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'qna_answer'


class QnaAnswerComment(models.Model):
    qna_answer = models.ForeignKey(QnaAnswer, models.DO_NOTHING)
    user = models.ForeignKey('users.User', models.DO_NOTHING)
    content = models.CharField(max_length=100)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'qna_answer_comment'


class QnaAnswerCommentReply(models.Model):
    qna_answer = models.ForeignKey(QnaAnswer, models.DO_NOTHING)
    qna_answer_comment = models.ForeignKey(QnaAnswerComment, models.DO_NOTHING)
    user = models.ForeignKey('users.User', models.DO_NOTHING)
    content = models.CharField(max_length=100)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'qna_answer_comment_reply'


class QnaPreview(models.Model):
    user = models.ForeignKey('users.User', models.DO_NOTHING)
    post = models.ForeignKey(Qna, models.DO_NOTHING)
    title = models.CharField(max_length=30)
    creation_date = models.DateTimeField()
    solved = models.BooleanField()
    type = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'qna_preview'


class QnaCount(models.Model):
    qna = models.ForeignKey(Qna, models.DO_NOTHING)
    creation_date = models.DateTimeField()
    count_likes = models.IntegerField()
    count_answers = models.IntegerField()
    count_saved = models.IntegerField()
    count_comments = models.IntegerField()
    count_reports = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'qna_count'


class QnaAnswerCount(models.Model):
    qna_answer = models.ForeignKey(QnaAnswer, models.DO_NOTHING)
    count_likes = models.IntegerField()
    count_comments = models.IntegerField()
    count_reports = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'qna_answer_count'

class QnaAnswerCommentCount(models.Model):
    qna_answer_comment = models.ForeignKey(QnaAnswerComment, models.DO_NOTHING)
    count_likes = models.IntegerField()
    count_reports = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'qna_answer_comment_count'

class UsersReportedPosts(models.Model):
    user = models.ForeignKey('users.User', models.DO_NOTHING)
    post = models.ForeignKey(Post, on_delete = CASCADE)
    creation_date = DateTimeField(auto_now_add = True)
    
    class Meta:
        unique_together = (('user', 'post'), )
        managed = True
        db_table = 'users_reported_posts'
    
class UsersReportedPostComments(models.Model):
    user = models.ForeignKey('users.User', models.DO_NOTHING)
    comment = models.ForeignKey(PostComment, on_delete = CASCADE)
    creation_date = DateTimeField(auto_now_add = True)
    
    class Meta:
        unique_together = (('user', 'comment'), )
        managed = True
        db_table = 'users_reported_post_comments'
class UsersReportedPostCommentReplies(models.Model):
    user = models.ForeignKey('users.User', models.DO_NOTHING)
    reply = models.ForeignKey(PostCommentReply, on_delete = CASCADE)
    creation_date = DateTimeField(auto_now_add = True)
    
    class Meta:
        unique_together = (('user', 'reply'), )
        managed = True
        db_table = 'users_reported_post_comment_replies'
class UsersReportedQnas(models.Model):
    user = models.ForeignKey('users.User', models.DO_NOTHING)
    qna = models.ForeignKey(Qna, on_delete = CASCADE)
    creation_date = DateTimeField(auto_now_add = True)
    
    class Meta:
        unique_together = (('user', 'qna'), )
        managed = True
        db_table = 'users_reported_qna'
class UsersReportedQnaAnswers(models.Model):
    user = models.ForeignKey('users.User', models.DO_NOTHING)
    answer = models.ForeignKey(QnaAnswer, on_delete = CASCADE)
    creation_date = DateTimeField(auto_now_add = True)
    class Meta:
        unique_together = (('user', 'answer'), )
        managed = True
        db_table = 'users_reported_qna_answer'    
class UsersReportedQnaAnswerComments(models.Model):
    user = models.ForeignKey('users.User', models.DO_NOTHING)
    comment = models.ForeignKey(QnaAnswerComment, on_delete = CASCADE)
    creation_date = DateTimeField(auto_now_add = True)
    class Meta:
        unique_together = (('user', 'comment'), )
        managed = True
        db_table = 'users_reported_qna_answer_comments'
class UsersReportedQnaAnswerCommentReplies(models.Model):
    user = models.ForeignKey('users.User', models.DO_NOTHING)
    reply = models.ForeignKey(QnaAnswerCommentReply, on_delete = CASCADE)
    creation_date = DateTimeField(auto_now_add = True)
    class Meta:
        unique_together = (('user', 'reply'), )
        managed = True
        db_table = 'users_reported_qna_answer_comment_replies'