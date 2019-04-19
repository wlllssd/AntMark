from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from simditor.fields import RichTextField

# Create your models here.

class UserInfo(models.Model):
    GENDER_CHOICES = (
        (u'M', u'Male'),
        (u'F', u'Female'),
    )
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name="user")
    nickname = models.CharField(max_length=20, default="None")
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default="Male")
    intro = models.CharField(max_length=200, default="None")
    phone = models.CharField(max_length=15, default="0")
    wechat = models.CharField(max_length=30, default="None")
    qq = models.CharField(max_length=16, default="0")
    profile = ProcessedImageField(upload_to='user/img', default='user/img/default.jpg', 
        processors=[ResizeToFill(500, 500)],  format='JPEG', options={'quality': 60})
    
    def __str__(self):
        return self.nickname + " " + self.user