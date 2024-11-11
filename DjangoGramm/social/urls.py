from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('', views.home, name='home'),

    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/<str:username>/edit', views.profile_edit_view, name='profile_edit'),
    path('profile/<str:username>/delete', views.profile_delete_view, name='profile_delete'),

    path('post/<int:post_id>/', views.post_view, name='post_detail'),
    path('post/', views.post_create_view, name='post_create'),
    path('post/<int:post_id>/like', views.post_like_view, name='add_like'),

    path('post/<int:post_id>/comment', views.post_comment_view, name='add_comment'),
    path('post/<int:post_id>/comment/<int:comment_id>/delete', views.post_comment_delete_view, name='comment_delete'),

    path('post/<int:post_id>/delete', views.post_delete_view, name='post_delete'),
    path('post/<int:post_id>/edit', views.post_edit_view, name='post_edit'),

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)