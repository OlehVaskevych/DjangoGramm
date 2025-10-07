from django.db import IntegrityError, DatabaseError
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_protect
from functools import wraps
import json
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.views.decorators.http import require_http_methods

from .forms import ProfileEditForm, PostEditForm, PostCreateForm
from .models import Profile, Post, Comment, Image, Follow


ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jpeg']
MAX_IMAGE_SIZE = 10 * 1024 * 1024 # 10mb


def user_is_profile_owner(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        username = kwargs.get('username')

        # 1. Перевірка, чи поточний користувач є власником
        if request.user.username != username:

            # 2. Якщо це AJAX/Fetch запит (або просто небезпечний метод для додаткової стійкості)
            # В більшості сучасних SPA-фреймворків, якщо запит приходить від Fetch API,
            # найкраще просто повернути JSON-помилку.
            if request.method != 'GET' or request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'error_message': 'You are not authorized to edit this profile.'
                }, status=403)

            # 3. Якщо це звичайний перехід (не AJAX), виконуємо перенаправлення
            return redirect('main')

        return view_func(request, *args, **kwargs)

    return wrapper


def main(request):
    posts = Post.objects.prefetch_related('images').all()

    posts_json = [
        {
            "id": post.id,
            "title": post.title,
            "description": post.description,
            "user": {
                "username": post.user.username,
                "profile": {
                    "avatar": {
                        "url": post.user.profile.avatar.url,
                    }
                }
            },
            "likes": {
                "count": post.likes.all().count(),
                "all": [
                    {
                        "username": user.username,
                    }
                    for user in post.likes.all()
                ]
            },
            "comments": [
                {
                    "id": comment.id,
                    "author": { "username": comment.author.username },
                    "text": comment.text,
                    "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
                for comment in post.comments.all()
            ],
            "images": [
                {
                    "image_file": { "url": image.image_file.url },
                }
                for image in post.images.all()
            ]
        }
        for post in posts
    ]

    context = {
        "posts": posts_json,
        "current_user": {
            "username": request.user.username if request.user.is_authenticated else None,
            "profile": {
                "avatar": {
                    "url": request.user.profile.avatar.url if request.user.is_authenticated else None,
                }
            } if request.user.is_authenticated else None
        },
        "userIsAuthenticated": request.user.is_authenticated,
    }

    return render(request, 'index.html', context)


def profile_view(request, username):
    user = get_object_or_404(User.objects.select_related('profile'), username=username)
    posts = Post.objects.filter(user_id=user.id).select_related('user')
    followers = user.followers.count()
    followings = user.followings.count()

    # Перевірка, чи користувач авторизований
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()

    return JsonResponse({
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        },
        "profile": {
            "first_name": user.profile.first_name,
            "last_name": user.profile.last_name,
            "bio": user.profile.bio,
            "avatar": user.profile.avatar.url if user.profile.avatar else None,
        },
        "posts": [
            {
                "id": post.id,
                "images": [{"image_file": img.image_file.url} for img in post.images.all()],
                "likes": [like.id for like in post.likes.all()],
                "comments": [c.id for c in post.comments.all()],
            }
            for post in posts
        ],
        "followers": followers,
        "followings": followings,
        "is_following": is_following,
        "current_user": request.user.id if request.user.is_authenticated else None,
    })



@login_required
@user_is_profile_owner
def profile_update_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        if request.POST.get("_method") == 'PUT':
            if request.POST.get('remove_avatar'):
                profile.avatar = settings.DEFAULT_AVATAR_PATH

            form = ProfileEditForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return JsonResponse({'status': 'success', 'redirect_url': f'/profile/{user.username}/'})
            else:
                # Повертаємо помилки форми
                return JsonResponse({
                    'status': 'error',
                    'errors': form.errors,
                    'error_message': 'Form validation failed. Please check the input fields.'
                }, status=400)

        elif request.POST.get("_method") == 'DELETE':
            user.delete()
            return JsonResponse({'status': 'success', 'redirect_url': f'/'})

    elif request.method == 'GET':
        initial_data = {
            'id': request.user.id,
            'username': request.user.username,
            'first_name': request.user.profile.first_name,
            'last_name': request.user.profile.last_name,
            'bio': request.user.profile.bio,
            'avatar': request.user.profile.avatar.url,
        }
        return JsonResponse({'status': 'success', 'initial_data': initial_data})

    else:
        return JsonResponse({'status': 'error', 'error_message': 'Invalid method specified'}, status=400)



