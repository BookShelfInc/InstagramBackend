from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from .views import getFollowers, getFollowing, followUser, unFollowUser, approveFollower,\
    makePrivate, makePublic, addAvatar, deleteAvatar

urlpatterns = [
    url(r'^followers/$', getFollowers),
    url(r'^following/$', getFollowing),
    url(r'^follow/(?P<pk>[0-9]+)/$', followUser),
    url(r'^unfollow/(?P<pk>[0-9]+)/$', unFollowUser),
    url(r'^approve/(?P<pk>[0-9]+)/$', approveFollower),
    url(r'^makeprivate/$', makePrivate),
    url(r'^makepublic/$', makePublic),
    url(r'^addavatar/$', addAvatar),
    url(r'^deleteavatar/$', deleteAvatar),
]