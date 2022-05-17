from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.shortcuts import render

@api_view(['GET'])
@permission_classes([])
def linkPage(request):
  return render(request, 'link_page.html')

