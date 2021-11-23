from django.urls import path, include

from community.views import PostCommentReplyViewSet, QnaAnswerCommentReplyViewset,  QnaAnswerViewset, getHotBoard, getMain, getQnaMain, getQnaMainSolved, getQnaMainType, getQnaMainUnsolved, postPost, postQna

urlpatterns = [
    path('getPostCommentReply', PostCommentReplyViewSet.list), #post_id
    path('postPost', postPost),
    path('getMain', getMain), #page_num
    path('getHotBoard', getHotBoard), #page_num
    path('getQnaAnswer', QnaAnswerViewset.list), #qna_id
    path('getQnaAnswerCommentReply', QnaAnswerCommentReplyViewset.list), #qna_answer_id
    path('postQna', postQna),
    path('getQnaMain', getQnaMain), #page_num
    path('getQnaMainSolved', getQnaMainSolved), #page_num
    path('getQnaMainUnsolved', getQnaMainUnsolved), #page_num
    path('getQnaMainType', getQnaMainType), #page_num & type
]