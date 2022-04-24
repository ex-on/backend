from django.urls import path
from .views import checkAvailableEmail, checkAvailableUsername, checkPassword, checkUserInfo, fcmToken, privacyPolicy, profilePrivacy, profileStats, getUserInfo, rankCardio, rankProtein, rankWeight, registerCognitoUserInfo, cognitoUserPhysicalInfo, updateUsername

urlpatterns = [
    path("check_email", checkAvailableEmail),  # email
    path("check_username", checkAvailableUsername),
    path("check_user_info", checkUserInfo),
    path("get_user_info", getUserInfo),
    path("register", registerCognitoUserInfo),
    path("update_username", updateUsername),
    path("password", checkPassword),
    path("physical_info", cognitoUserPhysicalInfo),
    path("fcm_token", fcmToken),
    path("privacy", profilePrivacy),
    path('stats', profileStats),
    path('rank/protein', rankProtein),
    path('rank/cardio', rankCardio),
    path('rank/weight', rankWeight),
    path('policy/privacy', privacyPolicy),
]
