from django.db import models
from django.db.models import Manager, QuerySet
from django.utils import timezone

class PostPublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            published_at__lte=timezone.now())

class PostQuerryset(QuerySet):
    def for_user(self, user=None):
        if user.is_staff:
            return self.all()
        elif user.is_authenticated:
            return self.filter(
                Q(published_at__lte=timezone.now() | Q(author=user)))
        else:
            return self.filter(published_at__lte=timezone.now())
        
class PostManager(Manager):
    def get_queryset(self):
        return PostQuerryset(self.model, using=self._db)
    
    def for_user(self, user=None):
        return self.get_queryset().for_user(user=user)