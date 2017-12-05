from django.db import models
from django.conf import settings

from auth_app.models import User

class Photo(models.Model):
    photo_path = models.TextField(blank=False, null=False)
    photo_small_path = models.TextField(blank=True, null=True)
    description = models.CharField(max_length=148, blank=True, null=True)
    publish_date = models.DateTimeField(auto_now_add=True, null=False)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False, related_name='owner')

    def __str__(self):
        return self.user_id.email + " photo " + str(self.id)

class Like(models.Model):
    photo = models.ForeignKey(Photo, blank=False, null=False, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False, related_name='likes', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('photo', 'user'))

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    comment = models.CharField(max_length=256, blank=False, null=False)
    publish_date = models.DateTimeField(auto_now_add=True, null=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, related_name='comments', on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, null=False, related_name='comments', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('author', 'photo'))

    def __str__(self):
        return self.author.username + ' ' + self.comment + ' ' + str(self.id)

