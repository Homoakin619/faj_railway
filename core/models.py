from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField

class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    title = models.CharField(max_length=100,null=True)
    content = RichTextField()
    image = models.ImageField(null=True,blank=True)
    video_link = models.CharField(max_length=250,blank=True,null=True)

    def __str__(self):
        return self.title
