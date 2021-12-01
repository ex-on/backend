from django.shortcuts import render
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
