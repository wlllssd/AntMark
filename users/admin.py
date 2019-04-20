from django.contrib import admin

# Register your models here.
from users.models import UserInfo

admin.site.register(UserInfo)