import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from bs4 import BeautifulSoup

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

    soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')

    menu_items = soup.select('.navigation ul li')
    assert 'Стрічка постів' in response.content.decode()
    assert 'Профіль' not in response.content.decode()
    assert len(menu_items) == 2


@pytest.mark.django_db
# Test Home Page for logged-in users
def test_home_page_logged_in(client, user):
    client.login(username='testuser', password='password')
    response = client.get(reverse('home'))

    soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')

    menu_items = soup.select('.navigation ul li')

    assert response.status_code == 200
    assert 'Стрічка постів' in response.content.decode()
    assert len(menu_items) == 5


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


@pytest.mark.django_db
# Test if likes count increases for an authorized user
def test_likes_count_authorized_user(client, post, user):
    client.login(username='testuser', password='password')

    response = client.get(reverse('home'))
    assert 'Likes: 0' in response.content.decode()

    response = client.post(reverse('add_like', kwargs={'post_id': post.id}))
    assert response.status_code == 302
    assert response.url == reverse('home')

    response = client.get(reverse('home'))
    assert 'Likes: 1' in response.content.decode()


@pytest.mark.django_db
# Test if unauthorized user cannot like a post
def test_likes_count_unauthorized_user(client, post):
    response = client.get(reverse('home'))
    assert 'Likes: 0' in response.content.decode()

    response = client.post(reverse('add_like', kwargs={'post_id': post.id}))

    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
# Test comments for an authorized user
def test_comments_authorized_user(client, post, comment):
    client.login(username='testuser', password='password')

    # Ensure the initial comment is present
    response = client.get(reverse('home'))
    assert 'Great post!' in response.content.decode()

    # Post a new comment
    response = client.post(reverse('add_comment', kwargs={'post_id': post.id}), {'comment': 'Test comment!'})
    assert response.status_code == 302  # Should redirect after posting comment

    # Redirect should send us back to the post page (or home page if no specific post)
    assert response.url == reverse('home')  # Or replace 'home' with the appropriate post URL

    # Check that the new comment appears on the page
    response = client.get(reverse('home'))
    assert 'Test comment!' in response.content.decode()



@pytest.mark.django_db
# Test comments for an unauthorized user
def test_comments_unauthorized_user(client, post):
    # Try to post a comment without being logged in
    response = client.post(reverse('add_comment', kwargs={'post_id': post.id}), {'comment': 'Test comment!'})
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))
