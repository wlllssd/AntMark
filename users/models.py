from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

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
    is_verified = models.BooleanField(default=False)
    stuCardPhoto = ProcessedImageField(upload_to='user/img/verify', null=True, format='JPEG')
    
    def __str__(self):
        return self.nickname + " " + str(self.user)


class Message(models.Model):
    TYPE_CHOICES = (
        (u'M', u'massage'),
        (u'S', u'stu_verify'),
        (u'C', u'commodity_verify'),
    )
    sender = models.ForeignKey(User, related_name="sender_msg", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="receiver_msg", on_delete=models.CASCADE)
    msg_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="message")
    text = models.CharField(max_length=2000)
    id_content = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    sender_del = models.BooleanField(default=False)
    receiver_del = models.BooleanField(default=False)
    
    def __str__(self):
        return self.text