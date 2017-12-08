from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from .views import getUserNotifications

urlpatterns = [
    url(r'^my/(?P<pk>[0-9]+)/$', getUserNotifications),
]