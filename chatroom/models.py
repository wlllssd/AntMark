from django.db import models 
from django.contrib.auth.models import User

from commodity.models import Commodity
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class Chatroom(models.Model):
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    member1 = models.ForeignKey(User, related_name="mem1", on_delete=models.CASCADE)
    member2 = models.ForeignKey(User, related_name="mem2", on_delete=models.CASCADE)
    date_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Chatroom " + str(self.member1) + " - " + str(self.member2)


class Chatmsg(models.Model):
    room = models.ForeignKey(Chatroom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=2000)
    timestamp = models.DateTimeField(auto_now_add=True)
    image = ProcessedImageField(upload_to='chatroom/img', default=None,
        format='JPEG', options={'quality': 60})
    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return self.content