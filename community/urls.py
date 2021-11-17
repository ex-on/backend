from django.urls import path, include

from community.views import getHotBoard, getMain, getPost, getQna, getQnaMain, getQnaMainSolved, getQnaMainType

urlpatterns = [
    path('getMain', getMain), #page_num
    path('getPost', getPost), #post_id
    path('getHotBoard', getHotBoard), #page_num
    path('getQnaMain', getQnaMain), #page_num
    path('getQnaMainSolved', getQnaMainSolved), #page_num
    path('getQnaMainType', getQnaMainType), #type
    path('getQna', getQna), #qna_id
]