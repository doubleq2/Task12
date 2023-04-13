from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.CharField(max_length=250)
    link = models.CharField(max_length=10)
    sub_count = models.IntegerField(default=0)

class Subscriptions(models.Model):
    user_id = models.ForeignKey(User, related_name="following",on_delete=models.CASCADE, verbose_name='Подписчик')
    following_user_id = models.ForeignKey(User, related_name="followers",on_delete=models.CASCADE, verbose_name='Подписан')
    
class Photo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    like_count = models.IntegerField(default=0)
    time_creation = models.CharField(max_length=30,default=0)
    
    def __str__(self):
        return self.title
     
class Likes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo,on_delete=models.CASCADE)