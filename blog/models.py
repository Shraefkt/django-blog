from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    likes = models.ManyToManyField(User, related_name='blogpost_like')
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail',kwargs= {"pk" : self.pk})

    def number_of_likes(self):
        return self.likes.count()

    def number_of_comments(self):
        return Comment.objects.filter(blogpost_connected=self).count()
class Comment(models.Model):
    blogpost_connected = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.author) + ', ' + self.blogpost_connected.title[:40]