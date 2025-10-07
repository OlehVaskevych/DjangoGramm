"""
URL configuration for the social network application.

This module defines all URL patterns for the application, including:
- Authentication endpoints (login, register, logout)
- Profile management (view, update, follow)
- Post operations (create, view, update, delete, like, comment)
- API endpoints for data retrieval
- Settings page

All URLs are organized by functionality for better maintainability.
"""

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    # Main page
    path('', views.main, name='main'),

    # Profile endpoints
    # View and update user profiles, manage follow relationships
    path('profile/<str:username>/update/', views.profile_update_view, name='profile_update'),
    path('profile/<str:username>/follows/', views.follow_view, name='follow'),

    # Post management endpoints
    # Create, view, update, and retrieve posts
    path('post/', views.post_create_view, name='post_create'),
    path('api/post/<int:post_id>/', views.post_view, name='post_detail'),
    path('api/posts/', views.posts_view, name='posts'),
    path('api/post/<int:post_id>/update/', views.post_update_view, name='post_edit'),

    # Post interaction endpoints
    # Like posts, add/delete comments
    path('post/<int:post_id>/likes', views.post_like_view, name='add_like'),
    path('post/<int:post_id>/comments', views.post_comment_view, name='add_comment'),
    path('post/<int:post_id>/comments/<int:comment_id>/', views.post_comment_delete_view, name='comment_delete'),

    # Authentication endpoints
    # User registration, login, and logout
    path('auth/register/', views.register_view, name='register'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),

    # Settings page
    path('settings/', views.settings_view, name='settings'),

    # API endpoints
    # Retrieve current user data and profile information
    path("api/current-user/", views.current_user_view, name="current_user"),
    path('api/profile/<str:username>/', views.profile_view, name='get_profile_data'),
]

# Serve media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
