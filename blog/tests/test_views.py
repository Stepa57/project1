from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
import json

from blog.models import Post, Forum
from blog.serializers import BlogPostListSerializer, BlogPostDetailSerializer

User = get_user_model()
client = Client()

class GetAllPostsTest(TestCase):
    def setUp(self):
        author = User.objects.create(username='author')
        forum = Forum.objects.create(title='Another Forum',
                                     description='description')
        Post.objects.create(title='First post',
                            text='text',
                            forum=forum,
                            author=author)
        Post.objects.create(title='Second post',
                            text='text',
                            forum=forum,
                            author=author)
        Post.objects.create(title='Third post',
                            text='text',
                            forum=forum,
                            author=author)
    
    def test_get_all_posts(self):
        response = client.get(reverse('post-list'))
        posts = Post.objects.all()
        serializer = BlogPostListSerializer(posts, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetSinglePostTest(TestCase):
    def setUp(self):
        author = User.objects.create(username='author')
        forum = Forum.objects.create(title='Another Forum',
                                     description='description')
        self.post = Post.objects.create(title='First post',
                                        text='text',
                                        forum=forum,
                                        author=author)
    
    def test_get_valid_single_post(self):
        response = client.get(reverse('post-detail', kwargs={'pk':self.post.pk}))
        post = Post.objects.get(pk=self.post.pk)
        serializer = BlogPostDetailSerializer(post)
        self.assertEqual(str(response.data), str(serializer.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_post(self):
        response = client.get(reverse('post-detail', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class CreateNewPostTest(TestCase):
    def setUp(self):
        self.author = User.objects.create(username='test')
        forum = Forum.objects.create(title='Another Forum',
                                     description='description')
        self.valid_payload = {
            'title': 'First post',
            'text': 'text',
            'author': 1,
            'forum': forum.toJSON(),
        }
        self.invalid_payload = {
            'title': 'First post',
            'author': 2,
            'forum': forum.toJSON(),
        }

    def test_create_valid_single_post(self):
        response = client.post(reverse('post-list'),
                               data=json.dumps(self.valid_payload),
                               content_type='application/json')
        print(reverse('post-list'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_invalid_single_post(self):
        response = client.post(reverse('post-list'),
                               data=json.dumps(self.invalid_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UpdateSinglePostTest(TestCase):
    def setUp(self):
        self.author = User.objects.create(username='username')
        forum = Forum.objects.create(title='Another Forum',
                                     description='description')
        self.post = Post.objects.create(title='First post',
                                        text='text',
                                        forum=forum,
                                        author=self.author)
        self.valid_payload = {
            'title': 'First post',
            'text': 'text text text',
            'author': 1,
            'forum': forum.toJSON(),
        }
        self.invalid_payload = {
            'title': 'First post',
            'text': None,
            'author': 2,
            'forum': forum.toJSON(),
        }

    def test_valid_update_post(self):
        response = client.put(reverse('post-detail',
                                      kwargs={'pk':self.post.pk}),
                                      data=json.dumps(self.valid_payload),
                                      content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_post(self):
        response = client.put(reverse('post-detail',
                                      kwargs={'pk':self.post.pk}),
                                      data=json.dumps(self.invalid_payload),
                                      content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)