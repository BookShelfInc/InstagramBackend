import itertools
from operator import itemgetter
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from AWS.dynamoDB import getNotifications

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def getUserNotifications(request, pk):
    if(request.method == 'GET'):
        res = getNotifications(userId=pk)
        print(res)
        return Response(res, status=status.HTTP_200_OK)
    return HttpResponse(status=400)


