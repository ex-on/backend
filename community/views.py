from django.http.response import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
import json
from rest_framework.permissions import IsAuthenticated
import json
from community.serializers import *
from .models import *

# Create your views here.

############게시판 메인화면###############


@api_view(['GET'])
@permission_classes([])
def getPostPreview(request):
    index = (int(request.GET['page_num']) - 1) * 10
    post = Post.objects.order_by('-creation_date')[index:index + 10]
    count = PostCount.objects.order_by('-creation_date')[index:index + 10]
    preview = {
        "post": post,
        "count": count
    }
    serializer = PostPreviewSerializer(preview, many = True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([])
def getHotBoardPreview(request):
    index = (int(request.GET['page_num']) - 1) * 10
    count = PostCount.objects.filter(count_likes__gt=9).order_by(
        '-creation_date')[index:index + 10]
    post = Post.objects.none()
    for id in list(count.values_list('post_id', flat=True)):
        instance = Post.objects.filter(id=id)
        post = post | instance
    preview = {
        "post": post,
        "count": count
    }
    serializer = PostPreviewSerializer(preview, many = True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([])
def getQnaMain(request):
    index = (int(request.GET['page_num']) - 1) * 10
    post = Qna.objects.order_by('-creation_date')[index:index + 10]
    count = QnaCount.objects.order_by('-creation_date')[index:index + 10]
    preview = {
        "qna": post,
        "count": count
    }
    serializer = QnaPreviewSerializer(preview, many = True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([])
def getQnaMainSolved(request):
    preview = QnaPreview.objects.filter(solved=True)
    index = (request.GET['page_num'] - 1) * 10
    preview = preview[index : index + 10]
    serializer = QnaPreviewSerializer(preview, many = True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([])
def getQnaMainUnsolved(request):
    preview = QnaPreview.objects.filter(solved=False)
    index = (request.GET['page_num'] - 1) * 10
    preview = preview[index : index + 10]
    serializer = QnaPreviewSerializer(preview, many = True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([])
def getQnaMainType(request):
    _type = request.GET['type']
    preview = QnaPreview.objects.filter(type=_type)
    index = (request.GET['page_num'] - 1) * 10
    preview = preview[index : index + 10]
    serializer = QnaPreviewSerializer(preview, many = True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([])
def getUserPostQna(request):
    _user_id = request.GET['user_id']
    post = Post.objects.filter(user_id = _user_id)
    qna = Qna.objects.filter(user_id = _user_id)
    total = {
        "post": post,
        "qna": qna
    }
    serializer = PostQnaSerializer(total, many = True)
    return Response(serializer.data)
    
############게시물 확인#################


@api_view(['GET'])
@permission_classes([])
def getPostCommentReply(request):
    _post_id = request.GET['post_id']
    post = Post.objects.filter(id=_post_id)
    comment = PostComment.objects.filter(post_id=_post_id)
    reply = PostCommentReply.objects.filter(post_id=_post_id)
    total = {
        "post": post,
        "comment": comment,
        "reply": reply
    }
    serializer = PostCommentReplyFinalSerializer(total)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getQnaAnswer(request):
    _qna_id = request.GET['qna_id']
    qna = Qna.objects.filter(id=_qna_id)
    answer = QnaAnswer.objects.filter(qna_id=_qna_id)
    qnaanswer = {
        "qna": qna,
        "answer": answer
    }
    serializer = QnaAnswerFinalSerializer(qnaanswer)
    return Response(serializer.data)
    # return Response(qnaanswer)


@api_view(['GET'])
@permission_classes([])
def getQnaAnswerCommentReply(request):
    _qna_answer_id = request.GET['qna_answer_id']
    comment = QnaAnswerComment.objects.filter(qna_answer_id=_qna_answer_id)
    reply = QnaAnswerCommentReply.objects.filter(qna_answer_id=_qna_answer_id)
    commentreply = {
        "comment": comment,
        "reply": reply
    }
    serializer = QnaAnswerCommentReplyFinalSerializer(commentreply)
    return Response(serializer.data)

############게시물 작성#################


@api_view(['POST'])
@permission_classes([])
def postPost(request):
    request = json.loads(request.body)
    post_instance = Post(user_id=request['user_id'], creation_date=request['creation_date'],
                         title=request['title'], content=request['content'], modified=False)
    post_instance.save()
    count_instance = PostCount(post_id = post_instance.id, creation_date = request['creation_date'], count_likes = 0, count_comments = 0, count_saved = 0, count_reports = 0)
    count_instance.save()
    return HttpResponse(status = 200)

@api_view(['POST'])
@permission_classes([])
def postPostComment(request):
    request = json.loads(request.body)
    comment_instance = PostComment(user_id=request['user_id'], post_id=request['post_id'],
                                   content=request['content'], creation_date=request['creation_date'])
    comment_instance.save()
    count_instance = PostCommentCount(post_comment_id = comment_instance.id, count_likes = 0, count_reports = 0)
    count_instance.save()
    return HttpResponse(status = 200)

@api_view(['POST'])
@permission_classes([])
def postPostCommentReply(request):
    request = json.loads(request.body)
    reply_instance = PostCommentReply(user_id=request['user_id'], post_id=request['post_id'],
                                      post_comment_id=request['post_comment_id'], content=request['content'], creation_date=request['creation_date'])
    reply_instance.save()
    count_instance = PostCommentReplyCount(post_comment_reply_id = reply_instance.id, count_likes = 0, count_reports = 0)
    count_instance.save()
    return HttpResponse(status = 200)
    
@api_view(['POST'])
@permission_classes([])
def postQna(request):
    request = json.loads(request.body)
    qna_instance = Qna(user_id=request['user_id'], title=request['title'], content=request['content'],
                       creation_date=request['creation_date'], modified=False, solved=False, type=request['type'])
    qna_instance.save()
    count_instance = QnaCount(qna_id = qna_instance.id, creation_date = request['creation_date'], count_total_likes = 0, count_answers = 0, count_saved = 0, count_total_comments = 0, count_reports = 0)
    count_instance.save()
    return HttpResponse(status = 200)

@api_view(['POST'])
@permission_classes([])
def postQnaAnswer(request):
    request = json.loads(request.body)
    answer_instance = QnaAnswer(user_id=request['user_id'], qna_id=request['qna_id'],
                                content=request['content'], creation_date=request['creation_date'])
    answer_instance.save()
    count_instance = QnaAnswerCount(qna_answer_id = answer_instance.id, count_likes = 0, count_comments = 0, count_reports = 0)
    count_instance.save()
    return HttpResponse(status = 200)

@api_view(['POST'])
@permission_classes([])
def postQnaAnswerComment(request):
    request = json.loads(request.body)
    answer_instance = QnaAnswerComment(user_id = request['user_id'], qna_answer_id = request['qna_answer_id'], content = request['content'], creation_date = request['creation_date'])
    answer_instance.save()
    return HttpResponse(status=200)


@api_view(['POST'])
@permission_classes([])
def postQnaAnswerCommentReply(request):
    request = json.loads(request.body)
    answer_instance = QnaAnswerCommentReply(user_id = request['user_id'], qna_answer_id = request['qna_answer_id'], qna_answer_comment_id = request['qna_answer_comment_id'], content = request['content'], creation_date = request['creation_date'])
    answer_instance.save()
    return HttpResponse(status=200)
