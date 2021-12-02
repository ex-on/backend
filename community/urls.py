from django.urls import path

from community.views import QnaAnswerCommentReplyViewset,  QnaAnswerViewset, getHotBoardPreview, getPostCommentReply, getPostPreview, getQnaMain, getQnaMainSolved, getQnaMainType, getQnaMainUnsolved, postPost, postQna

urlpatterns = [
    ########게시판 메인화면###########
    path('postmain', getPostPreview), #page_num
    path('hotboardmain', getHotBoardPreview), #page_num
    path('qnamain', getQnaMain), #page_num
    path('QnaMainSolved', getQnaMainSolved), #page_num
    path('QnaMainUnsolved', getQnaMainUnsolved), #page_num
    path('QnaMainType', getQnaMainType), #page_num & type
    ########게시물 확인###############
    path('getpost', getPostCommentReply), #post_id
    path('QnaAnswer', QnaAnswerViewset.list), #qna_id
    path('QnaAnswerCommentReply', QnaAnswerCommentReplyViewset.list), #qna_answer_id   
    ########게시물 작성###############
    path('Post', postPost),
    path('Qna', postQna),
]