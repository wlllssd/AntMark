from django.db import models

# Create your models here.
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
    profile = ProcessedImageField(upload_to='user/img', default='user/img/default.jpg', 
        processors=[ResizeToFill(500, 500)],  format='JPEG', options={'quality': 60})
    
    def __str__(self):
        return self.nickname + " " + self.user

class Chatroom(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    # commodity = models.ForeignKey(Commodity, on_delete=models.SET_NULL)
    talker1 = models.ForeignKey(User, related_name="talker1", on_delete=models.CASCADE)
    talker2 = models.ForeignKey(User, related_name="talker2", on_delete=models.CASCADE)

    def __str__(self):
        return "This is a chatroom between " + str(self.talker1) + " and " + str(self.talker2)

class Message(models.Model):
    belong_to = models.ForeignKey(Chatroom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = MarkdownxField(max_length=2000)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
