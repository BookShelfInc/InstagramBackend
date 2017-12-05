from django.contrib import admin

from .models import User, Follows, PendingFollows

admin.site.register(User)
admin.site.register(Follows)
admin.site.register(PendingFollows)
