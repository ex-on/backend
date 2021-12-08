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

@api_view(['GET'])
@permission_classes([])
def getPostPreview(request):
    index = (int(request.GET['page_num']) - 1) * 10
    post = Post.objects.order_by('-creation_date')[index:index + 10]
    return_data = []
    for instance in post:
        delta = datetime.datetime.now() - instance.creation_date.replace(tzinfo = None)
        if delta.days > 0:
            delta = str(delta.days) + "일 전"
        elif delta.seconds // 3600 > 0:
            delta = str(delta.seconds // 3600) + "시간 전"
        else: delta = str(delta.seconds // 60) + "분 전"
        data = {
            "post_id": instance.id,
            "title": instance.title,
            "content_preview": instance.content[0:60],
            "created_at": delta
        }
        user = User.objects.get(uuid = instance.user_id)
        user_data = {
            "user_name": user.username,
            "profile_icon": UserDetailsStatic.objects.get(user_id = user.uuid).profile_icon
        }
        count = PostCount.objects.get(post_id = instance.id)
        count = {
            "count_likes": count.count_likes,
            "count_comments": count.count_comments
        }
        preview = {
            "user_date": user_data,
            "post_data": data,
            "count": count
        }
        return_data.append(preview)
    return Response(return_data)


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
        "post": post.order_by('-creation_date'),
        "count": count
    }
    serializer = PostPreviewSerializer(preview)
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
    serializer = QnaPreviewSerializer(preview)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([])
def getQnaMainSolved(request):
    index = (int(request.GET['page_num']) - 1) * 10
    qna = Qna.objects.filter(solved = True).order_by('-creation_date')[index:index + 10]
    count = QnaCount.objects.none()
    for id in list(qna.values_list('id', flat = True)):
        instance = QnaCount.objects.filter(qna_id = id)
        count = count | instance
    preview = {
        "qna": qna,
        "count": count.order_by('-creation_date')
    }
    serializer = QnaPreviewSerializer(preview)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([])
def getQnaMainUnsolved(request):
    index = (int(request.GET['page_num']) - 1) * 10
    qna = Qna.objects.filter(solved = False).order_by('-creation_date')[index:index + 10]
    count = QnaCount.objects.none()
    for id in list(qna.values_list('id', flat = True)):
        instance = QnaCount.objects.filter(qna_id = id)
        count = count | instance
    preview = {
        "qna": qna,
        "count": count.order_by('-creation_date')
    }
    serializer = QnaPreviewSerializer(preview)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([])
def getQnaMainType(request):
    _type = int(request.GET['type'])
    index = (int(request.GET['page_num']) - 1) * 10
    qna = Qna.objects.filter(type = _type).order_by('-creation_date')[index:index + 10]
    count = QnaCount.objects.none()
    for id in list(qna.values_list('id', flat = True)):
        instance = QnaCount.objects.filter(qna_id = id)
        count = count | instance
    preview = {
        "qna": qna,
        "count": count.order_by('-creation_date')
    }
    serializer = QnaPreviewSerializer(preview)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([])
def getUserPostQna(request):
    _user_id = request.GET['user_id']
    post = Post.objects.filter(user_id = _user_id).order_by('-creation_date')
    qna = Qna.objects.filter(user_id = _user_id).order_by('-creation_date')
    total = {
        "post": post,
        "qna": qna
    }
    serializer = PostQnaSerializer(total)
    return Response(serializer.data)
    
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
    _post_id = request.GET['post_id']
    comment = PostComment.objects.filter(post_id = _post_id).order_by('-creation_date')
    comment_count = PostCommentCount.objects.none()
    user = User.objects.none()
    user_profile = UserDetailsStatic.objects.none()
    print(list(comment.values_list('id', flat = True)))
    for id in list(comment.values_list('id', flat = True)):
        instance = PostCommentCount.objects.filter(post_comment_id = id)
        comment_count = comment_count | instance
    for id in list(comment.values_list('user_id', flat = True)):
        user_instance = User.objects.filter(uuid = id)
        user = user | user_instance
        profile_instance = UserDetailsStatic.objects.filter(user_id = id)
        user_profile = user_profile | profile_instance
    print(user, user_profile)
    print(user_profile.values('profile_icon'))
    total = {
        "comment": comment,
        "comment_count": comment_count,
        "user_name": user,
        "user_profile": user_profile
    }
    serializer = PostCommentViewSerializer(total)
    return Response(serializer.data)

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