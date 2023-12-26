from django.contrib import admin
from .models import Post, Forum, Comment

admin.site.register(Forum)
admin.site.register(Post)

# Register your models here.
