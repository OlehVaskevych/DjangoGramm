from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('', views.main, name='main'),

    # path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/<str:username>/update/', views.profile_update_view, name='profile_update'),
    path('profile/<str:username>/follows', views.follow_view, name='follow'),

    path('news/', views.news_feed, name='news'),

    path('post/', views.post_create_view, name='post_create'),
    path('api/post/<int:post_id>/', views.post_view, name='post_detail'),
    path('api/posts/', views.posts_view, name='posts'),

    path('post/<int:post_id>/likes', views.post_like_view, name='add_like'),
    path('post/<int:post_id>/comments', views.post_comment_view, name='add_comment'),
    path('post/<int:post_id>/comments/<int:comment_id>/', views.post_comment_delete_view, name='comment_delete'),

    path('api/post/<int:post_id>/update/', views.post_update_view, name='post_edit'),

    path('auth/register/', views.register_view, name='register'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),

    path('settings/', views.settings_view, name='settings'),

    path('api/profile/<str:username>/', views.profile_view, name='get_profile_data'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)