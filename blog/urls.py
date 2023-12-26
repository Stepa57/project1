from django.urls import include, path
from . import views
from rest_framework import routers

from core.views import CommentViewSet, BlogPostViewSet

router = routers.DefaultRouter()
router.register(r'comments', CommentViewSet)
router.register(r'posts', BlogPostViewSet)

urlpatterns = [
    path('API', include(router.urls)),
    path('', views.forum_list, name='forum_list'),
    path('forum/<int:forum_id>/posts', views.post_list, name='post_list'),
    path('forum/<int:forum_id>/all_posts', views.all_posts, name='all_posts'),
    path('forum/<int:forum_id>/posts/post/<int:post_id>', views.post, name='post'),
    path('forum/<int:forum_id>/posts/post/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('forum/<int:forum_id>/posts/post/<int:post_id>/publish/', views.post_publish, name='post_publish'),
    path('forum/<int:forum_id>/posts/post/<int:post_id>/comment/<int:comment_id>/comment_edit/', views.comment_edit, name='comment_edit'),
    path('forum/<int:forum_id>/posts/post/<int:post_id>/comment_add/', views.comment_edit, name='comment_add'),
    path('forum/<int:forum_id>/posts/add', views.post_edit, name='post_add'),
]