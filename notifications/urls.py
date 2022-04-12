from django.urls import path
from .views import *

urlpatterns = [
    path('list', notificationList),
    path('read', notificationRead),
    path('delete', deleteNotification),
]
