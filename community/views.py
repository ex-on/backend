from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import datetime
import json

from community.serializers import PostPreviewSerializer, PostSerializer, QnaPostSerializer, QnaPreviewSerializer, QnaSerializer
from .models import *
from users.models import User

# Create your views here.
@api_view(['GET'])
def getMain(request):
    preview = PostPreview.objects.all().order_by('-creation_date')
    index = (request.GET(['page_num']) - 1) * 10
    preview = preview[index : index + 10]
    serializer = PostPreviewSerializer(preview)
    return Response(serializer.data)

@api_view(['GET'])
def getPost(request):
    postId = request.GET(['post_id'])
    post = Post.objects.filter(id = postId)
    serializer = PostSerializer(post)
    return Response(serializer.data)

@api_view(['GET'])
def getHotBoard(request):
    preview = PostPreview.objects.filter(PostCount.count_likes > 10)
    preview = preview.order_by('-creation_date')
    index = (request.GET(['page_num']) - 1) * 10
    preview = preview[index : index + 10]
    serializer = PostPreviewSerializer(preview)
    return Response(serializer.data)

@api_view(['GET'])
def getQnaMain(request):
    preview = QnaPreview.objects.all().order_by('-creation_date')
    index = (request.GET(['page_num']) - 1) * 10
    preview = preview[index : index + 10]
    serializer = QnaPreviewSerializer(preview)
    return Response(serializer.data)

@api_view(['GET'])
def getQnaMainSolved(request):
    preview = QnaPreview.objects.filter(solved = True)
    index = (request.GET(['page_num']) - 1) * 10
    preview = preview[index : index + 10]
    serializer = QnaPreviewSerializer(preview)
    return Response(serializer.data)

@api_view(['GET'])
def getQnaMainUnsolved(request):
    preview = QnaPreview.objects.filter(solved = False)
    index = (request.GET(['page_num']) - 1) * 10
    preview = preview[index : index + 10]
    serializer = QnaPreviewSerializer(preview)
    return Response(serializer.data)

@api_view(['GET'])
def getQnaMainType(request):
    _type = request.GET(['type'])
    preview = QnaPreview.objects.filter(type = _type)
    serializer = QnaPreviewSerializer(preview)
    return Response(serializer.data)

@api_view(['GET'])
def getQna(request):
    qnaId = request.GET(['qna_id'])
    qna = QnaPost.objects.filter(id = qnaId)
    serializer = QnaSerializer(qna)
    return Response(serializer.data)