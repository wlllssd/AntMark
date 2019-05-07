from django.db import models

# Create your models here.
class Announcement(models.Model):
    title = models.CharField(max_length=200, blank = False, default = None)
    text = models.CharField(max_length=20000)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-timestamp', )
    def __str__(self):
        return self.text