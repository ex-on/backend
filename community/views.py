from django.http.response import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
import json
from rest_framework.permissions import IsAuthenticated
import json
from community.serializers import *
import datetime
from .models import *
from users.models import *

# Create your views here.

############게시판 메인화면###############
def zeroadder(num):
    if num < 10: return "0" + str(num)
    else: return str(num)

def timecalculator(date_time):
    delta = (datetime.datetime.now() - date_time.replace(tzinfo = None)).seconds
    if datetime.date.today() != date_time.date():
        return zeroadder(date_time.month) + "/" + zeroadder(date_time.day)
    elif delta // 3600 > 0:
        return zeroadder(date_time.hour) + ":" + zeroadder(date_time.minute)
    else: return str(delta // 60) + "분 전"

@api_view(['GET'])
@permission_classes([])
def getPostPreview(request):
    type = int(request.GET['type'])
    index_num = int(request.GET['index_num'])
    index = (int(request.GET['page_num']) - 1) * index_num
    if type == 0: posts = Post.objects.order_by('-creation_date')[index:index + index_num]
    else: posts = Post.objects.filter(type = type).order_by('-creation_date')[index:index + index_num]
    return_data = []
    for post in posts:
        if len(post.content) > 70: post.content = post.content[0:70] + "..."
        post.creation_date = timecalculator(post.creation_date)
        preview = {
            "user_data": {
                "username": User.objects.get(uuid = post.user_id).username,
                "profile_icon": UserDetailsStatic.objects.get(user_id = post.user_id).profile_icon
            },
            "post_data": PostPreviewSerializer(post).data,
            "count": PostCountMiniSerializer(PostCount.objects.get(post_id = post.id)).data
        }
        return_data.append(preview)
    return Response(return_data)

@api_view(['GET'])
@permission_classes([])
def getHotBoardPreview(request):
    index_num = int(request.GET['index_num'])
    index = (int(request.GET['page_num']) - 1) * index_num
    counts = PostCount.objects.filter(count_likes__gt = 9).order_by('-creation_date')[index:index + index_num]
    return_data = []
    for count in counts:
        post = Post.objects.get(id = count.post_id)
        if len(post.content) > 70: post.content = post.content[0:70] + "..."
        post.creation_date = timecalculator(post.creation_date)
        preview = {
            "user_data": {
                "username": User.objects.get(uuid = post.user_id).username,
                "profile_icon": UserDetailsStatic.objects.get(user_id = post.user_id).profile_icon
            },
            "post_data": PostPreviewSerializer(post).data,
            "count": PostCountMiniSerializer(PostCount.objects.get(post_id = post.id)).data
        }
        return_data.append(preview)
    return Response(return_data)

@api_view(['GET'])
@permission_classes([])
def getQnaMain(request):
    index = (int(request.GET['page_num']) - 1) * 10
    qnas = Qna.objects.order_by('-creation_date')[index:index + 10]
    return_data = []
    for qna in qnas:
        if len(qna.content) > 70: qna.content = qna.content[0:70] + "..."
        qna.creation_date = timecalculator(qna.creation_date)
        preview = {
            "user_data": {
                "username": User.objects.get(uuid = qna.user_id).username,
                "profile_icon": UserDetailsStatic.objects.get(user_id = qna.user_id).profile_icon
            },
            "post_data": QnaPreviewSerializer(qna).data,
            "count": QnaCountMiniSerializer(QnaCount.objects.get(qna_id = qna.id)).data
        }
        return_data.append(preview)
    return Response(return_data)


@api_view(['GET'])
@permission_classes([])
def getQnaMainSolved(request):
    index = (int(request.GET['page_num']) - 1) * 10
    qnas = Qna.objects.filter(solved = True).order_by('-creation_date')[index:index + 10]
    return_data = []
    for qna in qnas:
        if len(qna.content) > 70: qna.content = qna.content[0:70] + "..."
        qna.creation_date = timecalculator(qna.creation_date)
        preview = {
            "user_data": {
                "username": User.objects.get(uuid = qna.user_id).username,
                "profile_icon": UserDetailsStatic.objects.get(user_id = qna.user_id).profile_icon
            },
            "post_data": QnaPreviewSerializer(qna).data,
            "count": QnaCountMiniSerializer(QnaCount.objects.get(qna_id = qna.id)).data
        }
        return_data.append(preview)
    return Response(return_data)


@api_view(['GET'])
@permission_classes([])
def getQnaMainUnsolved(request):
    index = (int(request.GET['page_num']) - 1) * 10
    qnas = Qna.objects.filter(solved = False).order_by('-creation_date')[index:index + 10]
    return_data = []
    for qna in qnas:
        if len(qna.content) > 70: qna.content = qna.content[0:70] + "..."
        qna.creation_date = timecalculator(qna.creation_date)
        preview = {
            "user_data": {
                "username": User.objects.get(uuid = qna.user_id).username,
                "profile_icon": UserDetailsStatic.objects.get(user_id = qna.user_id).profile_icon
            },
            "post_data": QnaPreviewSerializer(qna).data,
            "count": QnaCountMiniSerializer(QnaCount.objects.get(qna_id = qna.id)).data
        }
        return_data.append(preview)
    return Response(return_data)


@api_view(['GET'])
@permission_classes([])
def getQnaMainType(request):
    type = int(request.GET['type'])
    index = (int(request.GET['page_num']) - 1) * 10
    qnas = Qna.objects.filter(type = type).order_by('-creation_date')[index:index + 10]
    return_data = []
    for qna in qnas:
        if len(qna.content) > 70: qna.content = qna.content[0:70] + "..."
        qna.creation_date = timecalculator(qna.creation_date)
        preview = {
            "user_data": {
                "username": User.objects.get(uuid = qna.user_id).username,
                "profile_icon": UserDetailsStatic.objects.get(user_id = qna.user_id).profile_icon
            },
            "post_data": QnaPreviewSerializer(qna).data,
            "count": QnaCountMiniSerializer(QnaCount.objects.get(qna_id = qna.id)).data
        }
        return_data.append(preview)
    return Response(return_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserPostQna(request):
    if "user_id" in request.GET: user_id = request.GET['user_id']
    else: user_id = request.user.uuid
    user = User.objects.get(uuid = user_id)
    user_info = {
        "username": user.username,
        "profile_icon": UserDetailsStatic.objects.get(user_id = user.uuid).profile_icon,
        "days": (datetime.date.today() - user.created_at.date() + datetime.timedelta(days = 1)).days,
        "post_num": Post.objects.filter(user_id = user_id).count(),
        "answer_num": QnaAnswer.objects.filter(user_id = user_id).count()
    }
    posts = Post.objects.filter(user_id = user_id).order_by('-creation_date')[0:8]
    answers = QnaAnswer.objects.filter(user_id = user_id).order_by('-creation_date')[0:8]
    post_preview, qna_preview = [], []
    for post in posts:
        if len(post.content) > 70: post.content = post.content[0:70] + "..."
        post.creation_date = timecalculator(post.creation_date)
        data = {
            "post_data": PostPreviewSerializer(post).data,
            "count": PostCountMiniSerializer(PostCount.objects.get(post_id = post.id)).data
        }
        post_preview.append(data)
    for answer in answers:
        qna = Qna.objects.get(id = answer.qna_id)
        if len(answer.content) > 70: answer.content = answer.content[0:70] + "..."
        data = {
            "qna_data": {
                "qna_title": qna.title,
                "answer_content": answer.content,
                "creation_date": timecalculator(answer.creation_date)    
            },
            "count": QnaCountMiniSerializer(QnaCount.objects.get(qna_id = qna.id)).data
        }
        qna_preview.append(data)
    total_data = {
        "user_info": user_info,
        "post_data": post_preview,
        "qna_data": qna_preview
    }
    return Response(total_data)
    

############게시물 확인#################

@api_view(['GET'])
@permission_classes([])
def getPost(request):
    post_id = request.GET['post_id']
    post = Post.objects.get(id = post_id)
    post_count = PostCount.objects.get(post_id = post_id)
    data = {
        "user_data": {
            "user_name": User.objects.get(uuid = post.user_id).username,
            "profile_icon": UserDetailsStatic.objects.get(user_id = post.user_id).profile_icon
        },
        "post": PostSerializer(post).data,
        "post_count": PostCountSerializer(post_count).data
    }
    return Response(data)

@api_view(['GET'])
@permission_classes([])
def getPostComment(request):
    post_id = request.GET['post_id']
    comments = PostComment.objects.filter(post_id = post_id).order_by('-creation_date')
    total_data = []
    for comment in comments:
        data = {
            "user_data": {
                "user_name": User.objects.get(uuid = comment.user_id).username,
                "profile_icon": UserDetailsStatic.objects.get(user_id = comment.user_id).profile_icon
            },
            "comment_data": PostCommentSerializer(comment).data,
            "comment_count": PostCommentCountSerializer(PostCommentCount.objects.get(post_comment_id = comment.id)).data
        }
        total_data.append(data)
    return Response(total_data)

@api_view(['GET'])
@permission_classes([])
def getPostCommentReply(request):
    _post_id = request.GET['post_id']
    reply = PostCommentReply.objects.filter(post_id = _post_id)
    reply_count = PostCommentReplyCount.objects.none()
    user = User.objects.none()
    user_profile = UserDetailsStatic.objects.none()
    for id in list(reply.values_list('id', flat = True)):
        instance = PostCommentReplyCount.objects.filter(post_comment_reply_id = id)
        reply_count = reply_count | instance
    for user_id in list(reply.values_list('user_id', flat = True)):
        user_instance = User.objects.filter(uuid = user_id)
        user = user | user_instance
        profile_instance = UserDetailsStatic.objects.filter(user_id = user_id)
        user_profile = user_profile | profile_instance
    total = {
        "reply": reply.order_by('-creation_date'),
        "reply_count": reply_count,
        "user_name": user,
        "user_profile": user_profile
    }
    serializer = PostCommentReplyViewSerializer(total)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([])
def getQna(request):
    _qna_id = request.GET['qna_id']
    qna = Qna.objects.filter(id = _qna_id)
    if qna.first() == None:
        qna_count = QnaCount.objects.none()
        user_name = User.objects.none()
        user_profile = UserDetailsStatic.objects.none()
    else:
        qna_count = QnaCount.objects.filter(qna_id = _qna_id)
        user_name = User.objects.filter(uuid = qna.first().user_id)
        user_profile = UserDetailsStatic.objects.filter(user_id = qna.first().user_id)
    total = {
        "qna": qna,
        "qna_count": qna_count,
        "user_name": user_name,
        "user_profile": user_profile
    }
    serializer = QnaViewSerializer(total)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([])
def getQnaAnswer(request):
    _qna_id = request.GET['qna_id']
    answer = QnaAnswer.objects.filter(qna_id = _qna_id)
    answer_count = QnaAnswerCount.objects.none()
    user = User.objects.none()
    user_profile = UserDetailsStatic.objects.none()
    for id in list(answer.values_list('id', flat = True)):
        instance = QnaAnswerCount.objects.filter(qna_answer_id = id)
        answer_count = answer_count | instance
    for user_id in list(answer.values_list('user_id', flat = True)):
        user_instance = User.objects.filter(uuid = user_id)
        user = user | user_instance
        profile_instance = UserDetailsStatic.objects.filter(user_id = user_id)
        user_profile = user_profile | profile_instance
    total = {
        "answer": answer.order_by('-creation_date'),
        "answer_count": answer_count,
        "user_name": user,
        "user_profile": user_profile
    }
    serializer = QnaAnswerViewSerializer(total)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([])
def getQnaAnswerCommentReply(request):
    _qna_answer_id = request.GET['qna_answer_id']
    comment = QnaAnswerComment.objects.filter(qna_answer_id = _qna_answer_id)
    reply = QnaAnswerCommentReply.objects.filter(qna_answer_id = _qna_answer_id)
    user_id_list = list(comment.values_list('user_id', flat = True)) + list(reply.values_list('user_id', flat = True))
    user_name = User.objects.none()
    user_profile = UserDetailsStatic.objects.none()
    for id in user_id_list:
        user_instance = User.objects.filter(uuid = id)
        profile_instance = UserDetailsStatic.objects.filter(user_id = id)
        user_name = user_name | user_instance
        user_profile = user_profile | profile_instance
    total = {
        "comment": comment,
        "reply": reply,
        "user_name": user_name,
        "user_profile": user_profile
    }
    serializer = QnaAnswerCommentReplyViewSerializer(total)
    return Response(serializer.data)

############게시물 작성#################

@api_view(['POST'])
@permission_classes([])
def postPost(request):
    request = json.loads(request.body)
    post_instance = Post(user_id=request['user_id'], creation_date=request['creation_date'],
                         title=request['title'], content=request['content'], modified=False, type = request['type'])
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

############ 게시물 수정 #######################

@api_view(['POST'])
@permission_classes([])
def modifyPost(request):
    request = json.loads(request.body)
    post = Post.objects.get(id = request['post_id'])
    post.title = request['title']
    post.content = request['content']
    post.type = request['type']
    post.modified = True
    post.save()
    return HttpResponse(status = 200)

@api_view(['POST'])
@permission_classes([])
def modifyPostComment(request):
    request = json.loads(request.body)
    comment = PostComment.objects.get(id = request['comment_id'])
    comment.content = request['content']
    comment.save()
    return HttpResponse(status = 200)

@api_view(['POST'])
@permission_classes([])
def modifyPostCommentReply(request):
    request = json.loads(request.body)
    reply = PostCommentReply.objects.get(id = request['reply_id'])
    reply.content = request['content']
    reply.save()
    return HttpResponse(status = 200)

@api_view(['POST'])
@permission_classes([])
def modifyQna(request):
    request = json.loads(request.body)
    qna = Qna.objects.get(id = request['qna_id'])
    qna.title = request['title']
    qna.content = request['content']
    qna.type = request['type']
    qna.modified = True
    qna.save()
    return HttpResponse(status = 200)

@api_view(['POST'])
@permission_classes([])
def modifyQnaAnswer(request):
    request = json.loads(request.body)
    answer = QnaAnswer.objects.get(id = request['answer_id'])
    answer.content = request['content']
    answer.save()
    return HttpResponse(status = 200)

@api_view(['POST'])
@permission_classes([])
def modifyQnaAnswerComment(request):
    request = json.loads(request.body)
    comment = QnaAnswerComment.objects.get(id = request['comment_id'])
    comment.content = request['content']
    comment.save()
    return HttpResponse(status = 200)

@api_view(['POST'])
@permission_classes([])
def modifyQnaAnswerCommentReply(request):
    request = json.loads(request.body)
    reply = QnaAnswerCommentReply.objects.get(id = request['reply_id'])
    reply.content = request['content']
    reply.save()
    return HttpResponse(status = 200)