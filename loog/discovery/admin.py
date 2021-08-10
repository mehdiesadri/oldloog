from django.contrib import admin

from .models import Tag, TagAssignment

admin.site.register(Tag)
admin.site.register(TagAssignment)
