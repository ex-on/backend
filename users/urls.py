from django.urls import path
from .views import checkAvailableEmail, checkAvailableUsername, checkUserInfo, getProfileStats, getUserInfo, registerCognitoUserInfo, cognitoUserPhysicalInfo

urlpatterns = [
    path("check_email", checkAvailableEmail),  # email
    path("check_username", checkAvailableUsername),
    path("register", registerCognitoUserInfo),
    path("physical_info", cognitoUserPhysicalInfo),
    path("check_user_info", checkUserInfo),
    path("get_user_info", getUserInfo),
    path('stats', getProfileStats),
]
