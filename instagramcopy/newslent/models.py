from django.db import models
from django.utils import timezone
from user.models import User

# Create your models here.
class News(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор поста')
    title = models.CharField(max_length=20, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Контент")
    publication_date = models.DateTimeField(default=timezone.now, verbose_name="Время публикаций")
    edited = models.BooleanField(default=False, verbose_name="Редактирован")

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return f'{self.title} : {self.publication_date}'
    
class PostAttachment(models.Model):
    name = models.CharField(
        max_length=100, 
        verbose_name='Название картинки', 
        blank=True, 
        null=True
    )
    image = models.ImageField(
        upload_to='posts/images/', 
        verbose_name='Картинка'
    )
    post = models.ForeignKey(
        News, 
        on_delete=models.CASCADE, 
        related_name='attachments',
        verbose_name='Пост'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def save(self, *args, **kwargs):
        self.name = self.image.name.split(".")[0].capitalize()
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = "Приложение к посту"
        verbose_name_plural = "Приложения к постам"
        ordering = ['-created_at']

    def __str__(self):
        return self.name if self.name else f"Приложение {self.id}"
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('News', on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.email} лайкнул {self.post.title}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('News', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email}: {self.text[:30]}"