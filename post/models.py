from django.conf import settings
from django.db import models


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts", null=True,
                               blank=True)
    title = models.CharField(max_length=255, default='')
    content = models.TextField(default='')

    def __str__(self):
        return '{} : {}'.format(self.author.username, self.title)
