from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from .views import register, getInfo, getAllUsers, getUserPage

urlpatterns = [
    url(r'^register/', register),
    url(r'^login/', obtain_jwt_token),
    url(r'^info/$', getInfo),
    url(r'^allUsers/$', getAllUsers),
    url(r'^user/(?P<pk>[0-9]+)/$', getUserPage),
]