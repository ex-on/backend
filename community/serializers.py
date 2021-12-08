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
        fields = ("title", "content", "creation_date", "modified")

class PostCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCount
        fields = ("count_likes", "count_comments", "count_saved")

class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = "__all__"
    
class PostCommentCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCommentCount
        fields = "__all__"

class PostCommentReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCommentReply
        fields = "__all__"

class PostCommentReplyCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCommentReplyCount
        fields = "__all__"

class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uuid','username']
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetailsStatic
        fields = ['user_id', 'profile_icon']
        
class PostPreviewSerializer(serializers.Serializer):
    post = PostSerializer(many = True)
    count = PostCountSerializer(many = True)

class PostViewSerializer(serializers.Serializer):
    post = PostSerializer(many = True)
    post_count = PostCountSerializer(many = True)
    user_name = UserNameSerializer(many = True)
    user_profile = UserProfileSerializer(many = True)

class PostCommentViewSerializer(serializers.Serializer):
    comment = PostCommentSerializer(many = True)
    comment_count = PostCommentCountSerializer(many = True)
    user_name = UserNameSerializer(many = True)
    user_profile = UserProfileSerializer(many = True)
    
class PostCommentReplyViewSerializer(serializers.Serializer):
    reply = PostCommentReplySerializer(many = True)
    reply_count = PostCommentReplyCountSerializer(many = True)
    user_name = UserNameSerializer(many = True)
    user_profile = UserProfileSerializer(many = True)

class QnaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qna
        fields = "__all__"

class QnaCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = QnaCount
        fields = "__all__"
class QnaAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QnaAnswer
        fields = "__all__"

class QnaAnswerCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = QnaAnswerCount
        fields = "__all__"

class QnaAnswerCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = QnaAnswerComment
        fields = "__all__"

class QnaAnswerCommentReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = QnaAnswerCommentReply
        fields = "__all__"

class QnaPreviewSerializer(serializers.Serializer):
    qna = QnaSerializer(many = True)
    count = QnaCountSerializer(many = True)

class QnaViewSerializer(serializers.Serializer):
    qna = QnaSerializer(many = True)
    qna_count = QnaCountSerializer(many = True)
    user_name = UserNameSerializer(many = True)
    user_profile = UserProfileSerializer(many = True)

class QnaAnswerViewSerializer(serializers.Serializer):
    answer = QnaAnswerSerializer(many = True)
    answer_count = QnaAnswerCountSerializer(many = True)
    user_name = UserNameSerializer(many = True)
    user_profile = UserProfileSerializer(many = True)

class QnaAnswerCommentReplyViewSerializer(serializers.Serializer):
    comment = QnaAnswerCommentSerializer(many = True)
    reply = QnaAnswerCommentReplySerializer(many = True)
    user_name = UserNameSerializer(many = True)
    user_profile = UserProfileSerializer(many = True)

class PostQnaSerializer(serializers.Serializer):
    post = PostSerializer(many = True)
    qna = QnaSerializer(many = True)
