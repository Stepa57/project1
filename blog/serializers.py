from rest_framework import serializers
from .models import Comment, Post, Forum

# class ForumSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=200)
#     description = serializers.CharField()

# class ForumSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Forum
#         fields = ('id', 'title', 'description')

class CommentSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=200)
    created_date = serializers.DateTimeField()

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'created_at', 'text')

class BlogPostListSerializer(serializers.ModelSerializer):
    preview_text = serializers.SerializerMethodField()

    def get_preview_text(self, post):
        return post.get_text_preview()
    
    class Meta:
        model = Post
        fields = ('author', 'title', 'preview_text', 'created_at')

class BlogPostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ()

class BlogPostDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()

    def get_comments_count(self, obj):
        return Comment.objects.filter(post=obj)
    
    class Meta:
        model = Post
        fields = ('author', 'title', 'text', 'published_at', 'comments', 'comments_count')