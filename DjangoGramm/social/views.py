from django.db import IntegrityError, DatabaseError
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from functools import wraps

from .forms import ProfileEditForm, PostEditForm, PostCreateForm
from .models import Profile, Post, Comment, Image, Follow


ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jpeg']
MAX_IMAGE_SIZE = 10 * 1024 * 1024 # 10mb


def user_is_profile_owner(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        username = kwargs.get('username')
        if request.user.username != username:
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


def home(request):
    posts = Post.objects.prefetch_related('images').all()

    return render(request, 'home.html', {'posts': posts})


def profile_view(request, username):
    user = get_object_or_404(User.objects.select_related('profile'), username=username)
    posts = Post.objects.filter(user_id=user.id).select_related('user')
    followers = user.followers.count()
    followings = user.followings.count()

    # Перевірка, чи користувач авторизований
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()

    return render(
        request,
        'profile.html',
        {
            'user': user,
            'profile': user.profile,
            'posts': posts,
            'followers': followers,
            'followings': followings,
            'is_following': is_following
        }
    )



@login_required
@user_is_profile_owner
def profile_update_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        if request.POST.get("_method") == 'PUT':
            form = ProfileEditForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('profile', username=request.user.username)
        elif request.POST.get("_method") == 'DELETE':
            user.delete()
            return redirect('home')

    else:
        form = ProfileEditForm(instance=profile)

    return render(request, 'profile_edit.html', {'form': form, 'profile': profile, 'user': user})


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
@csrf_protect
def post_create_view(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        images = request.FILES.getlist('images')

        if images:
            # Перевірка на розмір зображень
            invalid_images = [image_file.name for image_file in images if image_file.size > MAX_IMAGE_SIZE]

            if invalid_images:
                error_message = f"The following images are too large (max 10MB): {', '.join(invalid_images)}"
                return JsonResponse({'status': 'error', 'error_message': error_message}, status=400)

            # Перевірка форми
            if form.is_valid():
                # Зберегти пост
                post = form.save(commit=False)
                post.user = request.user
                post.save()

                uploaded_files = []
                for image_file in images:
                    image_instance = Image.objects.create(post=post, image_file=image_file)
                    uploaded_files.append(image_instance.image_file.url)

                return JsonResponse({'status': 'success', 'post_id': post.id, 'redirect_url': f"/post/{post.id}"})
            else:
                return JsonResponse({'status': 'error', 'error_message': 'Form is invalid'}, status=400)
        else:
            error_message = "You must select at least one image to create the post."
            return JsonResponse({'status': 'error', 'error_message': error_message}, status=400)

    else:
        form = PostCreateForm()

    return render(request, 'post_create.html', {'form': form})



@login_required
@csrf_protect
def post_like_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
@csrf_protect
def post_comment_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        if comment_text:
            Comment.objects.create(post=post, author=request.user, text=comment_text)
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
@csrf_protect
def post_comment_delete_view(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=comment_id, post=post)
    if request.user == comment.author:
        comment.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
@csrf_protect
def post_update_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)

    if request.method == 'POST':
        if request.POST.get('_method') == 'PUT':
            form = PostEditForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                return redirect('post_detail', post_id=post.id)
        elif request.POST.get('_method') == 'DELETE':
            post.delete()
            return redirect('home')
        else:
            # Якщо _method не дорівнює ні PUT, ні DELETE
            form = PostEditForm(instance=post)  # Форма повертається у вихідному стані
    else:
        form = PostEditForm(instance=post)

    return render(request, 'post_edit.html', {'form': form, 'post': post})



def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
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


@login_required
@csrf_protect
def follow_view(request, username):
    user_to_follow = get_object_or_404(User, username=username)

    if request.user == user_to_follow:
        # Заборонити підписку на себе
        return redirect('profile', username=username)

    try:
        follow, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
        if not created:

            try:
                follow.delete()

            except DatabaseError as e:
                print(f"Error deleting follow relationship: {e}")
                return redirect('profile', username=username)

    except IntegrityError as e:
        print(f"Integrity Error during follow creation: {e}")
        return redirect('profile', username=username)

    except DatabaseError as e:
        print(f"Database Error during follow creation: {e}")
        return redirect('profile', username=username)

    return redirect('profile', username=username)


@login_required
def news_feed(request):
    follows = Follow.objects.filter(follower=request.user)
    posts = Post.objects.filter(user_id__in=[follow.following for follow in follows]).order_by('-created_at')
    return render(request, 'news_feed.html', {'posts': posts})


@login_required
def settings_view(request):
    return render(request, 'settings.html')