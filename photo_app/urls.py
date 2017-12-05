from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from .views import getImages, uploadImage, getFeed, getImagesByUser, getInteresting, \
createComment, deleteComment, likePhoto

urlpatterns = [
    url(r'^my/$', getImages),
    url(r'^feed/$', getFeed),
    url(r'^userphotos/(?P<pk>[0-9]+)/$', getImagesByUser),
    url(r'^uploadimage/$', uploadImage),
    url(r'^interesting/$', getInteresting),

    url(r'^createcomment/$', createComment),
    url(r'^deletecomment/(?P<pk>[0-9]+)/$', deleteComment),
    url(r'^like/(?P<pk>[0-9]+)/$', likePhoto),
]