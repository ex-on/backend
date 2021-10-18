from django.db import models

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)
    creation_date = models.DateTimeField()
    title = models.CharField(max_length=30)
    content = models.CharField(max_length=500)
    modified = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'post'


class PostComment(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)
    post = models.ForeignKey(Post, models.DO_NOTHING)
    content = models.CharField(max_length=100)
    creation_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'post_comment'


class PostCommentCount(models.Model):
    post_comment = models.ForeignKey(PostComment, models.DO_NOTHING)
    count_likes = models.IntegerField()
    count_reports = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post_comment_count'


class PostCommentReply(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)
    post_comment = models.ForeignKey(PostComment, models.DO_NOTHING)
    content = models.CharField(max_length=100)
    creation_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'post_comment_reply'


class PostCommentReplyCount(models.Model):
    post_comment_reply = models.ForeignKey(PostCommentReply, models.DO_NOTHING)
    count_likes = models.IntegerField()
    count_reports = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post_comment_reply_count'


class PostCount(models.Model):
    post = models.ForeignKey(Post, models.DO_NOTHING)
    count_likes = models.IntegerField()
    count_comments = models.IntegerField()
    count_saved = models.IntegerField()
    count_reports = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post_count'


class QnaPost(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)
    title = models.CharField(max_length=30)
    content = models.CharField(max_length=500)
    creation_date = models.DateTimeField()
    modified = models.IntegerField()
    solved = models.IntegerField()
    type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'qna_post'


class QnaPostAnswer(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)
    qna_post = models.ForeignKey(QnaPost, models.DO_NOTHING)
    content = models.CharField(max_length=500)
    creation_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'qna_post_answer'


class QnaPostAnswerComment(models.Model):
    qna_post_answer = models.ForeignKey(QnaPostAnswer, models.DO_NOTHING)
    user = models.ForeignKey('User', models.DO_NOTHING)
    content = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'qna_post_answer_comment'


class QnaPostAnswerCommentReply(models.Model):
    qna_post_answer_comment = models.ForeignKey(QnaPostAnswerComment, models.DO_NOTHING)
    user = models.ForeignKey('User', models.DO_NOTHING)
    content = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'qna_post_answer_comment_reply'


class QnaPostAnswerCount(models.Model):
    qna_post_answer = models.ForeignKey(QnaPostAnswer, models.DO_NOTHING)
    count_likes = models.IntegerField()
    count_comments = models.IntegerField()
    count_reports = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'qna_post_answer_count'


class QnaPostCount(models.Model):
    qna_post = models.ForeignKey(QnaPost, models.DO_NOTHING)
    count_total_likes = models.IntegerField()
    count_answers = models.IntegerField()
    count_saved = models.IntegerField()
    count_total_comments = models.IntegerField()
    count_reports = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'qna_post_count'