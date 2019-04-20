from django.contrib import admin

# Register your models here.
from chatroom.models import Chatroom, Chatmsg

admin.site.register(Chatroom)
admin.site.register(Chatmsg)