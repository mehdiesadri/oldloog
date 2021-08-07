from django.contrib import admin

from .models import Profile, Tag, InvitedUser, TagAssignment

admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(InvitedUser)
admin.site.register(TagAssignment)
