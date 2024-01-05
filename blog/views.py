from django.shortcuts import render, redirect
from django.http import Http404
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Forum, Post, Comment
from .forms import PostForm, CommentForm, ForumForm

def forum_list(request):
    forums = Forum.objects.all()
    return render(request, 'blog/forum_list.html', {'forums': forums})

def post_list(request, forum_id):
    try:
        forum = Forum.objects.get(id=forum_id)
    except Forum.DoesNotExist:
        raise Http404('Форум не найден')
    posts = Post.published.all().order_by('published_at')
    return render(request, 'blog/post_list.html', {'posts': posts, 'forum_id': forum_id})

def all_posts(request, forum_id):
    try:
        forum = Forum.objects.get(id=forum_id)
    except Forum.DoesNotExist:
        raise Http404('Форум не найден')
    posts = Post.objects.all().order_by('created_at')
    return render(request, 'blog/all_posts.html', {'posts': posts, 'forum_id': forum_id})

def post(request, forum_id, post_id):
    try:
        post = Post.objects.all().get(id = post_id)
    except Post.DoesNotExist:
        raise Http404('Запись не найдена')
    if not post.is_publish() and not request.user.is_staff:
        raise Http404('Запись в блоге не найдена')
    comments = Comment.objects.filter(post=post)
    return render(request, 'blog/post.html', {'post': post, 'comments': comments, 'forum_id': forum_id})

@login_required
def post_edit(request, post_id=None, forum_id=None):
    if request.user.is_authenticated:
        return post_update(request, post_id, forum_id)
    return redirect('post_list', forum_id=forum_id)
    
def post_update(request, post_id, forum_id):
    if post_id:    
        try:
            post = Post.published.all().get(id = post_id)
        except Post.DoesNotExist:
            raise Http404('Запись не найдена')
        if post and post.author != request.user:
            return redirect('post_list', forum_id=forum_id)
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
        else:
            form = PostForm(instance=post)
    else:
        if request.method == "POST":
            form = PostForm(request.POST)
        else:
            form = PostForm()
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        if post.is_published:
            post.published_at=timezone.now()
        else:
            post.published_date=None
        post.save()
        return redirect('post', post_id=post.id, forum_id=forum_id)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_publish(request, post_id, forum_id):
    try:
        post = Post.objects.all().get(id = post_id)
    except Post.DoesNotExist:
        raise Http404('Запись не найдена')
    post.publish()
    return redirect('post', post_id=post_id, forum_id=forum_id)

@login_required
def comment_edit(request, forum_id, post_id, comment_id=None):
    if request.user.is_authenticated:
        return comment_update(request, comment_id=comment_id, post_id=post_id, forum_id=post_id)
    return redirect('post', forum_id=forum_id, post_id=post_id)
    
def comment_update(request, post_id, forum_id, comment_id):
    if comment_id:    
        try:
            comment = Comment.objects.all().get(id = comment_id)
        except Comment.DoesNotExist:
            raise Http404('Комментарий не найден')
        if comment and comment.author != request.user:
            return redirect('post', forum_id=forum_id, post_id=post_id)
        if request.method == "POST":
            form = CommentForm(request.POST, instance=comment)
        else:
            form = CommentForm(instance=comment)
    else:
        if request.method == "POST":
            form = CommentForm(request.POST)
        else:
            form = CommentForm()
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post  = Post.published.all().get(id = post_id)
        comment.save()
        return redirect('post', forum_id=forum_id, post_id=post_id)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def forum_edit(request, forum_id=None):
    if request.user.is_authenticated:
        return forum_update(request, forum_id)
    return redirect('forum_list')
    
def forum_update(request, forum_id):
    if forum_id:    
        try:
            forum = Forum.all().get(id = forum_id)
        except Forum.DoesNotExist:
            raise Http404('Форум не найден')
        if forum and forum.author != request.user:
            return redirect('forum_list')
        if request.method == "POST":
            form = ForumForm(request.POST, instance=forum)
        else:
            form = ForumForm(instance=forum)
    else:
        if request.method == "POST":
            form = ForumForm(request.POST)
        else:
            form = ForumForm()
    if form.is_valid():
        forum = form.save(commit=False)
        forum.author = request.user
        forum.save()
        return redirect('post_list', forum_id=forum.id)
    return render(request, 'blog/forum_edit.html', {'form': form})
