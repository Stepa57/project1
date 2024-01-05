from django import forms
from .models import Post, Comment, Forum

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'forum', 'is_published')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ('title','description')