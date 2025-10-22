import pytest
from django.contrib.auth.models import User
from social.models import Profile, Post, Like, Tag


@pytest.mark.django_db
def test_create_user_and_post():
    # Створення користувача
    user = User.objects.create_user(username='test_user', password='TestPassword123')

    # Створення профілю
    # profile = Profile.objects.create(user=user, first_name='Test', last_name='User', bio='This is a bio.')
    user.profile.first_name = 'TestFirstName'

    # Створення тега
    tag = Tag.objects.create(name='Django')

    # Створення поста
    post = Post.objects.create(user=user, title='Test', description='This is a test.')
    post.tags.add(tag)

    # Перевірка кількості постів
    assert Post.objects.count() == 1

    # Перевірка атрибутів поста
    assert post.user.username == 'test_user'
    assert post.tags.first().name == 'Django'

    # Перевірка атрибутів профілю
    assert user.profile.first_name == 'TestFirstName'

