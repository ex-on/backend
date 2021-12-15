from django.http.response import HttpResponse
from rest_framework import status
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
    if num < 10:
        return "0" + str(num)
    else:
        return str(num)


def timecalculator(date_time):
    delta = (datetime.datetime.now() - date_time.replace(tzinfo=None)).seconds
    if datetime.date.today() != date_time.date():
        return zeroadder(date_time.month) + "/" + zeroadder(date_time.day)
    elif delta // 3600 > 0:
        return zeroadder(date_time.hour) + ":" + zeroadder(date_time.minute)
    else:
        return str(delta // 60) + "분 전"


@api_view(['GET'])
@permission_classes([])
def getPostPreview(request):
    type = int(request.GET['type'])
    index_num = int(request.GET['index_num'])
    index = (int(request.GET['page_num']) - 1) * index_num
    if type == 0:
        posts = Post.objects.order_by(
            '-creation_date')[index:index + index_num]
    else:
        posts = Post.objects.filter(type=type).order_by(
            '-creation_date')[index:index + index_num]
    return_data = []
    for post in posts:
        if len(post.content) > 70:
            post.content = post.content[0:70] + "..."
        post.creation_date = timecalculator(post.creation_date)
        preview = {
            "user_data": {
                "username": User.objects.get(uuid=post.user_id).username,
                "profile_icon": UserDetailsStatic.objects.get(user_id=post.user_id).profile_icon
            },
            "post_data": PostPreviewSerializer(post).data,
            "count": PostCountMiniSerializer(PostCount.objects.get(post_id=post.id)).data
        }
        return_data.append(preview)
    return Response(return_data)


@api_view(['GET'])
@permission_classes([])
def getHotBoardPreview(request):
    index_num = int(request.GET['index_num'])
    index = (int(request.GET['page_num']) - 1) * index_num
    counts = PostCount.objects.filter(count_likes__gt=9).order_by(
        '-creation_date')[index:index + index_num]
    return_data = []
    for count in counts:
        post = Post.objects.get(id=count.post_id)
        if len(post.content) > 70:
            post.content = post.content[0:70] + "..."
        post.creation_date = timecalculator(post.creation_date)
        preview = {
            "user_data": {
                "username": User.objects.get(uuid=post.user_id).username,
                "profile_icon": UserDetailsStatic.objects.get(user_id=post.user_id).profile_icon
            },
            "post_data": PostPreviewSerializer(post).data,
            "count": PostCountMiniSerializer(PostCount.objects.get(post_id=post.id)).data
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
        if len(qna.content) > 70:
            qna.content = qna.content[0:70] + "..."
        qna.creation_date = timecalculator(qna.creation_date)
        preview = {
            "user_data": {
                "username": User.objects.get(uuid=qna.user_id).username,
                "profile_icon": UserDetailsStatic.objects.get(user_id=qna.user_id).profile_icon
            },
            "post_data": QnaPreviewSerializer(qna).data,
            "count": QnaCountMiniSerializer(QnaCount.objects.get(qna_id=qna.id)).data
        }
        return_data.append(preview)
    return Response(return_data)


@api_view(['GET'])
@permission_classes([])
def getQnaMainSolved(request):
    index = (int(request.GET['page_num']) - 1) * 10
    qnas = Qna.objects.filter(solved=True).order_by(
        '-creation_date')[index:index + 10]
    return_data = []
    for qna in qnas:
        if len(qna.content) > 70:
            qna.content = qna.content[0:70] + "..."
        qna.creation_date = timecalculator(qna.creation_date)
        preview = {
            "user_data": {
                "username": User.objects.get(uuid=qna.user_id).username,
                "profile_icon": UserDetailsStatic.objects.get(user_id=qna.user_id).profile_icon
            },
            "post_data": QnaPreviewSerializer(qna).data,
            "count": QnaCountMiniSerializer(QnaCount.objects.get(qna_id=qna.id)).data
        }
        return_data.append(preview)
    return Response(return_data)


@api_view(['GET'])
@permission_classes([])
def getQnaMainUnsolved(request):
    index = (int(request.GET['page_num']) - 1) * 10
    qnas = Qna.objects.filter(solved=False).order_by(
        '-creation_date')[index:index + 10]
    return_data = []
    for qna in qnas:
        if len(qna.content) > 70:
            qna.content = qna.content[0:70] + "..."
        qna.creation_date = timecalculator(qna.creation_date)
        preview = {
            "user_data": {
                "username": User.objects.get(uuid=qna.user_id).username,
                "profile_icon": UserDetailsStatic.objects.get(user_id=qna.user_id).profile_icon
            },
            "post_data": QnaPreviewSerializer(qna).data,
            "count": QnaCountMiniSerializer(QnaCount.objects.get(qna_id=qna.id)).data
        }
        return_data.append(preview)
    return Response(return_data)


@api_view(['GET'])
@permission_classes([])
def getQnaMainType(request):
    type = int(request.GET['type'])
    index = (int(request.GET['page_num']) - 1) * 10
    qnas = Qna.objects.filter(type=type).order_by(
        '-creation_date')[index:index + 10]
    return_data = []
    for qna in qnas:
        if len(qna.content) > 70:
            qna.content = qna.content[0:70] + "..."
        qna.creation_date = timecalculator(qna.creation_date)
        preview = {
            "user_data": {
                "username": User.objects.get(uuid=qna.user_id).username,
                "profile_icon": UserDetailsStatic.objects.get(user_id=qna.user_id).profile_icon
            },
            "post_data": QnaPreviewSerializer(qna).data,
            "count": QnaCountMiniSerializer(QnaCount.objects.get(qna_id=qna.id)).data
        }
        return_data.append(preview)
    return Response(return_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserPostQna(request):
    if "user_id" in request.GET:
        user_id = request.GET['user_id']
    else:
        user_id = request.user.uuid
    posts = Post.objects.filter(
        user_id=user_id).order_by('-creation_date')[0:8]
    answers = QnaAnswer.objects.filter(
        user_id=user_id).order_by('-creation_date')[0:8]
    post_preview, qna_preview = [], []
    for post in posts:
        if len(post.content) > 70:
            post.content = post.content[0:70] + "..."
        post.creation_date = timecalculator(post.creation_date)
        data = {
            "post_data": PostPreviewSerializer(post).data,
            "count": PostCountMiniSerializer(PostCount.objects.get(post_id=post.id)).data
        }
        post_preview.append(data)
    for answer in answers:
        qna = Qna.objects.get(id=answer.qna_id)
        if len(answer.content) > 70:
            answer.content = answer.content[0:70] + "..."
        data = {
            "qna_data": {
                "qna_title": qna.title,
                "answer_content": answer.content,
                "creation_date": timecalculator(answer.creation_date)
            },
            "count": QnaCountMiniSerializer(QnaCount.objects.get(qna_id=qna.id)).data
        }
        qna_preview.append(data)
    total_data = {
        "post_num": Post.objects.filter(user_id=user_id).count(),
        "answer_num": QnaAnswer.objects.filter(user_id=user_id).count(),
        "post_data": post_preview,
        "qna_data": qna_preview
    }
    return Response(total_data)


############게시물 확인#################

@api_view(['GET'])
@permission_classes([])
def getPost(request):
    post_id = request.GET['post_id']
    post = Post.objects.get(id=post_id)
    data = {
        "user_data": {
            "username": User.objects.get(uuid=post.user_id).username,
            "profile_icon": UserDetailsStatic.objects.get(user_id=post.user_id).profile_icon
        },
        "post": PostSerializer(post).data,
    }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPostComments(request):
    uuid = request.user.uuid
    post_id = request.GET['post_id']
    comments = PostComment.objects.filter(
        post_id=post_id).order_by('creation_date')
    replies = PostCommentReply.objects.filter(post_id=post_id)
    totalDataList = []
    for comment in comments:
        replyDataList = []
        commentReplies = replies.filter(post_comment_id=comment.id)
        for reply in commentReplies:
            replyData = {
                "user_data": {
                    "username": User.objects.get(uuid=reply.user_id).username,
                    "profile_icon": UserDetailsStatic.objects.get(user_id=reply.user_id).profile_icon
                },
                "reply_data": PostCommentReplySerializer(reply).data,
                "reply_count": PostCommentReplyCountSerializer(PostCommentReplyCount.objects.get(post_comment_reply_id=reply.id)).data,
                "liked": UsersLikedPostCommentReplies.objects.filter(user_id=uuid, post_comment_reply_id=reply.id).exists()
            }
            replyDataList.append(replyData)
        data = {
            "comments": {
                "user_data": {
                    "username": User.objects.get(uuid=comment.user_id).username,
                    "profile_icon": UserDetailsStatic.objects.get(user_id=comment.user_id).profile_icon
                },
                "comment_data": PostCommentSerializer(comment).data,
                "comment_count": PostCommentCountSerializer(PostCommentCount.objects.get(post_comment_id=comment.id)).data,
                "liked": UsersLikedPostComments.objects.filter(user_id=uuid, post_comment_id=comment.id).exists()
            },
            "replies": replyDataList
        }
        totalDataList.append(data)
    return Response(totalDataList)


@api_view(['GET'])
@permission_classes([])
def getQna(request):
    _qna_id = request.GET['qna_id']
    qna = Qna.objects.filter(id=_qna_id)
    if qna.first() == None:
        qna_count = QnaCount.objects.none()
        user_name = User.objects.none()
        user_profile = UserDetailsStatic.objects.none()
    else:
        qna_count = QnaCount.objects.filter(qna_id=_qna_id)
        user_name = User.objects.filter(uuid=qna.first().user_id)
        user_profile = UserDetailsStatic.objects.filter(
            user_id=qna.first().user_id)
    total = {
        "qna": qna,
        "qna_count": qna_count,
        "username": user_name,
        "user_profile": user_profile
    }
    serializer = QnaViewSerializer(total)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([])
def getQnaAnswer(request):
    _qna_id = request.GET['qna_id']
    answer = QnaAnswer.objects.filter(qna_id=_qna_id)
    answer_count = QnaAnswerCount.objects.none()
    user = User.objects.none()
    user_profile = UserDetailsStatic.objects.none()
    for id in list(answer.values_list('id', flat=True)):
        instance = QnaAnswerCount.objects.filter(qna_answer_id=id)
        answer_count = answer_count | instance
    for user_id in list(answer.values_list('user_id', flat=True)):
        user_instance = User.objects.filter(uuid=user_id)
        user = user | user_instance
        profile_instance = UserDetailsStatic.objects.filter(user_id=user_id)
        user_profile = user_profile | profile_instance
    total = {
        "answer": answer.order_by('-creation_date'),
        "answer_count": answer_count,
        "username": user,
        "user_profile": user_profile
    }
    serializer = QnaAnswerViewSerializer(total)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([])
def getQnaAnswerCommentReply(request):
    _qna_answer_id = request.GET['qna_answer_id']
    comment = QnaAnswerComment.objects.filter(qna_answer_id=_qna_answer_id)
    reply = QnaAnswerCommentReply.objects.filter(qna_answer_id=_qna_answer_id)
    user_id_list = list(comment.values_list('user_id', flat=True)) + \
        list(reply.values_list('user_id', flat=True))
    user_name = User.objects.none()
    user_profile = UserDetailsStatic.objects.none()
    for id in user_id_list:
        user_instance = User.objects.filter(uuid=id)
        profile_instance = UserDetailsStatic.objects.filter(user_id=id)
        user_name = user_name | user_instance
        user_profile = user_profile | profile_instance
    total = {
        "comment": comment,
        "reply": reply,
        "username": user_name,
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
                         title=request['title'], content=request['content'], modified=False, type=request['type'])
    post_instance.save()
    count_instance = PostCount(
        post_id=post_instance.id, creation_date=request['creation_date'], count_likes=0, count_comments=0, count_saved=0, count_reports=0)
    count_instance.save()
    return HttpResponse(status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def postPostComment(request):
    uuid = request.user.uuid
    data = json.loads(request.body)
    comment_instance = PostComment(user_id=uuid, post_id=data['post_id'],
                                   content=data['content'])
    comment_instance.save()
    count_instance = PostCommentCount(
        post_comment_id=comment_instance.id, count_likes=0, count_reports=0)
    count_instance.save()
    post_count = PostCount.objects.get(post_id=data['post_id'])
    post_count.count_comments += 1
    post_count.save()
    return HttpResponse(status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def postPostCommentReply(request):
    uuid = request.user.uuid
    data = json.loads(request.body)
    reply_instance = PostCommentReply(user_id=uuid, post_id=data['post_id'],
                                      post_comment_id=data['post_comment_id'], content=data['content'])
    reply_instance.save()
    count_instance = PostCommentReplyCount(
        post_comment_reply_id=reply_instance.id,)
    count_instance.save()
    post_count = PostCount.objects.get(post_id=data['post_id'])
    post_count.count_comments += 1
    post_count.save()
    return HttpResponse(status=200)


@api_view(['POST'])
@permission_classes([])
def postQna(request):
    request = json.loads(request.body)
    qna_instance = Qna(user_id=request['user_id'], title=request['title'], content=request['content'],
                       creation_date=request['creation_date'], modified=False, solved=False, type=request['type'])
    qna_instance.save()
    count_instance = QnaCount(qna_id=qna_instance.id, creation_date=request['creation_date'],
                              count_total_likes=0, count_answers=0, count_saved=0, count_total_comments=0, count_reports=0)
    count_instance.save()
    return HttpResponse(status=200)


@api_view(['POST'])
@permission_classes([])
def postQnaAnswer(request):
    request = json.loads(request.body)
    answer_instance = QnaAnswer(user_id=request['user_id'], qna_id=request['qna_id'],
                                content=request['content'], creation_date=request['creation_date'])
    answer_instance.save()
    count_instance = QnaAnswerCount(
        qna_answer_id=answer_instance.id, count_likes=0, count_comments=0, count_reports=0)
    count_instance.save()
    return HttpResponse(status=200)


@api_view(['POST'])
@permission_classes([])
def postQnaAnswerComment(request):
    request = json.loads(request.body)
    answer_instance = QnaAnswerComment(
        user_id=request['user_id'], qna_answer_id=request['qna_answer_id'], content=request['content'], creation_date=request['creation_date'])
    answer_instance.save()
    return HttpResponse(status=200)


@api_view(['POST'])
@permission_classes([])
def postQnaAnswerCommentReply(request):
    request = json.loads(request.body)
    answer_instance = QnaAnswerCommentReply(user_id=request['user_id'], qna_answer_id=request['qna_answer_id'],
                                            qna_answer_comment_id=request['qna_answer_comment_id'], content=request['content'], creation_date=request['creation_date'])
    answer_instance.save()
    return HttpResponse(status=200)

############ 게시물 수정 #######################


@api_view(['POST'])
@permission_classes([])
def modifyPost(request):
    request = json.loads(request.body)
    post = Post.objects.get(id=request['post_id'])
    post.title = request['title']
    post.content = request['content']
    post.type = request['type']
    post.modified = True
    post.save()
    return HttpResponse(status=200)


@api_view(['POST'])
@permission_classes([])
def modifyPostComment(request):
    request = json.loads(request.body)
    comment = PostComment.objects.get(id=request['comment_id'])
    comment.content = request['content']
    comment.save()
    return HttpResponse(status=200)


@api_view(['POST'])
@permission_classes([])
def modifyPostCommentReply(request):
    request = json.loads(request.body)
    reply = PostCommentReply.objects.get(id=request['reply_id'])
    reply.content = request['content']
    reply.save()
    return HttpResponse(status=200)


@api_view(['POST'])
@permission_classes([])
def modifyQna(request):
    request = json.loads(request.body)
    qna = Qna.objects.get(id=request['qna_id'])
    qna.title = request['title']
    qna.content = request['content']
    qna.type = request['type']
    qna.modified = True
    qna.save()
    return HttpResponse(status=200)


@api_view(['POST'])
@permission_classes([])
def modifyQnaAnswer(request):
    request = json.loads(request.body)
    answer = QnaAnswer.objects.get(id=request['answer_id'])
    answer.content = request['content']
    answer.save()
    return HttpResponse(status=200)


@api_view(['POST'])
@permission_classes([])
def modifyQnaAnswerComment(request):
    request = json.loads(request.body)
    comment = QnaAnswerComment.objects.get(id=request['comment_id'])
    comment.content = request['content']
    comment.save()
    return HttpResponse(status=200)


@api_view(['POST'])
@permission_classes([])
def modifyQnaAnswerCommentReply(request):
    request = json.loads(request.body)
    reply = QnaAnswerCommentReply.objects.get(id=request['reply_id'])
    reply.content = request['content']
    reply.save()
    return HttpResponse(status=200)

    ########게시물 좋아요, 저장###############


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPostUserStatus(request):
    uuid = request.user.uuid
    postId = request.GET['post_id']
    extent = request.GET['extent']
    resData = {}
    if (extent == 'likes' or 'all'):
        isLiked = UsersLikedPosts.objects.filter(
            user_id=uuid, post_id=postId).exists()
        resData['is_liked'] = isLiked
    if (extent == 'saved' or 'all'):
        isSaved = UsersSavedPosts.objects.filter(
            user_id=uuid, post_id=postId).exists()
        resData['is_saved'] = isSaved
    return Response(resData)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPostCount(request):
    post_id = request.GET['post_id']
    post_count = PostCount.objects.get(post_id=post_id)
    data = PostCountSerializer(post_count).data

    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPostCommentsCount(request):
    postId = request.GET['post_id']
    postComments = PostComment.objects.filter(post_id=postId)
    postCommentsCount = []
    for comment in postComments:
        postCommentCount = PostCommentCount.objects.get(
            post_comment_id=comment.id)
        postCommentsCount.append(postCommentCount)
    data = PostCommentCountSerializer(postCommentsCount, many=True).data

    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updatePostLikeCount(request):
    uuid = request.user.uuid
    data = json.loads(request.body)
    postCount = PostCount.objects.get(post_id=data['post_id'])
    if data['add'] == True:
        postCount.count_likes += 1
        usersLikedPosts = UsersLikedPosts(
            user_id=uuid, post_id=data['post_id'])
        postCount.save()
        usersLikedPosts.save()
    else:
        postCount.count_likes -= 1
        usersLikedPosts = UsersLikedPosts.objects.filter(
            user_id=uuid, post_id=data['post_id'])
        postCount.save()
        usersLikedPosts.delete()
    return HttpResponse(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updatePostSavedCount(request):
    uuid = request.user.uuid
    data = json.loads(request.body)
    postCount = PostCount.objects.get(post_id=data['post_id'])
    if data['add'] == True:
        print('add saved')
        postCount.count_saved += 1
        usersSavedPosts = UsersSavedPosts(
            user_id=uuid, post_id=data['post_id'])
        postCount.save()
        usersSavedPosts.save()
    else:
        postCount.count_saved -= 1
        usersSavedPosts = UsersSavedPosts.objects.filter(
            user_id=uuid, post_id=data['post_id'])
        postCount.save()
        usersSavedPosts.delete()
    return HttpResponse(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updatePostCommentLikeCount(request):
    uuid = request.user.uuid
    data = json.loads(request.body)
    postCommentCount = PostCommentCount.objects.get(
        post_comment_id=data['post_comment_id'])
    if data['add'] == True:
        postCommentCount.count_likes += 1
        usersLikedPostComments = UsersLikedPostComments(
            user_id=uuid, post_comment_id=data['post_comment_id'])
        postCommentCount.save()
        usersLikedPostComments.save()
    else:
        postCommentCount.count_likes -= 1
        usersLikedPostComments = UsersLikedPostComments.objects.filter(
            user_id=uuid, post_comment_id=data['post_comment_id'])
        postCommentCount.save()
        usersLikedPostComments.delete()
    return HttpResponse(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updatePostCommentReplyLikeCount(request):
    uuid = request.user.uuid
    data = json.loads(request.body)
    postCommentReplyCount = PostCommentReplyCount.objects.get(
        post_comment_reply_id=data['post_comment_reply_id'])
    if data['add'] == True:
        postCommentReplyCount.count_likes += 1
        usersLikedPostCommentReplies = UsersLikedPostCommentReplies(
            user_id=uuid, post_comment_reply_id=data['post_comment_reply_id'])
        postCommentReplyCount.save()
        usersLikedPostCommentReplies.save()
    else:
        postCommentReplyCount.count_likes -= 1
        usersLikedPostCommentReplies = UsersLikedPostCommentReplies.objects.filter(
            user_id=uuid, post_comment_reply_id=data['post_comment_reply_id'])
        postCommentReplyCount.save()
        usersLikedPostCommentReplies.delete()
    return HttpResponse(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSavedPostPreview(request):
    user_id = request.user.uuid
    userSavedPosts = UsersSavedPosts.objects.filter(user_id=user_id)

    postData = []
    for data in userSavedPosts:
        post = Post.objects.get(id=data.post_id)
        if len(post.content) > 70:
            post.content = post.content[0:70] + "..."
        post.creation_date = timecalculator(post.creation_date)
        preview = {
            "user_data": {
                "username": User.objects.get(uuid=post.user_id).username,
                "profile_icon": UserDetailsStatic.objects.get(user_id=post.user_id).profile_icon
            },
            "post_data": PostPreviewSerializer(post).data,
            "count": PostCountMiniSerializer(PostCount.objects.get(post_id=post.id)).data
        }
        postData.append(preview)

    return Response(postData)
