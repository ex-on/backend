from django.db import models
from django.db.models.deletion import DO_NOTHING

# Create your models here.


class Post(models.Model):
    user = models.ForeignKey('users.User', models.DO_NOTHING)
    creation_date = models.DateTimeField()
    title = models.CharField(max_length=30)
    content = models.CharField(max_length=500)
    modified = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'post'

class PostComment(models.Model):
    user = models.ForeignKey('users.User', models.DO_NOTHING)
    post = models.ForeignKey(Post, models.DO_NOTHING)
    content = models.CharField(max_length=100)
    creation_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'post_comment'


class PostCommentCount(models.Model):
    post_comment = models.ForeignKey(PostComment, models.DO_NOTHING)
    count_likes = models.IntegerField()
    count_reports = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'post_comment_count'


class PostCommentReply(models.Model):
    user = models.ForeignKey('users.User', models.DO_NOTHING)
    post = models.ForeignKey('users.User', models.DO_NOTHING)
    post_comment = models.ForeignKey(PostComment, models.DO_NOTHING)
    content = models.CharField(max_length=100)
    creation_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'post_comment_reply'

class PostPreview(models.Model):
    user = models.ForeignKey('users.User', models.DO_NOTHING)
    post = models.ForeignKey('Post', models.DO_NOTHING)
    title = models.CharField(max_length = 30)
    creation_date = models.DateTimeField()

    class Meta:
        managed = True
        managed = False
        db_table = 'post_preview'

class PostCount(models.Model):
    post = models.ForeignKey(Post, models.DO_NOTHING)
    preview = models.OneToOneField(PostPreview)
    count_likes = models.IntegerField()
    count_comments = models.IntegerField()
    count_saved = models.IntegerField()
    count_reports = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'post_count'

class PostCommentCount(models.Model):
    post_comment = models.ForeignKey(PostComment, models.DO_NOTHING)
    count_likes = models.IntegerField()
    count_reports = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'post_comment_count'

class PostCommentReplyCount(models.Model):
    post_comment_reply = models.ForeignKey(PostCommentReply, models.DO_NOTHING)
    count_likes = models.IntegerField()
    count_reports = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post_comment_reply_count'

class Qna(models.Model):
    user = models.ForeignKey('users.User', models.DO_NOTHING)
    title = models.CharField(max_length=30)
    content = models.CharField()
    creation_date = models.DateTimeField()
    modified = models.IntegerField()
    solved = models.BooleanField()
    type = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'qna_post'

class QnaAnswer(models.Model):
    user = models.ForeignKey('users.User', models.DO_NOTHING)
    qna = models.ForeignKey(Qna, models.DO_NOTHING)
    content = models.CharField(max_length=500)
    creation_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'qna_post_answer'

class QnaAnswerComment(models.Model):
    qna_answer = models.ForeignKey(QnaAnswer, models.DO_NOTHING)
    user = models.ForeignKey('users.User', models.DO_NOTHING)
    content = models.CharField(max_length=100)
    creation_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'qna_post_answer_comment'

class QnaAnswerCommentReply(models.Model):
    qna_answer = models.ForeignKey(QnaAnswer, models.DO_NOTHING)
    qna_answer_comment = models.ForeignKey(QnaAnswerComment, models.DO_NOTHING)
    user = models.ForeignKey('users.User', models.DO_NOTHING)
    content = models.CharField(max_length=100)
    creation_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'qna_post_answer_comment_reply'

class QnaPreview(models.Model):
    user = models.ForeignKey('users.User', models.DO_NOTHING)
    post = models.ForeignKey(Qna, models.DO_NOTHING)
    title = models.CharField(max_length = 30)
    creation_date = models.DateTimeField()
    solved = models.BooleanField()
    type = models.IntegerField()
    
    class Meta:
        managed = True
        db_table = 'qna_preview'

class QnaCount(models.Model):
    qna = models.ForeignKey(Qna, models.DO_NOTHING)
    count_total_likes = models.IntegerField()
    count_answers = models.IntegerField()
    count_saved = models.IntegerField()
    count_total_comments = models.IntegerField()
    count_reports = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'qna_post_count'
class QnaAnswerCount(models.Model):
    qna_answer = models.ForeignKey(QnaAnswer, models.DO_NOTHING)
    count_likes = models.IntegerField()
    count_comments = models.IntegerField()
    count_reports = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'qna_post_answer_count'
