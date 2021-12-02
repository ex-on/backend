from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import *
import json

# Create your views here.
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def checkAvailableEmail(request):
    email = request.GET['email']
    isEmailAvailable = not User.objects.filter(email=email).exists()
    return Response(isEmailAvailable)

@api_view(['POST'])
def registerCognitoUser(request):
    email = request.POST['email']
    uuid = request.POST['sub']
    username = request.POST['username']
    phone_number = request.POST['phone_number']
    userData = User(email=email, uuid=uuid, username=username, phone_number=phone_number)
    userData.save()
    return HttpResponse(status = status.HTTP_201_CREATED)