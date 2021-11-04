from django.urls import path, include

from community.views import getMain, getPost

urlpatterns = [
    path('main', getMain), #page_num
    path('getPost', getPost), #post_id
    path('getHotBoard'),
]