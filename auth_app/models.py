from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import PermissionsMixin, AbstractUser, User

from photo_app.models import Photo

class User(AbstractUser):
    email = models.EmailField(blank=False, null=False, unique=True)
    password = models.CharField(max_length=256, blank=False, null=False)
    bio = models.CharField(max_length=320, blank=True, null=True)
    photo = models.ForeignKey(Photo, blank=True, null=True, related_name='user_photo')
    private_account = models.BooleanField(default=False)

    def __str__(self):
        return self.username + ' ' + self.email + ' ' + str(self.private_account) + ' ' + str(self.id)

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        if(not Follows.objects.filter(target_user=self).count()):
            followsInstance = Follows(target_user=self)
            followsInstance.save()

class Follows(models.Model):
    target_user = models.OneToOneField(User, related_name='profile')
    following = models.ManyToManyField(User, blank=True, related_name='followed_by')
    
    def __str__(self):
        return self.target_user.username + ' ' + str(self.following.count())

    def get_following(self):
        users = self.following.all()  # User.objects.all().exclude(username=self.user.username)
        return users.exclude(username=self.target_user.username)

class PendingFollows(models.Model):
    target_user = models.ForeignKey(User, null=False, blank=False, related_name='pending_account')
    follow_user = models.ForeignKey(User, null=False, blank=False, related_name='pending_follow_account')

    def __str__(self):
        return self.target_user.username + ' ' + self.follow_user.username

    class Meta:
        unique_together = (('target_user', 'follow_user'))