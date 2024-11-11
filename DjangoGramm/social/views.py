from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User

from .forms import ProfileEditForm, PostEditForm, PostCreateForm
from .models import Profile, Post, Comment, Image


def home(request):
    posts = Post.objects.all()
    image = Image.objects.all()

    return render(request, 'home.html', {'posts': posts, 'image': image})


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    posts = Post.objects.filter(user_id=user.id)

    return render(request, 'profile.html', {'user': user, 'profile': profile, 'posts': posts})


@login_required
def profile_edit_view(request, username):
    if request.user.username != username:
        return redirect('profile', username=request.user.username)

    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileEditForm(instance=profile)

    return render(request, 'profile_edit.html', {'form': form, 'profile': profile, 'user': user})


@login_required
def profile_delete_view(request, username):
    user = get_object_or_404(User, username=username)
    if request.user != user:
        return redirect('profile', username=request.user.username)

    if request.method == 'POST':
        user.delete()
        return redirect('home')

    return render(request, 'profile_delete.html', {'profile_user': user})


def post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()  # Get all comments related to the post
    images = post.images.all()  # Get all images related to the post
    tags = post.tags.all()  # Get all tags related to the post
    like_count = post.likes.count()  # Get the number of likes for the post

    context = {
        'post': post,
        'comments': comments,
        'images': images,
        'tags': tags,
        'like_count': like_count,
    }
    return render(request, 'post.html', context)


@login_required
def post_create_view(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            # Save the post instance
            post = form.save(commit=False)
            post.user = request.user  # Associate the post with the logged-in user
            post.save()
            form.save_m2m()  # Save any many-to-many fields, if applicable

            # Handle multiple image uploads
            images = request.FILES.getlist('images')
            for image_file in images:
                Image.objects.create(post=post, image_file=image_file)

            return redirect('post_detail', post_id=post.id)  # Redirect to the post detail page
    else:
        form = PostCreateForm()

    return render(request, 'post_create.html', {'form': form})


@login_required
def post_like_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def post_comment_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        if comment_text:
            Comment.objects.create(post=post, author=request.user, text=comment_text)
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def post_comment_delete_view(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=comment_id, post=post)
    if request.user == comment.author:
        comment.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def post_edit_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        form = PostEditForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostEditForm(instance=post)
    return render(request, 'post_edit.html', {'form': form, 'post': post})


@login_required
def post_delete_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'post_delete.html', {'post': post})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            Profile.objects.create(user=user)  # Create an empty profile for the new user
            return redirect('profile', username=user.username)
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    return render(request, 'logout.html')
