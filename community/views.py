from re import search
from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from collections import namedtuple
import datetime
import json

from rest_framework.serializers import Serializer

from community.serializers import PostCommentReplyFinalSerializer, PostCommentReplySerializer, PostCommentSerializer, PostPreviewSerializer, PostSerializer, QnaAnswerCommentReplyFinalSerializer, QnaAnswerFinalSerializer, QnaPreviewSerializer, QnaSerializer
from .models import *

# Create your views here.
@api_view(['GET'])
def getPostCommentReply(request):
    _post_id = request.GET['post_id']
    post = Post.objects.filter(id = _post_id)
    comment = PostComment.objects.filter(post_id = _post_id)
    reply = PostCommentReply.objects.filter(post_id = _post_id)
    total = {
        "post": post,
        "comment": comment,
        "reply": reply
    }
    serializer = PostCommentReplyFinalSerializer(total)
    return Response(serializer.data)

@api_view(['POST'])
def postPost(request):
    request = json.loads(request.body)
    post_instance = Post(user_id = request['user_id'], creation_date = request['creation_date'], title = request['title'], content = request['content'], modified = False)
    post_instance.save()
    PostCount.objects.create(post = post_instance, count_likes = 0, count_comments = 0, count_saved = 0, count_reports = 0)
    return HttpResponse(status = 200)

@api_view(['GET'])
def getPostPreview(request):
    index = (int(request.GET['page_num']) - 1) * 10
    post = Post.objects.order_by('-creation_date')[index:index + 10]
    count = PostCount.objects.order_by('-creation_date')[index:index + 10]
    preview = {
        "post": post,
        "count": count
    }
    serializer = PostPreviewSerializer(preview)
    return Response(serializer.data)

@api_view(['GET'])
def getHotBoardPreview(request):
    index = (int(request.GET['page_num']) - 1) * 10
    count = PostCount.objects.filter(count_likes__gt = 9).order_by('-creation_date')[index:index + 10]
    post = Post.objects.none()
    for id in list(count.values_list('post_id', flat = True)):
        instance = Post.objects.filter(id = id)
        post = post|instance
    preview = {
        "post": post,
        "count": count
    }
    serializer = PostPreviewSerializer(preview)
    return Response(serializer.data)

QnaAnswer_namedtuple = namedtuple('QnaAnswer_namedtuple', ('qna', 'answer'))
class QnaAnswerViewset(viewsets.ViewSet):
    @api_view(['GET'])
    def list(self, request):
        qnaId = request.GET['qna_id']
        qnaanswer = QnaAnswer_namedtuple(
            qna = Qna.objects.filter(id = qnaId),
            answer = QnaAnswer.objects.filter(qna_id = qnaId)
        )
        serializer = QnaAnswerFinalSerializer(qnaanswer)
        return Response(serializer.data)
    
QnaAnswerCommentReply_namedtuple = namedtuple('QnaAnswerCommentReply_namedtuple', ('comment', 'reply'))
class QnaAnswerCommentReplyViewset(viewsets.ViewSet):
    @api_view(['GET'])
    def list(self, request):
        qna_answer_id = request.GET['qna_answer_id']
        qnaanswercommentreply = QnaAnswerCommentReply_namedtuple(
            comment = QnaAnswerComment.objects.filter(qna_answer = qna_answer_id),
            reply = QnaAnswerCommentReply.objects.filter(qna_answer = qna_answer_id)
        )
        serializer = QnaAnswerCommentReplyFinalSerializer(qnaanswercommentreply)
        return Response(serializer.data)

@api_view(['POST'])
def postQna(request):
    request = json.loads(request.body)
    qna = Qna(user_id = request['user_id'], title = request['title'], content = request['content'], creation_date = request['creation_date'], modified = False, solved = False, type = request['type'])
    qna.save()
    return HttpResponse(status = 200)

@api_view(['GET'])
def getQnaMain(request):
    index = (int(request.GET['page_num']) - 1) * 10
    post = Qna.objects.order_by('-creation_date')[index:index + 10]
    count = QnaCount.objects.order_by('-creation_date')[index:index + 10]
    preview = {
        "qna": post,
        "count": count
    }
    serializer = QnaPreviewSerializer(preview)
    return Response(serializer.data)

@api_view(['GET'])
def getQnaMainSolved(request):
    preview = QnaPreview.objects.filter(solved = True)
    index = (request.GET['page_num'] - 1) * 10
    preview = preview[index : index + 10]
    serializer = QnaPreviewSerializer(preview)
    return Response(serializer.data)

@api_view(['GET'])
def getQnaMainUnsolved(request):
    preview = QnaPreview.objects.filter(solved = False)
    index = (request.GET['page_num'] - 1) * 10
    preview = preview[index : index + 10]
    serializer = QnaPreviewSerializer(preview)
    return Response(serializer.data)

@api_view(['GET'])
def getQnaMainType(request):
    _type = request.GET['type']
    preview = QnaPreview.objects.filter(type = _type)
    index = (request.GET['page_num'] - 1) * 10
    preview = preview[index : index + 10]
    serializer = QnaPreviewSerializer(preview)
    return Response(serializer.data)