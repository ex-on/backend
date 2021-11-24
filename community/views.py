from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from collections import namedtuple
import datetime
import json

from community.serializers import PostCommentReplyFinalSerializer, PostCommentReplySerializer, PostPreviewSerializer, PostSerializer, QnaAnswerCommentReplyFinalSerializer, QnaAnswerFinalSerializer, QnaPreviewSerializer, QnaSerializer
from .models import *
from users.models import User

# Create your views here.
PostCommentReply_namedtuple = namedtuple('PostCommentReply_namedtuple', ('post', 'comment','reply'))
class PostCommentReplyViewSet(viewsets.ViewSet):
    @api_view(['GET'])
    def list(self, request):
        postid = request.GET['post_id']
        postcommentreply = PostCommentReply_namedtuple(
            post = Post.objects.filter(id = postid),
            comment = PostComment.objects.filter(post_id = postid),
            reply = PostCommentReply.objects.filter(post_id = postid)
        )
        serializer = PostCommentReplyFinalSerializer(postcommentreply)
        return Response(serializer.data)

@api_view(['POST'])
def postPost(request):
    request = json.loads(request.body)
    post_instance = Post(user_id = request['user_id'], creation_date = request['creation_date'], title = request['title'], content = request['content'], modified = False)
    post_instance.save()
    PostCount.objects.create(post = post_instance, count_likes = 0, count_comments = 0, count_saved = 0, count_reports = 0)
    return HttpResponse(status = 200)

PostPreview = namedtuple('PostPreview', ('post', 'count'))
class PostPreviewViewSet(viewsets.ViewSet):
    @api_view(['GET'])
    def list(self, request):
        index = (int(request.GET['page_num']) - 1) * 10
        preview = PostPreview(
            preview = Post.objects.order_by('-id')[index:index + 10],
            count = PostCount.objects.order_by('-id')[index:index + 10]
        )
        serializer = PostPreviewSerializer(preview)
        return Response(serializer.data)

class HotBoardPreviewViewSet(viewsets.ViewSet):
    @api_view(['GET'])
    def list(request):
        index = (request.GET['page_num'] - 1) * 10
        preview = PostPreview(
            post = Post.objects.filter(PostCount.count_likes >= 10).order_by('-id')[index:index + 10],
            count = PostCount.objects.filter(count_likes__gt = 9).order_by('-id')[index:index + 10]
        )
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
    preview = QnaPreview.objects.all().order_by('-creation_date')
    index = (request.GET['page_num'] - 1) * 10
    preview = preview[index : index + 10]
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