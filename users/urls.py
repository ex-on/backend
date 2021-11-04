from django.urls import path
from .views import checkAvailableEmail

urlpatterns = [
    path("check_email", checkAvailableEmail),  # email
]
