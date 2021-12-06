from django.urls import path
from .views import checkAvailableEmail, registerCognitoUserInfo

urlpatterns = [
    path("check_email", checkAvailableEmail),  # email
    path("register", registerCognitoUserInfo),
]
