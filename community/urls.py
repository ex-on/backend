from django.urls import path

from community.views import *

urlpatterns = [
    ########게시판 메인화면###########
    path('postmain', getPostPreview),  # page_num
    path('hotboardmain', getHotBoardPreview),  # page_num
    path('qnamain', getQnaMain),  # page_num
    path('qnamainsolved', getQnaMainSolved),  # page_num
    path('qnamainunsolved', getQnaMainUnsolved),  # page_num
    path('qnamaintype', getQnaMainType),  # page_num & type
    path('user_recent_community', getUserPostQna),
    ########게시물 확인###############
    path('getpost', getPost),  # post_id
    path('getpostcomments', getPostComments),
    path('getqna', getQna),
    path('getqnaanswer', getQnaAnswer),
    path('getqnaanswercommentreply', getQnaAnswerCommentReply),
    ########게시물 작성###############
    path('post', postPost),
    path('postcomment', postPostComment),
    path('postcommentreply', postPostCommentReply),
    path('qna', postQna),
    path('qnaanswer', postQnaAnswer),
    path('qnaanswercomment', postQnaAnswerComment),
    path('qnaanswercommentreply', postQnaAnswerCommentReply),
    ########게시물 수정###############
    path('modifypost', modifyPost),
    path('modifypostcomment', modifyPostComment),
    path('modifypostcommentreply', modifyPostCommentReply),
    path('modifyqna', modifyQna),
    path('modifyqnaanswer', modifyQnaAnswer),
    path('modifyqnaanswercomment', modifyQnaAnswerComment),
    path('modifyqnaanswercommentreply', modifyQnaAnswerCommentReply),
    ########게시물 좋아요, 저장###############
    path('get_post_count', getPostCount),
    path('update_post_count/likes', updatePostLikeCount),
    path('update_post_comment_count/likes', updatePostCommentLikeCount),
    path('update_post_comment_reply_count/likes', updatePostCommentReplyLikeCount),
    path('update_post_count/saved', updatePostSavedCount),
    path('get_post_user_status', getPostUserStatus),
    ########게시판 보관함###########
    path('get_saved_posts', getSavedPostPreview),
]
