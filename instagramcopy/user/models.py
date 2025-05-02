from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
# models.py
class User(AbstractUser):
    first_name = models.CharField(max_length=50, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=50, blank=True, verbose_name='Фамилия')
    email = models.EmailField(unique=True, verbose_name='Почта')
    phone = models.CharField(blank=True, max_length=15, verbose_name='Номер телефона')
    password = models.CharField(max_length=128, verbose_name='Пароль')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватарка')
    bio = models.TextField(blank=True, null=True, verbose_name='О себе')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.email}'

class Follow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='following_set'  
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followers_set'  
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')  

    def __str__(self):
        return f"{self.follower} подписан на {self.following}"
    