from re import T
from django.db import models
from django.db.models import fields
from django.utils import tree
from rest_framework import serializers
from rest_framework.fields import CharField

from community.models import *
from users.models import *


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ("title", "content", "created_at", "modified")


class PostCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCount
        fields = ("count_likes", "count_comments", "count_saved")


class PostCountMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCount
        fields = ("count_likes", "count_comments")


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = ("content", "created_at", "id")


class PostCommentCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCommentCount
        fields = ("count_likes",)


class PostCommentReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCommentReply
        fields = ('id', "content", "created_at")


class PostCommentReplyCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCommentReplyCount
        fields = ("count_likes",)


class PostPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'created_at', 'type')


class QnaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qna
        fields = ("title", "content", "created_at", "modified", "solved",)


class QnaCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = QnaCount
        fields = ("count_likes", "count_saved", "count_answers")


class QnaAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QnaAnswer
        fields = ("content", "created_at", "selected_type","id")


class QnaAnswerCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = QnaAnswerCount
        fields = ("count_likes", "count_comments")


class QnaAnswerCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = QnaAnswerComment
        fields = ("id", "content", "created_at")


class QnaAnswerCommentCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = QnaAnswerCommentCount
        fields = ("count_likes",)


class QnaAnswerCommentReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = QnaAnswerCommentReply
        fields = ("content", "created_at", "id",)


class QnaPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qna
        fields = ("id", "title", "content", "created_at", "solved", )


class QnaCountMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = QnaCount
        fields = ("count_likes", "count_answers")
