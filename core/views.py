from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from blog.models import Forum, Post, Comment
from blog.serializers import CommentSerializer, BlogPostListSerializer, BlogPostDetailSerializer, BlogPostCreateUpdateSerializer


class ActionSerializedViewSet(viewsets.ModelViewSet):
    action_serializers = {}
    
    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
            
        return self.serializer_class
    
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

class BlogPostViewSet(ActionSerializedViewSet):
    serializer_class = BlogPostListSerializer
    queryset = Post.objects.all()

    action_serializers = {
        'list': BlogPostListSerializer,
        'retrieve': BlogPostDetailSerializer,
        'create': BlogPostCreateUpdateSerializer,
        'update': BlogPostCreateUpdateSerializer,
    }

    @action(detail=True,
            methods=['post'],
            permission_classes=[IsAuthenticated])
    def publish(self, request, pk=None):
        post = self.get_object()
        if request.user == post.author:
            return Response({'message':'blog post was published'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You do not have permissions'},
                             status=status.HTTP_403_FORBIDDEN)
        
    @action(detail=False)
    def published_posts(self, request):
        published_posts = Post.published.all()

        page = self.paginate_queryset(published_posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(published_posts, many=True)
        return Response(serializer.data)
    
    def get_queryset(self):
        queryset = self.queryset
        author = self.request.query_params.get('author', None)
        if author:
            queryset = queryset.filter(author__username=author)
        return queryset
    
    # yfffd