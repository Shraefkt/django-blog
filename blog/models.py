from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from PIL import Image
# Create your models here.
class Post(models.Model):
    cover_image = models.ImageField(default="default_post_cover.jpg", upload_to="post_images/")
    title = models.CharField(max_length=100,default="")
    tagline = models.CharField(max_length=300, default="")
    content = models.TextField()
    notes = models.CharField(max_length=1000,default="")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default = timezone.now,editable=False)
    is_published = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name='blogpost_like',editable=False)
    tags = TaggableManager()
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail',kwargs= {"pk" : self.pk})

    def number_of_likes(self):
        return self.likes.count()

    def number_of_comments(self):
        return Comment.objects.filter(blogpost_connected=self).count()
    def reading_time(self):
        return round(len(self.content) / 1500)

class Comment(models.Model):
    blogpost_connected = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.author) + ', ' + self.blogpost_connected.title[:40]

