from django.db import models
from django.db.models import fields
from rest_framework import serializers

from community.models import Post, PostComment, PostCommentReply, PostPreview, Qna, QnaAnswer, QnaAnswerComment, QnaAnswerCommentReply, QnaPost, QnaPostAnswer, QnaPreview

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('user', 'creation_date', 'title', 'content', 'modified')

class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = ('user', 'content', 'creation_date')
        
class PostCommentReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCommentReply
        fields = ('user', 'post_comment','content', 'creation_date')

class PostCommentReplyFinalSerializer(serializers.Serializer):
    post = PostSerializer()
    comment = PostCommentSerializer(many = True)
    reply = PostCommentReplySerializer(many = True)
    
class PostPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostPreview
        fields = ('user', 'title', 'creation_date')

class QnaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qna
        fields = ('user', 'title', 'content', 'creation_date', 'modified')

class QnaAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QnaAnswer
        fields = ('user', 'content', 'creation_date')

class QnaAnswerFinalSerializer(serializers.Serializer):
    qna = QnaSerializer()
    answer = QnaAnswerSerializer(many = True)
    
class QnaAnswerCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = QnaAnswerComment
        fields = ('user', 'content', 'creation_date')

class QnaAnswerCommentReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = QnaAnswerCommentReply
        fields = ('user', 'qna_answer_comment', 'content', 'creation_date')
        
class QnaAnswerCommentReplyFinalSerializer(serializers.Serializer):
    comment = QnaAnswerCommentSerializer(many = True)
    reply = QnaAnswerCommentReplySerializer(many = True)
class QnaPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = QnaPreview
        fields = ('user', 'title', 'creation_date', 'solved')