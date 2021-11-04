from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import datetime
import json

from community.serializers import PostPreviewSerializer, PostSerializer
from .models import *
from users.models import User

# Create your views here.
@api_view(['GET'])
def getPost(request):
    postId = request.GET(['post_id'])
    post = Post.objects.filter(id = postId)
    serializer = PostSerializer(post)
    return Response(serializer.data)

@api_view(['GET'])
def getMain(request):
    preview = PostPreview.objects.all().order_by('-creation_date')
    index = (request.GET(['page_num']) - 1) * 10
    preview = preview[index : index + 10]
    serializer = PostPreviewSerializer(preview)
    return Response(serializer.data)

@api_view(['GET'])
def getHotBoard(request):
    preview = PostPreview.objects.filter(PostCount.count_likes > 10)
    preview = preview.order_by('-creation_date')
    index = (request.GET(['page_num']) - 1) * 10
    preview = preview[index : index + 10]
    serializer = PostPreviewSerializer(preview)
    return Response(serializer.data)