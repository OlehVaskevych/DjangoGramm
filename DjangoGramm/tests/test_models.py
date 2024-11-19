import pytest
from django.contrib.auth.models import User

from social.models import Profile, Post, Image, Like, Tag


@pytest.mark.django_db
def test_create_user_and_post():
    user = User.objects.create_user(username='test_user', password='test_password1')

    profile = Profile.objects.create(user=user, first_name='Test', last_name='User', bio='This is a bio.')

    tag = Tag.objects.create(name='Django')

    post = Post.objects.create(user=user, title='Test', description='This is a test.')
    post.tags.add(tag)

    assert Post.objects.count() == 1
    assert post.user.username == 'test_user'
    assert post.tags.first().name == 'Django'
    assert profile.user.username == 'test_user'
    assert profile.first_name == 'Test'
