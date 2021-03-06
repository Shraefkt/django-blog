from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.

class Profile(models.Model):
    followers = models.ManyToManyField(User, related_name='user_followers')
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")
    bio = models.TextField()
    following = models.ManyToManyField(User, related_name='user_following')

    def __str__(self):
        return f"{self.user.username}'s Profile"
    def save(self,*args,**kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

