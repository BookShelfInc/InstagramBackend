import itertools
from operator import itemgetter
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from auth_app.models import Follows
from .models import Photo, Comment, Like
from .serializers import PhotoSerializer, CommentCreateSerializer

from AWS.aws_s3 import uploadImageUser
from AWS.dynamoDB import postComment

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def getImages(request):
    if(request.method == 'GET'):
        user = request.user
        allImages = Photo.objects.filter(user_id=user)
        serialized = PhotoSerializer(allImages, many=True)
        return JsonResponse(serialized.data, status=status.HTTP_200_OK, safe=False)
    return HttpResponse(status=400)

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def getImagesByUser(request, pk):
    if(request.method == 'GET'):
        allImages = Photo.objects.filter(user_id_id=pk)
        serialized = PhotoSerializer(allImages, many=True)
        return JsonResponse(serialized.data, status=status.HTTP_200_OK, safe=False)
    return HttpResponse(status=400)

@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def uploadImage(request):
    if(request.method == 'POST'):
        if('image' in request.FILES):
            photo_path_ = uploadImageUser(request.user.username, request.FILES['image'])

            photo = Photo(user_id=request.user, photo_path=photo_path_)
            photo.save()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=404)
    return HttpResponse(status=400)

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def getFeed(request):
    if(request.method == 'GET'):
        user = request.user
        photos = []
        following = Follows.get_following(user.profile)
        for i in following:
            a = Photo.objects.filter(user_id=i)
            photos = itertools.chain(photos, a)
        res = []
        for i in photos:
            res.append(i)
        res.sort(key=lambda x: x.publish_date, reverse=True)
        serialized = PhotoSerializer(res, many=True)
        return JsonResponse(serialized.data, status=status.HTTP_200_OK, safe=False)
    return HttpResponse(status=400)

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def getInteresting(request):
    if(request.method == 'GET'):
        photos = Photo.objects.all()
        images = {}
        res = []
        for i in photos:
            images[i] = i.likes.count()
        for i in images.keys():
            res.append((images[i], i))
        res.sort(key=itemgetter(0), reverse=True)
        res = [i[1] for i in res]
        serialized = PhotoSerializer(res, many=True)
        return JsonResponse(serialized.data, status=status.HTTP_200_OK, safe=False)
    return HttpResponse(status=400)


@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def createComment(request):
    if(request.method == 'POST'):
        data = JSONParser().parse(request)
        data['author'] = request.user.id
        serialized = CommentCreateSerializer(data=data)
        if(serialized.is_valid()):
            serialized.save()

            author_id = serialized.data['author']
            photo_id = serialized.data['photo']
            commentt = Comment.objects.filter(author_id=author_id, photo_id=photo_id)[0]

            photoObj = Photo.objects.get(pk=photo_id)
            postComment(commentt.id, commentt.comment, author_id, photo_id, photoObj.user_id.id)

            return JsonResponse(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    return HttpResponse(status=400)

@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def deleteComment(request, pk):
    if(request.method == 'POST'):
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return HttpResponse(status=200)
    return HttpResponse(status=400)

@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def likePhoto(request, pk):
    if(request.method == 'POST'):
        user = request.user
        if(Like.objects.filter(user=user, photo_id=pk).count()):
            Like.objects.filter(user=user, photo_id=pk).delete()
        else:
            like = Like(user=user, photo_id=pk)
            like.save()
        return HttpResponse(status=200)
    return HttpResponse(status=400)
