from django.urls import path

from community.views import *

urlpatterns = [
    path('search', search),
    path('post_list', getPostPreview),  # page_num
    path('post_list/hot', getHotPostPreview),  # page_num
    path('post', post),
    path('post_count', getPostCount),
    path('post_user_status', getPostUserStatus),
    path('post_comment', postComment),
    path('post_comment_reply', postPostCommentReply),
    path('post/update', updatePost),
    path('post_count/update_likes', updatePostLikeCount),
    path('post_count/update_saved', updatePostSavedCount),
    path('post_comment_count/update_likes', updatePostCommentLikeCount),
    path('post_comment_reply_count/update_likes', updatePostCommentReplyLikeCount),

    path('qna_list', getQnaPreview),  # page_num
    path('qna_list/hot', getHotQnaPreview),
    path('qna', qna),
    path('qna_count', getQnaCount),
    path('qna_user_status', getQnaUserStatus),
    path('qna_answer', qnaAnswer),
    path('qna_answer_comment', qnaAnswerComment),
    path('qna_answer_comment_reply', postQnaAnswerCommentReply),
    path('qna/update', updateQna),
    path('qna_answer/update', updateQnaAnswer),
    path('qna_count/update_saved', updateQnaSavedCount),
    path('qna_answer_count/update_likes', updateQnaAnswerLikeCount),
    path('qna_answer_comment_count/update_likes',
         updateQnaAnswerCommentLikeCount),
    path('qna_select_answer', qnaSelectAnswer),

    path('user_recent_community', getUserRecentPostQna),
    path('saved', savedPage),
    path('saved/bookmarks/posts', bookmarkedPosts),
    path('saved/bookmarks/qnas', bookmarkedQnas),
    path('saved/user_posts', savedUserPosts),
    path('saved/user_commented_posts', savedUserCommentedPosts),
    path('saved/user_qnas', savedUserQnas),
    path('saved/user_answered_qnas', savedUserAnsweredQnas),
    path('delete', deleteInstance),
    path('report', report),
]
