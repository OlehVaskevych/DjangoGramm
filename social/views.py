"""
Django views for the social network application.

This module contains all view functions for handling user authentication,
profiles, posts, comments, likes, follows, and settings.
"""

import json
from functools import wraps

from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import AnonymousUser, User
from django.core.paginator import Paginator
from django.db import DatabaseError, IntegrityError
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods

from .forms import PostCreateForm, PostEditForm, ProfileEditForm
from .models import Comment, Follow, Image, Post, Profile

ALLOWED_EXTENSIONS = [".png", ".jpg", ".jpeg"]
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB


def user_is_profile_owner(view_func):
    """
    Decorator to ensure that only the profile owner can access certain views.

    Checks if the authenticated user matches the username in the URL.
    Returns a 403 JSON error for AJAX requests or redirects for regular requests.

    Args:
        view_func: The view function to wrap

    Returns:
        The wrapped view function with ownership validation
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        username = kwargs.get("username")

        # Check if the current user is the owner
        if request.user.username != username:
            # For AJAX/Fetch requests or unsafe methods
            # In most modern SPA frameworks, if the request comes from Fetch API,
            # it's best to return a JSON error
            if (
                request.method != "GET"
                or request.headers.get("x-requested-with") == "XMLHttpRequest"
            ):
                return JsonResponse(
                    {
                        "status": "error",
                        "error_message": "You are not authorized to edit this profile.",
                    },
                    status=403,
                )

            # For regular navigation (not AJAX), perform a redirect
            return redirect("main")

        return view_func(request, *args, **kwargs)

    return wrapper


def main(request):
    """
    Main page view that displays all posts.

    Fetches all posts with their images, likes, and comments, and serializes
    them to JSON format for the frontend.

    Args:
        request: The HTTP request object

    Returns:
        Rendered HTML template with posts data and current user information
    """
    posts = Post.objects.prefetch_related("images").all()

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
                },
            },
            "likes": {
                "count": post.likes.all().count(),
                "all": [
                    {
                        "username": user.username,
                    }
                    for user in post.likes.all()
                ],
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
                {
                    "image_file": {"url": image.image_file.url},
                }
                for image in post.images.all()
            ],
        }
        for post in posts
    ]

    context = {
        "posts": posts_json,
        "current_user": {
            "username": (
                request.user.username if request.user.is_authenticated else None
            ),
            "profile": (
                {
                    "avatar": {
                        "url": (
                            request.user.profile.avatar.url
                            if request.user.is_authenticated
                            else None
                        ),
                    }
                }
                if request.user.is_authenticated
                else None
            ),
        },
        "userIsAuthenticated": request.user.is_authenticated,
    }

    return render(request, "index.html", context)


def profile_view(request, username):
    """
    User profile view that displays profile information and posts.

    Returns JSON data containing user information, profile details, posts,
    follower/following counts, and follow status.

    Args:
        request: The HTTP request object
        username: The username of the profile to view

    Returns:
        JsonResponse with profile data and posts
    """
    user = get_object_or_404(User.objects.select_related("profile"), username=username)
    posts = Post.objects.filter(user_id=user.id).select_related("user")
    followers = user.followers.count()
    followings = user.followings.count()

    # Check if the current user is following this profile
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(
            follower=request.user, following=user
        ).exists()

    return JsonResponse(
        {
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
                    "images": [
                        {"image_file": img.image_file.url} for img in post.images.all()
                    ],
                    "likes": [like.id for like in post.likes.all()],
                    "comments": [c.id for c in post.comments.all()],
                }
                for post in posts
            ],
            "followers": followers,
            "followings": followings,
            "is_following": is_following,
            "current_user": request.user.id if request.user.is_authenticated else None,
        }
    )


@login_required
@user_is_profile_owner
def profile_update_view(request, username):
    """
    Profile update view for editing user profile information.

    Handles GET requests to fetch current profile data and POST requests
    with PUT method to update profile or DELETE method to delete account.

    Args:
        request: The HTTP request object
        username: The username of the profile to update

    Returns:
        JsonResponse with success/error status and redirect URL or form errors
    """
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == "POST":
        if request.POST.get("_method") == "PUT":
            # Handle avatar removal if requested
            if request.POST.get("remove_avatar"):
                profile.avatar = settings.DEFAULT_AVATAR_PATH

            form = ProfileEditForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return JsonResponse(
                    {"status": "success", "redirect_url": f"/profile/{user.username}/"}
                )
            else:
                # Return form validation errors
                return JsonResponse(
                    {
                        "status": "error",
                        "errors": form.errors,
                        "error_message": "Form validation failed. Please check the input fields.",
                    },
                    status=400,
                )

        elif request.POST.get("_method") == "DELETE":
            # Delete user account
            user.delete()
            return JsonResponse({"status": "success", "redirect_url": f"/"})

    elif request.method == "GET":
        # Return current profile data
        initial_data = {
            "id": request.user.id,
            "username": request.user.username,
            "first_name": request.user.profile.first_name,
            "last_name": request.user.profile.last_name,
            "bio": request.user.profile.bio,
            "avatar": request.user.profile.avatar.url,
        }
        return JsonResponse({"status": "success", "initial_data": initial_data})

    else:
        return JsonResponse(
            {"status": "error", "error_message": "Invalid method specified"}, status=400
        )


def post_view(request, post_id):
    """
    Single post detail view.

    Returns JSON data for a specific post including title, description,
    author information, likes, comments, and images.

    Args:
        request: The HTTP request object
        post_id: The ID of the post to view

    Returns:
        JsonResponse with post data and current user information
    """
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
            },
        },
        "likes": {
            "count": post.likes.count(),
            "all": [{"username": user.username} for user in post.likes.all()],
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
            {"image_file": {"url": image.image_file.url}} for image in post.images.all()
        ],
    }

    return JsonResponse(
        {
            "post": post_json,
            "currentUser": {
                "username": (
                    request.user.username if request.user.is_authenticated else None
                ),
                "profile": (
                    {
                        "avatar": {
                            "url": (
                                request.user.profile.avatar.url
                                if request.user.is_authenticated
                                else None
                            ),
                        }
                    }
                    if request.user.is_authenticated
                    else None
                ),
            },
            "userIsAuthenticated": request.user.is_authenticated,
        }
    )


def posts_view(request):
    """
    Paginated posts feed view.

    Supports two feed types:
    - 'all': Shows all posts (default)
    - 'news': Shows posts only from followed users (requires authentication)

    Args:
        request: The HTTP request object with optional query parameters:
            - page: Page number (default: 1)
            - limit: Posts per page (default: 10)
            - feed: Feed type 'all' or 'news' (default: 'all')

    Returns:
        JsonResponse with paginated posts data and pagination info
    """
    page_number = int(request.GET.get("page", 1))
    per_page = int(request.GET.get("limit", 10))
    feed_type = request.GET.get("feed", "all")  # 'all' or 'news'

    # If user opened the News page, authentication is required
    if feed_type == "news":
        if not request.user.is_authenticated:
            return HttpResponseForbidden(
                "Authentication required to view followed users' posts."
            )

        # Get users that the current user is following
        followed_users = Follow.objects.filter(follower=request.user).values_list(
            "following", flat=True
        )

        # If not following anyone yet, return empty list
        posts_qs = Post.objects.filter(user__id__in=followed_users).order_by("-id")

    else:
        # For the main page, show all posts
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
                        "url": (
                            post.user.profile.avatar.url
                            if getattr(post.user.profile.avatar, "url", None)
                            else ""
                        ),
                    }
                },
            },
            "likes": {
                "count": post.likes.count(),
                "all": [{"username": u.username} for u in post.likes.all()],
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
                {"image_file": {"url": i.image_file.url}} for i in post.images.all()
            ],
        }
        for post in page_obj
    ]

    return JsonResponse(
        {
            "posts": posts_json,
            "has_next": page_obj.has_next(),
            "page": page_number,
        }
    )


@login_required
@csrf_protect
def post_create_view(request):
    """
    Post creation view.

    Handles POST requests to create a new post with images.
    Validates image size (max 10MB per image) and requires at least one image.

    Args:
        request: The HTTP request object with POST data and FILES

    Returns:
        JsonResponse with success status and redirect URL or error message
        For GET requests, renders the post creation form
    """
    if request.method == "POST":
        form = PostCreateForm(request.POST)
        images = request.FILES.getlist("images")

        if images:
            # Validate image sizes
            invalid_images = [
                image_file.name
                for image_file in images
                if image_file.size > MAX_IMAGE_SIZE
            ]

            if invalid_images:
                error_message = f"The following images are too large (max 10MB): {', '.join(invalid_images)}"
                return JsonResponse(
                    {"status": "error", "error_message": error_message}, status=400
                )

            # Validate form
            if form.is_valid():
                # Save post
                post = form.save(commit=False)
                post.user = request.user
                post.save()

                # Upload and save images
                uploaded_files = []
                for image_file in images:
                    image_instance = Image.objects.create(
                        post=post, image_file=image_file
                    )
                    uploaded_files.append(image_instance.image_file.url)

                return JsonResponse(
                    {
                        "status": "success",
                        "post_id": post.id,
                        "redirect_url": f"/post/{post.id}",
                    }
                )
            else:
                return JsonResponse(
                    {"status": "error", "error_message": "Form is invalid"}, status=400
                )
        else:
            error_message = "You must select at least one image to create the post."
            return JsonResponse(
                {"status": "error", "error_message": error_message}, status=400
            )

    else:
        form = PostCreateForm()

    return render(request, "post_create.html", {"form": form})


@login_required
@csrf_protect
def post_like_view(request, post_id):
    """
    Post like/unlike toggle view.

    Toggles the like status for the current user on a specific post.
    If already liked, removes the like; if not liked, adds a like.

    Args:
        request: The HTTP request object
        post_id: The ID of the post to like/unlike

    Returns:
        JsonResponse with liked status (boolean) and total likes count
    """
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
    """
    Post comment creation view.

    Creates a new comment on a specific post.

    Args:
        request: The HTTP request object with POST data containing 'comment' text
        post_id: The ID of the post to comment on

    Returns:
        JsonResponse with created comment data or error message
    """
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        comment_text = request.POST.get("comment")
        if comment_text:
            created_comment = Comment.objects.create(
                post=post, author=request.user, text=comment_text
            )
            return JsonResponse(
                {
                    "id": created_comment.id,
                    "author": {"username": created_comment.author.username},
                    "text": created_comment.text,
                    "created_at": created_comment.created_at.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                }
            )
        else:
            return JsonResponse(
                {"status": "error", "message": "Comment text is empty"}, status=400
            )
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)


@login_required
@csrf_protect
def post_comment_delete_view(request, post_id, comment_id):
    """
    Comment deletion view.

    Deletes a comment if the current user is the comment author.

    Args:
        request: The HTTP request object
        post_id: The ID of the post containing the comment
        comment_id: The ID of the comment to delete

    Returns:
        JsonResponse with deleted comment ID
    """
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=comment_id, post=post)
    if request.user == comment.author:
        deleted_comment = comment.id
        comment.delete()
        return JsonResponse({"id": deleted_comment})


@login_required
@csrf_protect
def post_update_view(request, post_id):
    """
    Post update and deletion view.

    Handles GET requests to fetch post data for editing,
    POST with PUT method to update post, and POST with DELETE method to delete post.
    Only the post owner can update or delete their posts.

    Args:
        request: The HTTP request object
        post_id: The ID of the post to update or delete

    Returns:
        JsonResponse with post data, success status, or error message
    """
    post = get_object_or_404(Post, id=post_id, user=request.user)

    if request.method == "POST":
        method = request.POST.get("_method")

        if method == "PUT":
            # Update post
            form = PostEditForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                return JsonResponse(
                    {
                        "status": "success",
                        "post_id": post.id,
                        "redirect_url": f"/post/{post.id}",
                    }
                )
            else:
                return JsonResponse(
                    {"status": "error", "errors": form.errors}, status=400
                )

        elif method == "DELETE":
            # Delete post
            post.delete()
            return JsonResponse({"status": "success", "redirect_url": "/"})

        else:
            return HttpResponseBadRequest("Invalid _method specified")

    elif request.method == "GET":
        # Return post data for editing
        initial_data = {
            "id": post.id,
            "title": post.title,
            "description": post.description,
        }
        return JsonResponse(initial_data)

    return HttpResponseBadRequest("Invalid request method")


def register_view(request):
    """
    User registration view.

    Handles user registration with Django's UserCreationForm.
    Automatically logs in the user after successful registration.

    Args:
        request: The HTTP request object

    Returns:
        JsonResponse with success status and redirect URL or form errors
        For GET requests, renders the registration form
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse(
                {"status": "success", "redirect_url": f"/profile/{user.username}/"}
            )
        else:
            return JsonResponse({"status": "error", "errors": form.errors})
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    """
    User login view.

    Handles user authentication with Django's AuthenticationForm.

    Args:
        request: The HTTP request object

    Returns:
        JsonResponse with success status and redirect URL or form errors
        For GET requests, renders the login form
    """
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return JsonResponse({"status": "success", "redirect_url": f"/"})
        else:
            return JsonResponse({"status": "error", "errors": form.errors})
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


