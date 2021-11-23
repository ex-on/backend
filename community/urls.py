from django.urls import path, include

from community.views import PostCommentReplyViewSet, QnaAnswerCommentReplyViewset,  QnaAnswerViewset, getHotBoard, getMain, getQnaMain, getQnaMainSolved, getQnaMainType, getQnaMainUnsolved, postPost, postQna

urlpatterns = [
    path('PostCommentReply', PostCommentReplyViewSet.list), #post_id
    path('Post', postPost),
    path('PostMain', getMain), #page_num
    path('HotBoard', getHotBoard), #page_num
    path('QnaAnswer', QnaAnswerViewset.list), #qna_id
    path('QnaAnswerCommentReply', QnaAnswerCommentReplyViewset.list), #qna_answer_id
    path('Qna', postQna),
    path('QnaMain', getQnaMain), #page_num
    path('QnaMainSolved', getQnaMainSolved), #page_num
    path('QnaMainUnsolved', getQnaMainUnsolved), #page_num
    path('QnaMainType', getQnaMainType), #page_num & type
]