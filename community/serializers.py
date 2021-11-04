from django.db import models
from django.db.models import fields
from rest_framework import serializers

from community.models import Post, PostPreview

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('user', 'creation_date', 'title', 'content', 'modified')

class PostPreviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PostPreview
        fields = ('user', 'title', 'creation_date')


