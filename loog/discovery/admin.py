from django.contrib import admin

from .models import Profile, Tag, InvitedUsers

admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(InvitedUsers)
