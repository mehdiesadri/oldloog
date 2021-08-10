from django.contrib import admin

# Register your models here.
from .models import Profile, InvitedUser

admin.site.register(Profile)
admin.site.register(InvitedUser)
