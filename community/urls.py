from django.urls import path

from community.views import *

urlpatterns = [
    ########게시판 메인화면###########
    path('post_list', getPostPreview),  # page_num
    path('post_list/hot', getHotPostPreview),  # page_num
    path('qna_list', getQnaPreview),  # page_num
    path('qna_list/hot', getHotQnaPreview),
    path('qnamainsolved', getQnaMainSolved),  # page_num
    path('qnamainunsolved', getQnaMainUnsolved),  # page_num
    path('qnamaintype', getQnaMainType),  # page_num & type
    path('user_recent_community', getUserRecentPostQna),
    ########게시물 확인###############
    path('getpost', getPost),  # post_id
    path('getpostcomments', getPostComments),
    path('getQna', getQna),
    path('getQnaAnswers', getQnaAnswers),
    path('get_qna_answer_comments', getQnaAnswerComments),
    ########게시물 작성###############
    path('post', postPost),
    path('postcomment', postPostComment),
    path('postcommentreply', postPostCommentReply),
    path('qna', postQna),
    path('qnaanswer', postQnaAnswer),
    path('qna_answer_comment', postQnaAnswerComment),
    path('qna_answer_comment_reply', postQnaAnswerCommentReply),
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
    path('update_post_comment_reply_count/likes',
         updatePostCommentReplyLikeCount),
    path('update_post_count/saved', updatePostSavedCount),
    path('get_post_user_status', getPostUserStatus),
    path('update_qna_count/saved', updateQnaSavedCount),
    path('get_qna_count', getQnaCount),
    path('get_qna_user_status', getQnaUserStatus),
    path('update_qna_count/saved', updateQnaSavedCount),
    path('update_qna_answer_count/likes', updateQnaAnswerLikeCount),
    path('update_qna_answer_comment_count/likes', updateQnaAnswerCommentLikeCount),
    ########게시판 보관함###########
    path('saved', getSavedPostQnaPreview),
    ########게시물 신고#######################
    path('update_report_post', updateUserReportedPosts),
    path('update_report_post_comment', updateUserReportedPostComments),
    path('update_report_post_comment_reply',
         updateUserReportedPostCommentReplies),
    path('update_report_qna', updateUserReportedQnas),
    path('update_report_qna_answer', updateUserReportedQnaAnswers),
    path('update_report_qna_answer_comment',
         updateUserReportedQnaAnswerComments),
    path('update_report_qna_answer_comment_reply',
         updateUserReportedQnaAnswerCommentReplies),
    ########게시물 삭제#######################
    path('delete_post', deletePost),
    path('delete_post_comment', deletePostComment),
    path('delete_post_comment_reply', deletePostCommentReply),
    path('delete_qna', deleteQna),
    path('delete_qna_answer', deleteQnaAnswer),
    path('delete_qna_answer_comment', deleteQnaAnswerComment),
    path('delete_qna_answer_comment_reply', deleteQnaAnswerCommentReply),
]
