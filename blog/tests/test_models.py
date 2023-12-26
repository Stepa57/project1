from django.contrib.auth import get_user_model
from django.test import TestCase

from blog.models import Post, Forum

User = get_user_model()

class PostTest(TestCase):
    def setUp(self):
        author_1 = User.objects.create(username='author #1')
        author_2 = User.objects.create(username='author #2')
        forum = Forum.objects.create(title='Another Forum',
                                     description='description')
        Post.objects.create(title='First post',
                            text='text',
                            forum=forum,
                            author=author_1)
        Post.objects.create(title='Second post',
                            text='text',
                            forum=forum,
                            author=author_2)
    def test_publish_method_for_post(self):
        post = Post.objects.get(title='First post')
        post.publish()
        self.assertEqual(post.is_published, True)

    def test_published_post_filtering(self):
        post = Post.objects.get(title='First post')
        post.publish()
        posts = Post.published.all()
        self.assertEqual(posts.count(), 1)