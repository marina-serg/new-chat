from django.contrib import admin

from .models import Message, Group

admin.site.register(Message)
admin.site.register(Group)
