from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import JSONParser
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from auth_app.models import User, Follows, PendingFollows
from auth_app.serializers import FollowsSerializer, UserSerializer

from photo_app.models import Photo

from AWS.env_variables import getVariable
from AWS.api_gateway import cropImage
from AWS.aws_s3 import uploadImageUser

# @api_view(['POST'])
# @authentication_classes([JSONWebTokenAuthentication, ])
# @permission_classes([IsAuthenticated, ])
# def addAvatar(request, pk):
#     if (request.method == 'POST'):
#         user = request.user
#         try:
#             photo = Photo.objects.get(pk=pk)
#             user.photo = photo
#             user.save()
#
#             imageName = photo.photo_path.replace(getVariable('s3BucketPath'), '')
#             photo.photo_small_path = getVariable('s3BucketPath') + cropImage(imageName)[1:-1]
#             photo.save()
#
#             return HttpResponse(status=200)
#         except Photo.DoesNotExist:
#             return HttpResponse(status=404)
#     return HttpResponse(status=400)

@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def addAvatar(request):
    if(request.method == 'POST'):
        if('image' in request.FILES):
            photo_path_ = uploadImageUser(request.user.username, request.FILES['image'])
            imageName = photo_path_.replace(getVariable('s3BucketPath'), '')
            photo_small_path_ = getVariable('s3BucketPath') + cropImage(imageName)[1:-1]

            photo = Photo(user_id=request.user, photo_path=photo_path_, photo_small_path=photo_small_path_)
            photo.save()

            user = request.user
            user.photo = photo
            user.save()

            return HttpResponse(status=200)
        else:
            return HttpResponse(status=404)
    return HttpResponse(status=400)

@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def deleteAvatar(request):
    if (request.method == 'POST'):
        user = request.user
        user.photo = None
        user.save()
        return HttpResponse(status=200)
    return HttpResponse(status=400)

@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def makePrivate(request):
    if (request.method == 'POST'):
        user = request.user
        user.private_account = True
        user.save()
        return HttpResponse(status=200)
    return HttpResponse(status=400)

@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def makePublic(request):
    if (request.method == 'POST'):
        user = request.user
        user.private_account = False
        user.save()
        return HttpResponse(status=200)
    return HttpResponse(status=400)

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def getFollowers(request):
    if(request.method == 'GET'):
        user = request.user
        followers = [i.target_user for i in user.followed_by.all()]
        serialized = UserSerializer(followers, many=True)
        return JsonResponse(serialized.data, status=status.HTTP_200_OK, safe=False)
    return HttpResponse(status=400)


@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def getFollowing(request):
    if(request.method == 'GET'):
        user = request.user
        following = Follows.get_following(user.profile)
        serialized = UserSerializer(following, many=True)
        return JsonResponse(serialized.data, status=status.HTTP_200_OK, safe=False)
    return HttpResponse(status=400)

@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def followUser(request, pk):
    if(request.method == 'POST'):
        user = request.user
        try:
            addUser = User.objects.get(id=pk)
            if(addUser.private_account == True):
                pendingFollowsInstance = PendingFollows(target_user=user, follow_user=addUser)
                pendingFollowsInstance.save()
            else:
                user.profile.following.add(addUser)
        except:
            return HttpResponse(status=400)
        return HttpResponse(status=200)
    return HttpResponse(status=400)

@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def unFollowUser(request, pk):
    if (request.method == 'POST'):
        user = request.user
        try:
            addUser = User.objects.get(id=pk)
            user.profile.following.remove(addUser)
        except:
            print('error')
            return HttpResponse(status=400)
        return HttpResponse(status=200)
    return HttpResponse(status=400)

@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def approveFollower(request, pk):
    if (request.method == 'POST'):
        user = request.user
        try:
            addUser = User.objects.get(id=pk)
            pendingFollowInstance = PendingFollows.objects.filter(target_user=addUser, follow_user=user)
            pendingFollowInstance.delete()
            addUser.profile.following.add(user)
        except:
            print('error')
            return HttpResponse(status=400)
        return HttpResponse(status=200)
    return HttpResponse(status=400)

