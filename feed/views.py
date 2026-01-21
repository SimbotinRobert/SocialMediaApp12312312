from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import PostForm, ProfileForm, CommentForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden
from .models import Post, Profile, Vote
from django.db.models import F,Sum
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from .models import Comment

@login_required(login_url='feed:register')
def feed(request):
    posts = Post.objects.all().annotate(total_score=Sum('vote__value')).order_by('-pub_date')
    context = {'posts': posts}
    return render(request, 'feed/feed.html', context)

def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
        return redirect('feed:feed')
    else:
        form = UserCreationForm()

    return render(request, 'feed/register.html', {'form': form})

def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('feed:feed')
        else:
            messages.error(request, "Nume de utilizator sau parolă incorectă!")
    else:
        form = AuthenticationForm()

    return render(request, 'feed/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('feed:feed')

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            return redirect('feed:feed')
    else:
        form = PostForm()

    return render(request, 'feed/create_post.html', {'form': form, 'user': request.user})

@login_required
def view_profile(request):
    profile,created = Profile.objects.get_or_create(user=request.user)
    user_posts = Post.objects.filter(user=request.user).annotate(total_score=Sum('vote__value')).order_by('-pub_date')
    context = {'profile': profile,'user': request.user,'user_posts': user_posts}
    return render(request, 'feed/profile.html', context)

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post,pk=pk)
    if post.user != request.user:
        return HttpResponseForbidden('You are not the owner')
    if request.method == "POST":
        post.delete()
    return redirect('feed:profile')

@login_required()
def public_profile(request, username):
    target_user = get_object_or_404(User, username=username)
    target_profile, created = Profile.objects.get_or_create(user=target_user)
    target_posts = Post.objects.filter(user=target_user).order_by('-pub_date')

    context = {
        'target_user': target_user,
        'target_profile': target_profile,
        'target_posts': target_posts,
    }
    return render(request, 'feed/public_profile.html', context)

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('feed:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'feed/edit_profile.html', {'form': form})

@login_required
def vote_post(request, pk,vote_type):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    new_value = 1 if vote_type == 'Like' else -1
    existing_vote = Vote.objects.filter(post=post, user=user).first()

    if existing_vote:
        if existing_vote.value == new_value:
            existing_vote.delete()
        else:
            existing_vote.value =new_value
            existing_vote.save()
    else:
        Vote.objects.create(post=post, user=user, value=new_value)

    return redirect(request.META.get('HTTP_REFERER','feed:feed'))

@login_required()
def add_comment(request,pk):
    previous_page = request.META.get('HTTP_REFERER')
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            if previous_page:
                return redirect(previous_page)
            return redirect('feed:feed')

    if previous_page:
        return redirect(previous_page)

    return redirect('feed:feed')


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.user == comment.user:
        comment.delete()

    previous_page = request.META.get('HTTP_REFERER')

    if previous_page:
        return redirect(previous_page)

    return redirect('feed:feed')