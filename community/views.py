import re
from django.db.models.query import QuerySet
from django.http.response import HttpResponse
from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
import json
from rest_framework.permissions import IsAuthenticated
from community.serializers import *
import datetime
from core.utils.transformers import timeCalculator

from notifications.fcm_notification import hot_post_fcm, hot_qna_fcm, post_comment_fcm, post_reply_fcm, qna_comment_fcm, qna_reply_fcm, qna_answer_fcm, qna_best_answer_fcm, qna_selected_answer_fcm
from .models import *
from users.models import *
from itertools import chain
from operator import attrgetter
from django.db.models import Q
# Create your views here.

############게시판 메인화면###############
def buildPostPreview(post):
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
    return preview


def buildQnaPreview(qna):
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
    return preview


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search(request):
    category = int(request.GET['category'])
    text = request.GET['text']
    data = []
    # 0: 게시판, 1: HOT 게시판, 2: 자유 게시판, 3: 정보 게시판, 4: Q&A, 5: HOT Q&A, 6: 미해결 Q&A, 7: 해결 Q&A
    if category == 0:
        posts = Post.objects.filter(Q(content__icontains=text) | Q(
            title__icontains=text)).order_by('-created_at')
        for post in posts:
            data.append(buildPostPreview(post))
    elif category == 1:
        counts = PostCount.objects.filter(count_likes__gt=9).order_by(
            '-created_at')
        hotPosts = Post.objects.none()
        for count in counts:
            hotPosts = hotPosts | Post.objects.filter(id=count.post_id)
        resultPosts = hotPosts.filter(
            Q(content__icontains=text) | Q(title__icontains=text))
        for post in resultPosts:
            data.append(buildPostPreview(post))
    elif category == 2:
        posts = Post.objects.filter(
            Q(type=1) & (Q(content__icontains=text) | Q(title__icontains=text))).order_by('-created_at')
        for post in posts:
            data.append(buildPostPreview(post))
    elif category == 3:
        posts = Post.objects.filter(
            Q(type=2) & (Q(content__icontains=text) | Q(title__icontains=text))).order_by('-created_at')
        for post in posts:
            data.append(buildPostPreview(post))
    elif category == 4:
        qnas = Qna.objects.filter(
            Q(content__icontains=text) | Q(title__icontains=text)).order_by('-created_at')
        for qna in qnas:
            data.append(buildQnaPreview(qna))
    elif category == 5:
        counts = QnaCount.objects.filter(
            count_likes__gt=9).order_by('-created_at')
        hotQnas = Qna.objects.none()
        for count in counts:
            hotQnas = hotQnas | Qna.objects.filter(id=count.qna_id)
        resultQnas = hotQnas.filter(
            Q(content__icontains=text) | Q(title__icontains=text))
        for qna in resultQnas:
            data.append(buildQnaPreview(qna))
    elif category == 6:
        qnas = Qna.objects.filter(
            Q(solved=False) | Q(content__icontains=text) | Q(title__icontains=text)).order_by('-created_at')
        for qna in qnas:
            data.append(buildQnaPreview(qna))
    elif category == 7:
        qnas = Qna.objects.filter(
            Q(solved=True) | Q(content__icontains=text) | Q(title__icontains=text)).order_by('-created_at')
        for qna in qnas:
            data.append(buildQnaPreview(qna))

    return Response(data=data)


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
        return_data.append(buildPostPreview(post))
    return Response(return_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getHotPostPreview(request):
    indexNum = int(request.GET['index_num'])
    startIndex = int(request.GET['start_index'])
    counts = PostCount.objects.filter(count_likes__gt=9).order_by(
        '-created_at')[startIndex:startIndex + indexNum]
    return_data = []
    for count in counts:
        post = Post.objects.get(id=count.post_id)
        return_data.append(buildPostPreview(post))
    return Response(return_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getQnaPreview(request):
    solved = True if request.GET['solved'] == 'true' else False
    indexNum = int(request.GET['index_num'])
    startIndex = int(request.GET['start_index'])

    qnas = Qna.objects.filter(solved=solved).order_by(
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
        if solved:
            answers = QnaAnswer.objects.filter(qna_id=qna.id)
            for answer in answers:
                if answer.selected_type in (1, 3):
                    selectedUserId = answer.user_id

            preview['selected_user_data'] = {
                "username": User.objects.get(uuid=selectedUserId).username,
                "activity_level": UserDetailsStatic.objects.get(user_id=selectedUserId).activity_level
            }
        return_data.append(preview)

    return Response(return_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
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

        if qna.solved:
            answers = QnaAnswer.objects.filter(qna_id=qna.id)
            for answer in answers:
                if answer.selected_type in (1, 3):
                    selectedUserId = answer.user_id

            preview['selected_user_data'] = {
                "username": User.objects.get(uuid=selectedUserId).username,
                "activity_level": UserDetailsStatic.objects.get(user_id=selectedUserId).activity_level
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

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def post(request):
    if request.method == 'GET':
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
    else:
        uuid = request.user.uuid
        data = json.loads(request.body)

        post = Post(user_id=uuid, title=data['title'],
                    content=data['content'], modified=False, type=data['type'])
        post.save()

        postCount = PostCount(
            post_id=post.id, count_likes=0, count_comments=0, count_saved=0, count_reports=0)
        postCount.save()

        userCount = UserDetailsCount.objects.get(user_id=uuid)
        userCount.count_uploaded_posts += 1
        userCount.save()

        return HttpResponse(status=200)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def postComment(request):
    uuid = request.user.uuid
    if request.method == 'GET':
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
    else:
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

        post_comment_fcm(uuid, data['post_id'], data['content'])

        return HttpResponse(status=200)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def qna(request):
    if request.method == 'GET':
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
    else:
        uuid = request.user.uuid
        data = json.loads(request.body)
        qna = Qna(user_id=uuid, title=data['title'], content=data['content'],
                  modified=False, solved=False)
        qna.save()
        qnaCount = QnaCount(qna_id=qna.id,
                            count_likes=0, count_answers=0, count_saved=0, count_comments=0, count_reports=0)
        qnaCount.save()
        userCount = UserDetailsCount.objects.get(user_id=uuid)
        userCount.count_uploaded_qnas += 1
        userCount.save()
        return HttpResponse(status=200)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def qnaAnswer(request):
    uuid = request.user.uuid
    if request.method == 'GET':
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
    else:
        data = json.loads(request.body)

        answer = QnaAnswer(user_id=uuid, qna_id=data['qna_id'],
                           content=data['content'])
        answer.save()

        qnaCount = QnaCount.objects.get(qna_id=data['qna_id'])
        qnaCount.count_answers += 1
        qnaCount.save()

        answerCount = QnaAnswerCount(
            qna_answer_id=answer.id, count_likes=0, count_comments=0, count_reports=0)
        answerCount.save()

        userCount = UserDetailsCount.objects.get(user_id=uuid)
        userCount.count_uploaded_answers += 1
        userCount.save()

        qna_answer_fcm(data['qna_id'], data['content'])

        return HttpResponse(status=200)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def qnaAnswerComment(request):
    uuid = request.user.uuid
    if request.method == 'GET':
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
    else:
        data = json.loads(request.body)

        comment = QnaAnswerComment(
            user_id=uuid, qna_answer_id=data['answer_id'], content=data['content'])
        comment.save()

        commentCount = QnaAnswerCommentCount(
            qna_answer_comment_id=comment.id, count_likes=0, count_reports=0)
        commentCount.save()

        answerCount = QnaAnswerCount.objects.get(
            qna_answer_id=data['answer_id'])
        answerCount.count_comments += 1
        answerCount.save()

        qnaAnswer = QnaAnswer.objects.get(id=data['answer_id'])
        qnaCount = QnaCount.objects.get(qna_id=qnaAnswer.qna_id)
        qnaCount.count_comments += 1
        qnaCount.save()

        qna_comment_fcm(uuid, qnaAnswer.qna_id,
                        data['answer_id'], data['content'])

        return HttpResponse(status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getQnaUserStatus(request):
    uuid = request.user.uuid
    qnaId = request.GET['qna_id']
    isSaved = UsersBookmarkedQnas.objects.filter(
        user_id=uuid, qna_id=qnaId).exists()
    resData = {
        'is_saved': isSaved
    }
    return Response(resData)


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

    post_reply_fcm(uuid, data['post_id'],
                   data['post_comment_id'], data['content'])

    return HttpResponse(status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def postQnaAnswerCommentReply(request):
    uuid = request.user.uuid
    data = json.loads(request.body)
    reply = QnaAnswerCommentReply(user_id=uuid, qna_answer_id=data['answer_id'],
                                  qna_answer_comment_id=data['qna_answer_comment_id'], content=data['content'])
    reply.save()
    replyCount = QnaAnswerCommentReplyCount(
        qna_answer_comment_reply_id=reply.id)
    replyCount.save()

    answerCount = QnaAnswerCount.objects.get(
        qna_answer_id=data['answer_id'])
    answerCount.count_comments += 1
    answerCount.save()

    qnaAnswer = QnaAnswer.objects.get(id=data['answer_id'])
    qnaCount = QnaCount.objects.get(qna_id=qnaAnswer.qna_id)
    qnaCount.count_comments += 1
    qnaCount.save()

    qna_reply_fcm(uuid, qnaCount.qna_id, answerCount.qna_answer_id,
                  data['qna_answer_comment_id'], data['content'])

    return HttpResponse(status=200)

############ 게시물 수정 #######################


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updatePost(request):
    data = json.loads(request.body)
    post = Post.objects.get(id=data['post_id'])
    post.title = data['title']
    post.content = data['content']
    post.modified = True
    post.save()

    return HttpResponse(status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateQna(request):
    data = json.loads(request.body)
    qna = Qna.objects.get(id=data['qna_id'])
    qna.title = data['title']
    qna.content = data['content']
    qna.modified = True
    qna.save()
    return HttpResponse(status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateQnaAnswer(request):
    data = json.loads(request.body)
    answer = QnaAnswer.objects.get(id=data['qna_answer_id'])
    answer.content = data['content']
    answer.save()
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
        isSaved = UsersBookmarkedPosts.objects.filter(
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
        if postCount.count_likes == 10:
            hotPost = Post.objects.get(id=postCount.post_id)
            if not hotPost.hot:
                hotPost.hot = True
                hotPost.save()
                hot_post_fcm(hotPost.user_id, hotPost.id)

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
        usersSavedPosts = UsersBookmarkedPosts(
            user_id=uuid, post_id=data['post_id'])
        postCount.save()
        usersSavedPosts.save()
    else:
        postCount.count_saved -= 1
        usersSavedPosts = UsersBookmarkedPosts.objects.get(
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
        usersSavedQnas = UsersBookmarkedQnas(
            user_id=uuid, qna_id=data['qna_id'])
        qnaCount.save()
        usersSavedQnas.save()
    else:
        qnaCount.count_saved -= 1
        usersSavedQnas = UsersBookmarkedQnas.objects.get(
            user_id=uuid, qna_id=data['qna_id'])
        qnaCount.save()
        usersSavedQnas.delete()
    return HttpResponse(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateQnaAnswerLikeCount(request):
    uuid = request.user.uuid
    data = json.loads(request.body)
    qnaAnswer = QnaAnswer.objects.get(id=data['qna_answer_id'])
    qnaAnswerCount = QnaAnswerCount.objects.get(
        qna_answer_id=data['qna_answer_id'])
    qnaCount = QnaCount.objects.get(qna_id=qnaAnswer.qna_id)

    if data['add'] == True:
        qnaAnswerCount.count_likes += 1
        qnaCount.count_likes += 1
        usersLikedQnaAnswers = UsersLikedQnaAnswers(
            user_id=uuid, qna_answer_id=data['qna_answer_id'])
        qnaAnswerCount.save()
        qnaCount.save()
        usersLikedQnaAnswers.save()

        if qnaCount.count_likes == 10:
            hotQna = Qna.objects.get(id=qnaCount.qna_id)
            if not hotQna.hot:
                hotQna.hot = True
                hotQna.save()
                hot_qna_fcm(hotQna.user_id, hotQna.id)
    else:
        qnaAnswerCount.count_likes -= 1
        qnaCount.count_likes -= 1
        usersLikedQnaAnswers = UsersLikedQnaAnswers.objects.filter(
            user_id=uuid, qna_answer_id=data['qna_answer_id'])
        qnaAnswerCount.save()
        qnaCount.save()
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
def savedPage(request):
    uuid = request.user.uuid
    userBookmarkedPosts = UsersBookmarkedPosts.objects.filter(user_id=uuid)
    posts = Post.objects.none()
    for userBookmarkedPost in userBookmarkedPosts:
        data = Post.objects.filter(id=userBookmarkedPost.post_id)
        posts = posts.union(data)
    userBookmarkedQnas = UsersBookmarkedQnas.objects.filter(user_id=uuid)
    qnas = Qna.objects.none()
    for userBookmarkedQna in userBookmarkedQnas:
        data = Qna.objects.filter(id=userBookmarkedQna.qna_id)
        qnas = qnas.union(data)
    savedPosts, savedQnas, userPosts, userCommentedPosts, userQnas, userAnsweredQnas = (
        [] for i in range(6))

    for post in posts.order_by('-created_at'):
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
        savedPosts.append(preview)

    for qna in savedQnas:
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
        savedQnas.append(preview)

    userPostObjects = Post.objects.filter(
        user_id=uuid).order_by('-created_at')[:5]

    for _post in userPostObjects:
        if len(_post.content) > 70:
            _post.content = _post.content[0:70] + "..."
        _post.created_at = timeCalculator(_post.created_at)
        preview = {
            "user_data": {
                "username": User.objects.get(uuid=_post.user_id).username,
                "activity_level": UserDetailsStatic.objects.get(user_id=_post.user_id).activity_level
            },
            "post_data": PostPreviewSerializer(_post).data,
            "count": PostCountMiniSerializer(PostCount.objects.get(post_id=_post.id)).data
        }
        userPosts.append(preview)

    userComments = PostComment.objects.filter(
        user_id=uuid).order_by('-created_at')[:5]
    for comment in userComments:
        _post = Post.objects.get(id=comment.post_id)
        if len(_post.content) > 70:
            _post.content = _post.content[0:70] + "..."
        _post.created_at = timeCalculator(_post.created_at)
        preview = {
            "user_data": {
                "username": User.objects.get(uuid=_post.user_id).username,
                "activity_level": UserDetailsStatic.objects.get(user_id=_post.user_id).activity_level
            },
            "post_data": PostPreviewSerializer(_post).data,
            "comment": comment.content,
            "count": PostCountMiniSerializer(PostCount.objects.get(post_id=_post.id)).data
        }
        userCommentedPosts.append(preview)

    userQnaObjects = Qna.objects.filter(
        user_id=uuid).order_by('-created_at')[:5]

    for _qna in userQnaObjects:
        if len(_qna.content) > 70:
            _qna.content = _qna.content[0:70] + "..."
        _qna.created_at = timeCalculator(_qna.created_at)

        preview = {
            "user_data": {
                "username": User.objects.get(uuid=_qna.user_id).username,
                "activity_level": UserDetailsStatic.objects.get(user_id=_qna.user_id).activity_level
            },

            "qna_data": QnaPreviewSerializer(_qna).data,
            "answer": QnaAnswer.objects.get(qna_id=_qna.id, selected_type__in=[1, 3]).content if _qna.solved else None,
            "count": QnaCountMiniSerializer(QnaCount.objects.get(qna_id=_qna.id)).data
        }
        if _qna.solved is True:
            answers = QnaAnswer.objects.filter(qna_id=_qna.id)
            for answer in answers:
                if answer.selected_type in (1, 3):
                    selectedUserId = answer.user_id

            preview['selected_user_data'] = {
                "username": User.objects.get(uuid=selectedUserId).username,
                "activity_level": UserDetailsStatic.objects.get(user_id=selectedUserId).activity_level
            }
        userQnas.append(preview)

    userAnswers = QnaAnswer.objects.filter(
        user_id=uuid).order_by('-created_at')[:5]
    for answer in userAnswers:
        _qna = Qna.objects.get(id=answer.qna_id)
        if len(_qna.content) > 70:
            _qna.content = _qna.content[0:70] + "..."
        _qna.created_at = timeCalculator(_qna.created_at)
        preview = {
            "user_data": {
                "username": User.objects.get(uuid=_qna.user_id).username,
                "activity_level": UserDetailsStatic.objects.get(user_id=_qna.user_id).activity_level
            },
            "qna_data": QnaPreviewSerializer(_qna).data,
            "answer": answer.content,
            "count": QnaCountMiniSerializer(QnaCount.objects.get(qna_id=_qna.id)).data,
            "answer_count": QnaAnswerCountSerializer(QnaAnswerCount.objects.get(qna_answer_id=answer.id)).data
        }
        if _qna.solved is True:
            answers = QnaAnswer.objects.filter(qna_id=_qna.id)
            for answer in answers:
                if answer.selected_type in (1, 3):
                    selectedUserId = answer.user_id

            preview['selected_user_data'] = {
                "username": User.objects.get(uuid=selectedUserId).username,
                "activity_level": UserDetailsStatic.objects.get(user_id=selectedUserId).activity_level
            }
        userAnsweredQnas.append(preview)

    data = {
        'saved_posts': savedPosts,
        'saved_qnas': savedQnas,
        'post_activity': {
            'user_posts': userPosts,
            'user_commented_posts': userCommentedPosts,
        },
        'qna_activity': {
            'user_qnas': userQnas,
            'user_answered_qnas': userAnsweredQnas,
        },
    }

    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bookmarkedPosts(request):
    uuid = request.user.uuid
    bookmarks = UsersBookmarkedPosts.objects.filter(user_id=uuid)
    data = []
    for bookmark in bookmarks:
        post = Post.objects.get(id=bookmark.post_id)
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
        data.append(preview)

    return Response(data=data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bookmarkedQnas(request):
    uuid = request.user.uuid
    bookmarks = UsersBookmarkedQnas.objects.filter(user_id=uuid)
    data = []
    for bookmark in bookmarks:
        qna = Qna.objects.get(id=bookmark.qna_id)
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
        if qna.solved is True:
            answers = QnaAnswer.objects.filter(qna_id=qna.id)
            for answer in answers:
                if answer.selected_type in (1, 3):
                    selectedUserId = answer.user_id

            preview['selected_user_data'] = {
                "username": User.objects.get(uuid=selectedUserId).username,
                "activity_level": UserDetailsStatic.objects.get(user_id=selectedUserId).activity_level
            }
        data.append(preview)

    return Response(data=data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def savedUserPosts(request):
    uuid = request.user.uuid
    userPosts = []
    userPostObjects = Post.objects.filter(
        user_id=uuid).order_by('-created_at')

    for _post in userPostObjects:
        if len(_post.content) > 70:
            _post.content = _post.content[0:70] + "..."
        _post.created_at = timeCalculator(_post.created_at)
        preview = {
            "user_data": {
                "username": User.objects.get(uuid=_post.user_id).username,
                "activity_level": UserDetailsStatic.objects.get(user_id=_post.user_id).activity_level
            },
            "post_data": PostPreviewSerializer(_post).data,
            "count": PostCountMiniSerializer(PostCount.objects.get(post_id=_post.id)).data
        }
        userPosts.append(preview)

    return Response(data=userPosts)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def savedUserCommentedPosts(request):
    uuid = request.user.uuid
    userCommentedPosts = []
    userComments = PostComment.objects.filter(
        user_id=uuid).order_by('-created_at')
    for comment in userComments:
        _post = Post.objects.get(id=comment.post_id)
        if len(_post.content) > 70:
            _post.content = _post.content[0:70] + "..."
        _post.created_at = timeCalculator(_post.created_at)
        preview = {
            "user_data": {
                "username": User.objects.get(uuid=_post.user_id).username,
                "activity_level": UserDetailsStatic.objects.get(user_id=_post.user_id).activity_level
            },
            "post_data": PostPreviewSerializer(_post).data,
            "comment": comment.content,
            "comment_count": PostCommentCountSerializer(PostCommentCount.objects.get(post_comment_id=comment.id)).data
        }
        userCommentedPosts.append(preview)

    return Response(data=userCommentedPosts)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def savedUserQnas(request):
    uuid = request.user.uuid
    userQnas = []
    userQnaObjects = Qna.objects.filter(
        user_id=uuid).order_by('-created_at')[:5]

    for _qna in userQnaObjects:
        if len(_qna.content) > 70:
            _qna.content = _qna.content[0:70] + "..."
        _qna.created_at = timeCalculator(_qna.created_at)

        preview = {
            "user_data": {
                "username": User.objects.get(uuid=_qna.user_id).username,
                "activity_level": UserDetailsStatic.objects.get(user_id=_qna.user_id).activity_level
            },
            "qna_data": QnaPreviewSerializer(_qna).data,
            "answer": QnaAnswer.objects.get(qna_id=_qna.id, selected_type__in=[1, 3]).content if _qna.solved else None,
            "count": QnaCountMiniSerializer(QnaCount.objects.get(qna_id=_qna.id)).data
        }

        if _qna.solved is True:
            answers = QnaAnswer.objects.filter(qna_id=_qna.id)
            for answer in answers:
                if answer.selected_type in (1, 3):
                    selectedUserId = answer.user_id

            preview['selected_user_data'] = {
                "username": User.objects.get(uuid=selectedUserId).username,
                "activity_level": UserDetailsStatic.objects.get(user_id=selectedUserId).activity_level
            }

        userQnas.append(preview)

    return Response(data=userQnas)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def savedUserAnsweredQnas(request):
    uuid = request.user.uuid
    userAnsweredQnas = []

    userAnswers = QnaAnswer.objects.filter(
        user_id=uuid).order_by('-created_at')

    for answer in userAnswers:
        _qna = Qna.objects.get(id=answer.qna_id)
        if len(_qna.content) > 70:
            _qna.content = _qna.content[0:70] + "..."
        _qna.created_at = timeCalculator(_qna.created_at)
        preview = {
            "user_data": {
                "username": User.objects.get(uuid=_qna.user_id).username,
                "activity_level": UserDetailsStatic.objects.get(user_id=_qna.user_id).activity_level
            },
            "qna_data": QnaPreviewSerializer(_qna).data,
            "answer": answer.content,
            "answer_count": QnaAnswerCountSerializer(QnaAnswerCount.objects.get(qna_answer_id=answer.id)).data
        }
        userAnsweredQnas.append(preview)

    return Response(data=userAnsweredQnas)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def qnaSelectAnswer(request):
    uuid = request.user.uuid
    data = json.loads(request.body)

    selectedAnswer = QnaAnswer.objects.get(id=data['qna_answer_id'])
    selectedAnswer.selected_type = 1
    selectedAnswer.save()

    qna_selected_answer_fcm(selectedAnswer.user_id, selectedAnswer.qna_id)

    maxLikes = 0
    bestAnswerId = 0

    answers = QnaAnswer.objects.filter(qna_id=selectedAnswer.qna_id)
    for answer in answers:
        answerCount = QnaAnswerCount.objects.get(qna_answer_id=answer.id)
        if answerCount.count_likes > maxLikes:
            bestAnswerId = answer.id
            maxLikes = answerCount.count_likes

    if bestAnswerId != 0:
        bestAnswer = answers.get(id=bestAnswerId)
        if bestAnswer.id == selectedAnswer.id:
            bestAnswer.selected_type = 3
        else:
            bestAnswer.selected_type = 2
        bestAnswer.save()
        qna_best_answer_fcm(bestAnswer.user_id, bestAnswer.qna_id)

    qna = Qna.objects.get(id=selectedAnswer.qna_id)
    qna.solved = True
    qna.save()

    userCount = UserDetailsCount.objects.get(user_id=selectedAnswer.user_id)
    userCount.count_accepted_answers += 1
    userCount.save()

    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deleteInstance(request):
    data = json.loads(request.body)
    category = data['category']

    if category == 'post':
        instance = Post.objects.get(
            id=data['id'])
    elif category == 'post_comment':
        instance = PostComment.objects.get(id=data['id'])
        count = PostCount.objects.get(post_id=instance.post_id)
        count.count_comments -= 1
        count.save()
    elif category == 'post_comment_reply':
        instance = PostCommentReply.objects.get(id=data['id'])
        count = PostCount.objects.get(post_id=instance.post_id)
        count.count_comments -= 1
        count.save()
    elif category == 'qna':
        instance = Qna.objects.get(id=data['id'])
    elif category == 'qna_answer':
        instance = QnaAnswer.objects.get(id=data['id'])
        count = QnaCount.objects.get(id=instance.qna_id)
        count.count_answers -= 1
        count.save()
    elif category == 'qna_answer_comment':
        instance = QnaAnswerComment.objects.get(id=data['id'])
        qnaAnswer = QnaAnswer.objects.get(id=instance.qna_answer_id)
        qnaCount = QnaCount.objects.get(qna_id=qnaAnswer.qna_id)
        qnaCount.count_comments -= 1
        qnaCount.save()
        answerCount = QnaAnswerCount.objects.get(
            qna_answer_id=instance.qna_answer_id)
        answerCount.count_comments -= 1
        answerCount.save()
    elif category == 'qna_answer_comment_reply':
        instance = QnaAnswerCommentReply.objects.get(id=data['id'])
        qnaAnswer = QnaAnswer.objects.get(id=instance.qna_answer_id)
        qnaCount = QnaCount.objects.get(qna_id=qnaAnswer.qna_id)
        qnaCount.count_comments -= 1
        qnaCount.save()
        answerCount = QnaAnswerCount.objects.get(
            qna_answer_id=instance.qna_answer_id)
        answerCount.count_comments -= 1
        answerCount.save()

    instance.delete()

    return HttpResponse(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def report(request):
    uuid = request.user.uuid
    data = json.loads(request.body)
    _id = data['id']
    category = data['category']

    if category == 'post':
        count = PostCount.objects.get(
            post_id=_id)
        instance = UsersReportedPosts(user_id=uuid, post_id=_id)
    elif category == 'post_comment':
        count = PostCommentCount.objects.get(post_comment_id=_id)
        instance = UsersReportedPostComments(user_id=uuid, post_comment_id=_id)
    elif category == 'post_comment_reply':
        count = PostCommentReplyCount.objects.get(post_comment_reply_id=_id)
        instance = UsersReportedPostCommentReplies(
            user_id=uuid, post_comment_reply_id=_id)
    elif category == 'qna':
        count = QnaCount.objects.get(qna_id=_id)
        instance = UsersReportedQnas(user_id=uuid, qna_id=_id)
    elif category == 'qna_answer':
        count = QnaAnswerCount.objects.get(qna_answer_id=_id)
        instance = UsersReportedQnaAnswers(user_id=uuid, qna_answer_id=_id)
    elif category == 'qna_answer_comment':
        count = QnaAnswerCommentCount.objects.get(qna_answer_comment_id=_id)
        instance = UsersReportedQnaAnswerComments(
            user_id=uuid, qna_answer_comment_id=_id)
    elif category == 'qna_answer_comment_reply':
        count = QnaAnswerCommentReplyCount.objects.get(
            qna_answer_comment_reply_id=_id)
        instance = UsersReportedQnaAnswerCommentReplies(
            user_id=uuid, qna_answer_comment_reply_id=_id)

    try:
        instance.save()
        count.count_reports += 1
        count.save()
        return HttpResponse(status=status.HTTP_200_OK)
    except:
        return HttpResponse(status=status.HTTP_208_ALREADY_REPORTED)
