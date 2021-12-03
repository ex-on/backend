from django.urls import path

from community.views import getHotBoardPreview, getPostCommentReply, getPostPreview, getQnaAnswer, getQnaAnswerCommentReply, getQnaMain, getQnaMainSolved, getQnaMainType, getQnaMainUnsolved, getUserPostQna, postPost, postPostComment, postPostCommentReply, postQna, postQnaAnswer, postQnaAnswerComment, postQnaAnswerCommentReply

urlpatterns = [
    ########게시판 메인화면###########
    path('postmain', getPostPreview), #page_num
    path('hotboardmain', getHotBoardPreview), #page_num
    path('qnamain', getQnaMain), #page_num
    path('qnamainsolved', getQnaMainSolved), #page_num
    path('qnamainunsolved', getQnaMainUnsolved), #page_num
    path('qnamaintype', getQnaMainType), #page_num & type
    path('userpost', getUserPostQna),
    ########게시물 확인###############
    path('getpost', getPostCommentReply), #post_id
    path('getqnaanswer', getQnaAnswer), #qna_id
    path('getqnaanswercommentreply', getQnaAnswerCommentReply), #qna_answer_id   
    ########게시물 작성###############
    path('post', postPost),
    path('postcomment', postPostComment),
    path('postcommentreply', postPostCommentReply),
    path('qna', postQna),
    path('qnaanswer', postQnaAnswer),
    path('qnaanswercomment', postQnaAnswerComment),
    path('qnaanswercommentreply', postQnaAnswerCommentReply),
]