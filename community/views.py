import re
from django.db.models.query import QuerySet
from django.http.response import HttpResponse
from django.db import IntegrityError
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
from itertools import chain
from operator import attrgetter

# Create your views here.

############게시판 메인화면###############


def zeroAdder(num):
    if num < 10:
        return "0" + str(num)
    else:
        return str(num)


def timeCalculator(date_time):
    delta = (datetime.datetime.now() - date_time.replace(tzinfo=None)).seconds
    if datetime.date.today() != date_time.date():
        return zeroAdder(date_time.month) + "/" + zeroAdder(date_time.day)
    elif delta // 3600 > 0:
        return zeroAdder(date_time.hour) + ":" + zeroAdder(date_time.minute)
    else:
        return str(delta // 60) + "분 전"


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPostPreview(request):
    postType = int(request.GET['type'])
    indexNum = int(request.GET['index_num'])
    # startIndex = (int(request.GET['page_num']) - 1) * index_num
    startIndex = int(request.GET['start_index'])
    if postType == 0:
        posts = Post.objects.order_by(
            '-created_at')[startIndex:startIndex + indexNum]
    else:
        posts = Post.objects.filter(type=postType).order_by(
            '-created_at')[startIndex:startIndex + indexNum]
    return_data = []
    for post in posts:
        if len(post.content) > 70:
            post.content = post.content[0:70] + "..."
        post.created_at = timeCalculator(post.created_at)
        preview = {
            "user_data": {
                "username": User.objects.get(uuid=post.user_id).username,
                "activity_level": UserDetailsStatic.objects.get(user_id=post.user_id).activity_level
            },
            "post_data": PostPreviewSerializer(post).data,
            "count": PostCountMiniSerializer(PostCount.objects.get(post_id=post.id)).data
        }
        return_data.append(preview)
    return Response(return_data)


@api_view(['GET'])
@permission_classes([])
def getHotPostPreview(request):
    indexNum = int(request.GET['index_num'])
    startIndex = int(request.GET['start_index'])
    counts = PostCount.objects.filter(count_likes__gt=9).order_by(
        '-created_at')[startIndex:startIndex + indexNum]
    return_data = []
    for count in counts:
        post = Post.objects.get(id=count.post_id)
        if len(post.content) > 70:
            post.content = post.content[0:70] + "..."
        post.created_at = timeCalculator(post.created_at)
        preview = {
            "user_data": {
                "username": User.objects.get(uuid=post.user_id).username,
                "activity_level": UserDetailsStatic.objects.get(user_id=post.user_id).activity_level
            },
            "post_data": PostPreviewSerializer(post).data,
            "count": PostCountMiniSerializer(PostCount.objects.get(post_id=post.id)).data
        }
        return_data.append(preview)
    return Response(return_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getQnaPreview(request):
    qnaType = int(request.GET['type'])
    indexNum = int(request.GET['index_num'])
    startIndex = int(request.GET['start_index'])
    if qnaType == 0:
        qnas = Qna.objects.order_by('-created_at')[startIndex:startIndex + 10]
    else:
        qnas = Qna.objects.filter(type=qnaType).order_by(
            '-created_at')[startIndex:startIndex + indexNum]
    return_data = []
    for qna in qnas:
        if len(qna.content) > 70:
            qna.content = qna.content[0:70] + "..."
        qna.created_at = timeCalculator(qna.created_at)
        preview = {
            "user_data": {
                "username": User.objects.get(uuid=qna.user_id).username,
                "activity_level": UserDetailsStatic.objects.get(user_id=qna.user_id).activity_level
            },
            "qna_data": QnaPreviewSerializer(qna).data,
            "count": QnaCountMiniSerializer(QnaCount.objects.get(qna_id=qna.id)).data
        }
        return_data.append(preview)
    return Response(return_data)


@api_view(['GET'])
@permission_classes([])
def getHotQnaPreview(request):
    indexNum = int(request.GET['index_num'])
    startIndex = int(request.GET['start_index'])
    counts = QnaCount.objects.filter(count_likes__gt=9).order_by(
        '-created_at')[startIndex:startIndex + indexNum]
    return_data = []
    for count in counts:
        qna = Qna.objects.get(id=count.qna_id)
        if len(qna.content) > 70:
            qna.content = qna.content[0:70] + "..."
        qna.created_at = timeCalculator(qna.created_at)
        preview = {
            "user_data": {
                "username": User.objects.get(uuid=qna.user_id).username,
                "activity_level": UserDetailsStatic.objects.get(user_id=qna.user_id).activity_level
            },
            "qna_data": QnaPreviewSerializer(qna).data,
            "count": QnaCountMiniSerializer(QnaCount.objects.get(qna_id=qna.id)).data
        }
        return_data.append(preview)
    return Response(return_data)


@api_view(['GET'])
@permission_classes([])
def getQnaMainSolved(request):
    index = (int(request.GET['page_num']) - 1) * 10
    qnas = Qna.objects.filter(solved=True).order_by(
        '-created_at')[index:index + 10]
    return_data = []
    for qna in qnas:
        if len(qna.content) > 70:
            qna.content = qna.content[0:70] + "..."
        qna.created_at = timeCalculator(qna.created_at)
        preview = {
            "user_data": {
                "username": User.objects.get(uuid=qna.user_id).username,
                "activity_level": UserDetailsStatic.objects.get(user_id=qna.user_id).activity_level
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
        '-created_at')[index:index + 10]
    return_data = []
    for qna in qnas:
        if len(qna.content) > 70:
            qna.content = qna.content[0:70] + "..."
        qna.created_at = timeCalculator(qna.created_at)
        preview = {
            "user_data": {
                "username": User.objects.get(uuid=qna.user_id).username,
                "activity_level": UserDetailsStatic.objects.get(user_id=qna.user_id).activity_level
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
        '-created_at')[index:index + 10]
    return_data = []
    for qna in qnas:
        if len(qna.content) > 70:
            qna.content = qna.content[0:70] + "..."
        qna.created_at = timeCalculator(qna.created_at)
        preview = {
            "user_data": {
                "username": User.objects.get(uuid=qna.user_id).username,
                "activity_level": UserDetailsStatic.objects.get(user_id=qna.user_id).activity_level
            },
            "post_data": QnaPreviewSerializer(qna).data,
            "count": QnaCountMiniSerializer(QnaCount.objects.get(qna_id=qna.id)).data
        }
        return_data.append(preview)
    return Response(return_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserRecentPostQna(request):
    if "user_id" in request.GET:
        user_id = request.GET['user_id']
    else:
        user_id = request.user.uuid
    posts = Post.objects.filter(
        user_id=user_id).order_by('-created_at')[0:8]
    answers = QnaAnswer.objects.filter(
        user_id=user_id).order_by('-created_at')[0:8]
    post_preview, qna_preview = [], []
    for post in posts:
        if len(post.content) > 70:
            post.content = post.content[0:70] + "..."
        post.created_at = timeCalculator(post.created_at)
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
                "created_at": timeCalculator(answer.created_at),
                "id": qna.id,
                "type": qna.type
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
            "activity_level": UserDetailsStatic.objects.get(user_id=post.user_id).activity_level
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
        post_id=post_id).order_by('created_at')
    replies = PostCommentReply.objects.filter(post_id=post_id)
    totalDataList = []
    for comment in comments:
        replyDataList = []
        commentReplies = replies.filter(post_comment_id=comment.id)
        for reply in commentReplies:
            replyData = {
                "user_data": {
                    "username": User.objects.get(uuid=reply.user_id).username,
                    "activity_level": UserDetailsStatic.objects.get(user_id=reply.user_id).activity_level
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
                    "activity_level": UserDetailsStatic.objects.get(user_id=comment.user_id).activity_level
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
    qna_id = request.GET['qna_id']
    qna = Qna.objects.get(id=qna_id)
    data = {
        "user_data": {
            "username": User.objects.get(uuid=qna.user_id).username,
            "activity_level": UserDetailsStatic.objects.get(user_id=qna.user_id).activity_level
        },
        "qna": QnaSerializer(qna).data,
    }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getQnaAnswers(request):
    uuid = request.user.uuid
    qna_id = request.GET['qna_id']
    answers = QnaAnswer.objects.filter(qna_id=qna_id)
    dataList = []
    for answer in answers:
        dataList.append({
            "user_data": {
                "username": User.objects.get(uuid=answer.user_id).username,
                "activity_level": UserDetailsStatic.objects.get(user_id=answer.user_id).activity_level
            },
            "answer_data": QnaAnswerSerializer(answer).data,
            "answer_count": QnaAnswerCountSerializer(QnaAnswerCount.objects.get(qna_answer_id=answer.id)).data,
            "liked": UsersLikedQnaAnswers.objects.filter(user_id=uuid, qna_answer_id=answer.id).exists()
        })
    return Response(dataList)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getQnaAnswerComments(request):
    uuid = request.user.uuid
    answer_id = request.GET['answer_id']
    comments = QnaAnswerComment.objects.filter(qna_answer_id=answer_id)
    replies = QnaAnswerCommentReply.objects.filter(qna_answer_id=answer_id)
    dataList = []
    for comment in comments:
        replyDataList = []
        commentReplies = replies.filter(qna_answer_comment_id=comment.id)
        for reply in commentReplies:
            replyData = {
                "user_data": {
                    "username": User.objects.get(uuid=reply.user_id).username,
                    "activity_level": UserDetailsStatic.objects.get(user_id=reply.user_id).activity_level
                },
                "reply_data": QnaAnswerCommentReplySerializer(reply).data,
            }
            replyDataList.append(replyData)
        data = {
            "comment": {
                "user_data": {
                    "username": User.objects.get(uuid=comment.user_id).username,
                    "activity_level": UserDetailsStatic.objects.get(user_id=comment.user_id).activity_level
                },
                "comment_data": QnaAnswerCommentSerializer(comment).data,
                "comment_count": QnaAnswerCommentCountSerializer(QnaAnswerCommentCount.objects.get(qna_answer_comment_id=comment.id)).data,
                "liked": UsersLikedQnaAnswerComments.objects.filter(user_id=uuid, qna_answer_comment_id=comment.id).exists()
            },
            "replies": replyDataList
        }
        dataList.append(data)

    return Response(dataList)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getQnaUserStatus(request):
    uuid = request.user.uuid
    qnaId = request.GET['qna_id']
    isSaved = UsersSavedQnas.objects.filter(
        user_id=uuid, qna_id=qnaId).exists()
    resData = {
        'is_saved': isSaved
    }
    return Response(resData)

############게시물 작성#################


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def postPost(request):
    uuid = request.user.uuid
    request = json.loads(request.body)
    post = Post(user_id=uuid, title=request['title'], content=request['content'], modified=False, type=request['type'])
    post.save()
    postCount = PostCount(
        post_id=post.id, count_likes=0, count_comments=0, count_saved=0, count_reports=0)
    postCount.save()
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
    postCount = PostCount.objects.get(post_id=data['post_id'])
    postCount.count_comments += 1
    postCount.save()
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
    postCount = PostCount.objects.get(post_id=data['post_id'])
    postCount.count_comments += 1
    postCount.save()
    return HttpResponse(status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def postQna(request):
    uuid = request.user.uuid
    request = json.loads(request.body)
    qna = Qna(user_id=uuid, title=request['title'], content=request['content'],
                     modified=False, solved=False, type=request['type'])
    qna.save()
    qnaCount = QnaCount(qna_id=qna.id,
                              count_likes=0, count_answers=0, count_saved=0, count_comments=0, count_reports=0)
    qnaCount.save()
    return HttpResponse(status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def postQnaAnswer(request):
    uuid = request.user.uuid
    request = json.loads(request.body)
    answer = QnaAnswer(user_id=uuid, qna_id=request['qna_id'],
                                content=request['content'])
    answer.save()
    answerCount = QnaAnswerCount(
        qna_answer_id=answer.id, count_likes=0, count_comments=0, count_reports=0)
    answerCount.save()
    return HttpResponse(status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def postQnaAnswerComment(request):
    uuid = request.user.uuid
    request = json.loads(request.body)
    comment = QnaAnswerComment(
        user_id=uuid, qna_answer_id=request['answer_id'], content=request['content'])
    comment.save()
    commentCount = QnaAnswerCommentCount(
        qna_answer_comment_id=comment.id, count_likes=0, count_reports=0)
    commentCount.save()
    answerCount = QnaAnswerCount.objects.get(qna_answer_id=request['answer_id'])
    answerCount.count_comments += 1
    answerCount.save()
    return HttpResponse(status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def postQnaAnswerCommentReply(request):
    uuid = request.user.uuid
    request = json.loads(request.body)
    reply = QnaAnswerCommentReply(user_id=uuid, qna_answer_id=request['answer_id'],
                                  qna_answer_comment_id=request['qna_answer_comment_id'], content=request['content'])
    reply.save()
    answerCount = QnaAnswerCount.objects.get(qna_answer_id=request['answer_id'])
    answerCount.count_comments += 1
    answerCount.save()
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
def getQnaCount(request):
    qna_id = request.GET['qna_id']
    qna_count = QnaCount.objects.get(qna_id=qna_id)
    data = QnaCountSerializer(qna_count).data

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
        postCount.count_saved += 1
        usersSavedPosts = UsersSavedPosts(
            user_id=uuid, post_id=data['post_id'])
        postCount.save()
        usersSavedPosts.save()
    else:
        postCount.count_saved -= 1
        usersSavedPosts = UsersSavedPosts.objects.get(
            user_id=uuid, post_id=data['post_id'])
        postCount.save()
        usersSavedPosts.delete()
    return HttpResponse(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateQnaSavedCount(request):
    uuid = request.user.uuid
    data = json.loads(request.body)
    qnaCount = QnaCount.objects.get(qna_id=data['qna_id'])
    if data['add'] == True:
        qnaCount.count_saved += 1
        usersSavedQnas = UsersSavedQnas(
            user_id=uuid, qna_id=data['qna_id'])
        qnaCount.save()
        usersSavedQnas.save()
    else:
        qnaCount.count_saved -= 1
        usersSavedQnas = UsersSavedQnas.objects.get(
            user_id=uuid, qna_id=data['qna_id'])
        qnaCount.save()
        usersSavedQnas.delete()
    return HttpResponse(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateQnaAnswerLikeCount(request):
    uuid = request.user.uuid
    data = json.loads(request.body)
    qnaAnswerCount = QnaAnswerCount.objects.get(
        qna_answer_id=data['qna_answer_id'])
    if data['add'] == True:
        qnaAnswerCount.count_likes += 1
        usersLikedQnaAnswers = UsersLikedQnaAnswers(
            user_id=uuid, qna_answer_id=data['qna_answer_id'])
        qnaAnswerCount.save()
        usersLikedQnaAnswers.save()
    else:
        qnaAnswerCount.count_likes -= 1
        usersLikedQnaAnswers = UsersLikedQnaAnswers.objects.filter(
            user_id=uuid, qna_answer_id=data['qna_answer_id'])
        qnaAnswerCount.save()
        usersLikedQnaAnswers.delete()
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
def updateQnaAnswerCommentLikeCount(request):
    uuid = request.user.uuid
    data = json.loads(request.body)
    qnaAnswerCommentCount = QnaAnswerCommentCount.objects.get(
        qna_answer_comment_id=data['qna_answer_comment_id'])
    if data['add'] == True:
        qnaAnswerCommentCount.count_likes += 1
        usersLikedQnaAnswerComments = UsersLikedQnaAnswerComments(
            user_id=uuid, qna_answer_comment_id=data['qna_answer_comment_id'])
        qnaAnswerCommentCount.save()
        usersLikedQnaAnswerComments.save()
    else:
        qnaAnswerCommentCount.count_likes -= 1
        usersLikedQnaAnswerComments = UsersLikedQnaAnswerComments.objects.filter(
            user_id=uuid, qna_answer_comment_id=data['qna_answer_comment_id'])
        qnaAnswerCommentCount.save()
        usersLikedQnaAnswerComments.delete()
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
def getSavedPostQnaPreview(request):
    user_id = request.user.uuid
    userSavedPosts = UsersSavedPosts.objects.filter(user_id=user_id)
    posts = Post.objects.none()
    for userSavedPost in userSavedPosts:
        data = Post.objects.filter(id=userSavedPost.post_id)
        posts = posts.union(data)
    userSavedQnas = UsersSavedQnas.objects.filter(user_id=user_id)
    qnas = Qna.objects.none()
    for userSavedQna in userSavedQnas:
        data = Qna.objects.filter(id=userSavedQna.qna_id)
        qnas = qnas.union(data)
    userSaved = sorted(chain(posts, qnas), key=attrgetter(
        'created_at'), reverse=True)
    savedData = []
    for data in userSaved:
        if isinstance(data, Post):
            if len(data.content) > 70:
                data.content = data.content[0:70] + "..."
            data.created_at = timeCalculator(data.created_at)
            preview = {
                "user_data": {
                    "username": User.objects.get(uuid=data.user_id).username,
                    "activity_level": UserDetailsStatic.objects.get(user_id=data.user_id).activity_level
                },
                "post_data": PostPreviewSerializer(data).data,
                "count": PostCountMiniSerializer(PostCount.objects.get(post_id=data.id)).data
            }
            savedData.append(preview)
        else:
            if len(data.content) > 70:
                data.content = data.content[0:70] + "..."
            data.created_at = timeCalculator(data.created_at)
            preview = {
                "user_data": {
                    "username": User.objects.get(uuid=data.user_id).username,
                    "activity_level": UserDetailsStatic.objects.get(user_id=data.user_id).activity_level
                },
                "qna_data": QnaPreviewSerializer(data).data,
                "count": QnaCountMiniSerializer(QnaCount.objects.get(qna_id=data.id)).data
            }
            savedData.append(preview)

    return Response(savedData)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateUserReportedPosts(request):
    request = json.loads(request.body)
    try:
        UsersReportedPosts.objects.create(
            user_id=request['user_id'], post_id=request['post_id'])
        return HttpResponse(status=status.HTTP_200_OK)
    except IntegrityError:
        pass
        return HttpResponse(status=status.HTTP_208_ALREADY_REPORTED)


@api_view(['POST'])
@permission_classes([])
def updateUserReportedPostComments(request):
    request = json.loads(request.body)
    try:
        UsersReportedPostComments.objects.create(
            user_id=request['user_id'], comment_id=request['comment_id'])
        return HttpResponse(status=status.HTTP_200_OK)
    except IntegrityError:
        pass
        return HttpResponse(status=status.HTTP_208_ALREADY_REPORTED)


@api_view(['POST'])
@permission_classes([])
def updateUserReportedPostCommentReplies(request):
    request = json.loads(request.body)
    try:
        UsersReportedPostCommentReplies.objects.create(
            user_id=request['user_id'], reply_id=request['reply_id'])
        return HttpResponse(status=status.HTTP_200_OK)
    except IntegrityError:
        pass
        return HttpResponse(status=status.HTTP_208_ALREADY_REPORTED)


@api_view(['POST'])
@permission_classes([])
def updateUserReportedQnas(request):
    request = json.loads(request.body)
    try:
        UsersReportedQnas.objects.create(
            user_id=request['user_id'], qna_id=request['qna_id'])
        return HttpResponse(status=status.HTTP_200_OK)
    except IntegrityError:
        pass
        return HttpResponse(status=status.HTTP_208_ALREADY_REPORTED)


@api_view(['POST'])
@permission_classes([])
def updateUserReportedQnaAnswers(request):
    request = json.loads(request.body)
    try:
        UsersReportedQnaAnswers.objects.create(
            user_id=request['user_id'], answer_id=request['answer_id'])
        return HttpResponse(status=status.HTTP_200_OK)
    except IntegrityError:
        pass
        return HttpResponse(status=status.HTTP_208_ALREADY_REPORTED)


@api_view(['POST'])
@permission_classes([])
def updateUserReportedQnaAnswerComments(request):
    request = json.loads(request.body)
    try:
        UsersReportedQnaAnswerComments.objects.create(
            user_id=request['user_id'], comment_id=request['comment_id'])
        return HttpResponse(status=status.HTTP_200_OK)
    except IntegrityError:
        pass
        return HttpResponse(status=status.HTTP_208_ALREADY_REPORTED)


@api_view(['POST'])
@permission_classes([])
def updateUserReportedQnaAnswerCommentReplies(request):
    request = json.loads(request.body)
    try:
        UsersReportedQnaAnswerCommentReplies.objects.create(
            user_id=request['user_id'], reply_id=request['reply_id'])
        return HttpResponse(status=status.HTTP_200_OK)
    except IntegrityError:
        pass
        return HttpResponse(status=status.HTTP_208_ALREADY_REPORTED)


@api_view(['POST'])
@permission_classes([])
def deletePost(request):
    request = json.loads(request.body)
    instance = Post.objects.get(
        user_id=request['user_id'], id=request['post_id'])
    instance.delete()
    return HttpResponse(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([])
def deletePostComment(request):
    request = json.loads(request.body)
    instance = PostComment.objects.get(
        user_id=request['user_id'], id=request['comment_id'])
    instance.delete()
    return HttpResponse(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([])
def deletePostCommentReply(request):
    request = json.loads(request.body)
    instance = PostCommentReply.objects.get(
        user_id=request['user_id'], id=request['reply_id'])
    instance.delete()
    return HttpResponse(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([])
def deleteQna(request):
    request = json.loads(request.body)
    instance = Qna.objects.get(
        user_id=request['user_id'], id=request['qna_id'])
    instance.delete()
    return HttpResponse(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([])
def deleteQnaAnswer(request):
    request = json.loads(request.body)
    instance = QnaAnswer.objects.get(
        user_id=request['user_id'], id=request['answer_id'])
    instance.delete()
    return HttpResponse(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([])
def deleteQnaAnswerComment(request):
    request = json.loads(request.body)
    instance = QnaAnswerComment.objects.get(
        user_id=request['user_id'], id=request['comment_id'])
    instance.delete()
    return HttpResponse(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([])
def deleteQnaAnswerCommentReply(request):
    request = json.loads(request.body)
    instance = QnaAnswerCommentReply.objects.get(
        user_id=request['user_id'], id=request['reply_id'])
    instance.delete()
    return HttpResponse(status=status.HTTP_200_OK)
