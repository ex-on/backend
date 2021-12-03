from re import T
from django.db import models
from django.db.models import fields
from django.utils import tree
from rest_framework import serializers

from community.models import Post, PostComment, PostCommentReply, PostCount, Qna, QnaAnswer, QnaAnswerComment, QnaAnswerCommentReply, QnaCount, QnaPreview


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = "__all__"


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = "__all__"


class PostCommentReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCommentReply
        fields = "__all__"


class PostCommentReplyFinalSerializer(serializers.Serializer):
    post = PostSerializer(many=True)
    comment = PostCommentSerializer(many=True)
    reply = PostCommentReplySerializer(many=True)


class PostCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCount
        fields = "__all__"


class PostSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class PostPreviewSerializer(serializers.Serializer):
    post = PostSerializer(many=True)
    count = PostCountSerializer(many=True)


class QnaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qna
        fields = "__all__"


class QnaAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QnaAnswer
        fields = "__all__"


class QnaCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = QnaCount
        fields = "__all__"


class QnaAnswerFinalSerializer(serializers.Serializer):
    qna = QnaSerializer(many=True)
    answer = QnaAnswerSerializer(many=True)


class QnaAnswerCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = QnaAnswerComment
        fields = "__all__"


class QnaAnswerCommentReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = QnaAnswerCommentReply
        fields = "__all__"


class QnaAnswerCommentReplyFinalSerializer(serializers.Serializer):
    comment = QnaAnswerCommentSerializer(many=True)
    reply = QnaAnswerCommentReplySerializer(many=True)


class QnaPreviewSerializer(serializers.Serializer):
    qna = QnaSerializer(many=True)
    count = QnaCountSerializer(many=True)