def post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    post_json = {
        "id": post.id,
        "title": post.title,
        "description": post.description,
        "user": {
            "username": post.user.username,
            "profile": {
                "avatar": {
                    "url": post.user.profile.avatar.url,
                }
            }
        },
        "likes": {
            "count": post.likes.count(),
            "all": [
                {"username": user.username}
                for user in post.likes.all()
            ]
        },
        "comments": [
            {
                "id": comment.id,
                "author": {"username": comment.author.username},
                "text": comment.text,
                "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for comment in post.comments.all()
        ],
        "images": [
            {"image_file": {"url": image.image_file.url}}
            for image in post.images.all()
        ]
    }

    return JsonResponse({
        "post": post_json,   # ✅ тепер один пост, а не масив
        "currentUser": {
            "username": request.user.username if request.user.is_authenticated else None,
            "profile": {
                "avatar": {
                    "url": request.user.profile.avatar.url if request.user.is_authenticated else None,
                }
            } if request.user.is_authenticated else None
        },
        "userIsAuthenticated": request.user.is_authenticated,
    })


def posts_view(request):
    page_number = int(request.GET.get("page", 1))
    per_page = int(request.GET.get("limit", 10))
    feed_type = request.GET.get("feed", "all")  # 'all' або 'news'

    # 🔹 Якщо користувач відкрив сторінку News — потрібен логін
    if feed_type == "news":
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Authentication required to view followed users' posts.")

        # Отримуємо користувачів, на яких поточний користувач підписаний
        followed_users = Follow.objects.filter(follower=request.user).values_list("following", flat=True)

        # Якщо ще ні на кого не підписаний — порожній список
        posts_qs = Post.objects.filter(user__id__in=followed_users).order_by("-id")

    else:
        # 🔹 Для головної сторінки — усі пости
        posts_qs = Post.objects.all().order_by("-id")

    paginator = Paginator(posts_qs, per_page)
    page_obj = paginator.get_page(page_number)

    posts_json = [
        {
            "id": post.id,
            "title": post.title,
            "description": post.description,
            "user": {
                "username": post.user.username,
                "profile": {
                    "avatar": {
                        "url": post.user.profile.avatar.url if getattr(post.user.profile.avatar, "url", None) else "",
                    }
                }
            },
            "likes": {
                "count": post.likes.count(),
                "all": [{"username": u.username} for u in post.likes.all()]
            },
            "comments": [
                {
                    "id": c.id,
                    "author": {"username": c.author.username},
                    "text": c.text,
                    "created_at": c.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
                for c in post.comments.all()
            ],
            "images": [
                {"image_file": {"url": i.image_file.url}}
                for i in post.images.all()
            ],
        }
        for post in page_obj
    ]

    return JsonResponse({
        "posts": posts_json,
        "has_next": page_obj.has_next(),
        "page": page_number,
    })


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
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({"liked": liked, "likes_count": post.likes.count()})


@login_required
@csrf_protect
def post_comment_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        if comment_text:
            created_comment = Comment.objects.create(post=post, author=request.user, text=comment_text)
            return JsonResponse({
                "id": created_comment.id,
                "author": { "username": created_comment.author.username },
                "text": created_comment.text,
                "created_at": created_comment.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            })
        else:
            return JsonResponse({'status': 'error', 'message': 'Comment text is empty'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)


@login_required
@csrf_protect
def post_comment_delete_view(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=comment_id, post=post)
    if request.user == comment.author:
        deleted_comment = comment.id
        comment.delete()
        return JsonResponse({'id': deleted_comment})


@login_required
@csrf_protect
def post_update_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)

    if request.method == 'POST':
        method = request.POST.get('_method')

        if method == 'PUT':
            form = PostEditForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                return JsonResponse({
                    'status': 'success',
                    'post_id': post.id,
                    'redirect_url': f"/post/{post.id}"
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'errors': form.errors
                }, status=400)

        elif method == 'DELETE':
            post.delete()
            return JsonResponse({'status': 'success', 'redirect_url': "/"})

        else:
            return HttpResponseBadRequest('Invalid _method specified')

    elif request.method == 'GET':
        # ⚡ віддаємо JSON замість шаблону
        initial_data = {
            'id': post.id,
            'title': post.title,
            'description': post.description,
        }
        return JsonResponse(initial_data)

    return HttpResponseBadRequest('Invalid request method')



def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({'status': 'success', 'redirect_url': f"/profile/{user.username}/"})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return JsonResponse({'status': 'success', 'redirect_url': f"/"})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'status': 'success', 'redirect_url': f"/"})
    return render(request, 'logout.html')


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404
from django.db import IntegrityError, DatabaseError

from .models import Follow
from django.contrib.auth.models import User


@login_required
@csrf_protect
def follow_view(request, username):
    user_to_follow = get_object_or_404(User, username=username)

    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'msg': 'Invalid method'}, status=405)

    if request.user == user_to_follow:
        return JsonResponse({'status': 'error', 'msg': 'You cannot follow yourself'}, status=400)

    try:
        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )

        if created:
            # ✅ Успішно підписався
            return JsonResponse({'status': 'success', 'action': 'followed', 'username': username})

        else:
            # ❗ Якщо вже підписаний — відписуємося
            follow.delete()
            return JsonResponse({'status': 'success', 'action': 'unfollowed', 'username': username})

    except (IntegrityError, DatabaseError):
        return JsonResponse({'status': 'error', 'msg': 'Database error'}, status=500)


@login_required
def settings_view(request):
    return render(request, 'settings.html')