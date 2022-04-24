from django.urls import path
from .views import checkAvailableEmail, checkAvailableUsername, checkPassword, checkUserInfo, fcmToken, privacyPolicy, profilePrivacy, profileStats, getUserInfo, rankCardio, rankProtein, rankWeight, registerCognitoUserInfo, cognitoUserPhysicalInfo, updateUsername

urlpatterns = [
    path("check_email", checkAvailableEmail),  # email
    path("check_username", checkAvailableUsername),
    path("update_username", updateUsername),
    path("password", checkPassword),
    path("register", registerCognitoUserInfo),
    path("physical_info", cognitoUserPhysicalInfo),
    path("check_user_info", checkUserInfo),
    path("get_user_info", getUserInfo),
    path("privacy", profilePrivacy),
    path("fcm_token", fcmToken),
    path('stats', profileStats),
    path('rank/protein', rankProtein),
    path('rank/cardio', rankCardio),
    path('rank/weight', rankWeight),
    path('policy/privacy', privacyPolicy),
]
