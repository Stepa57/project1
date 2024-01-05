from django.db import models
from django.conf import settings
from django.utils import timezone
from .managers import PostPublishedManager, PostManager
from django.template.defaultfilters import truncatewords
import json

class Forum(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=False)
    description = models.TextField()
    objects = models.Manager()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    
    def __str__(self):
        return self.title

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    published_at = models.DateTimeField(blank=True, null=True, verbose_name="Дата публикации")
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    published = PostPublishedManager()
    objects = PostManager()
    is_published = models.BooleanField(default=False, verbose_name="Запись опубликована?")

    def get_text_preview(self):
        return truncatewords(self.text, 10)

    def is_publish(self):
        return True if self.published_at else False

    def publish(self):
        self.published_at = timezone.now()
        self.is_published = True
        self.save()

    class Meta:
        verbose_name = 'Запись в блоге'
        verbose_name_plural = 'Записи в блоге'
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete =models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
    objects = models.Manager()
