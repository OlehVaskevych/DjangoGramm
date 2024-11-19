import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from social.models import Post, Comment, Like


@pytest.fixture
def user():
    return get_user_model().objects.create_user(username='testuser', password='password')


@pytest.fixture
def post(user):
    return Post.objects.create(title="Post 1", description="Description for post 1", user=user)


@pytest.fixture
def comment(user, post):
    return Comment.objects.create(post=post, author=user, text="Great post!")


@pytest.fixture
def like(user, post):
    return Like.objects.create(post=post, user=user)


@pytest.mark.django_db
# Test Home Page for logged-out users
def test_home_page_logged_out(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert 'Стрічка постів' in response.content.decode()
    assert 'Профіль' not in response.content.decode()


@pytest.mark.django_db
# Test Home Page for logged-in users
def test_home_page_logged_in(client, user):
    client.login(username='testuser', password='password')
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert 'Стрічка постів' in response.content.decode()
    assert 'Профіль' in response.content.decode()


@pytest.mark.django_db
# Test if posts are rendered on the home page
def test_posts_rendered(client, post):
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert "Post 1" in response.content.decode()
    assert "Description for post 1" in response.content.decode()


@pytest.mark.django_db
# Test if likes count is rendered correctly
def test_likes_count(client, post, like):
    response = client.get(reverse('home'))
    assert 'Likes: 0' in response.content.decode()


@pytest.mark.django_db
# Test comments section for a post
def test_comments_section(client, post, comment):
    response = client.get(reverse('home'))
    assert 'Great post!' in response.content.decode()


@pytest.mark.django_db
# Test "No comments" message if there are no comments
def test_no_comments_message(client, user):
    post_no_comments = Post.objects.create(title="Post with no comments", description="No comments post", user=user)
    response = client.get(reverse('home'))
    assert 'Немає коментарів' in response.content.decode()