@login_required
def logout_view(request):
    """
    User logout view.

    Logs out the current user and redirects to the home page.

    Args:
        request: The HTTP request object

    Returns:
        JsonResponse with success status and redirect URL
        For GET requests, renders the logout confirmation page
    """
    if request.method == "POST":
        logout(request)
        return JsonResponse({"status": "success", "redirect_url": f"/"})
    return render(request, "logout.html")


@login_required
@csrf_protect
def follow_view(request, username):
    """
    Follow/unfollow toggle view.

    Toggles the follow status for the current user on a specific user.
    If already following, unfollows; if not following, follows.
    Users cannot follow themselves.

    Args:
        request: The HTTP request object
        username: The username of the user to follow/unfollow

    Returns:
        JsonResponse with success status and action performed ('followed' or 'unfollowed')
    """
    user_to_follow = get_object_or_404(User, username=username)

    if request.method != "POST":
        return JsonResponse({"status": "error", "msg": "Invalid method"}, status=405)

    if request.user == user_to_follow:
        return JsonResponse(
            {"status": "error", "msg": "You cannot follow yourself"}, status=400
        )

    try:
        follow, created = Follow.objects.get_or_create(
            follower=request.user, following=user_to_follow
        )

        if created:
            # Successfully followed
            return JsonResponse(
                {"status": "success", "action": "followed", "username": username}
            )

        else:
            # Already following, so unfollow
            follow.delete()
            return JsonResponse(
                {"status": "success", "action": "unfollowed", "username": username}
            )

    except (IntegrityError, DatabaseError):
        return JsonResponse({"status": "error", "msg": "Database error"}, status=500)


@login_required
def settings_view(request):
    """
    Settings page view.

    Renders the settings page for authenticated users.

    Args:
        request: The HTTP request object

    Returns:
        Rendered settings.html template
    """
    return render(request, "settings.html")


@login_required
def current_user_view(request):
    """
    Current user information view.

    Returns JSON data for the currently authenticated user including
    username, email, name, and avatar.

    Args:
        request: The HTTP request object

    Returns:
        JsonResponse with current user data
    """
    user = request.user
    profile = getattr(user, "profile", None)

    return JsonResponse(
        {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "avatar": profile.avatar.url if profile and profile.avatar else None,
        }
    )
