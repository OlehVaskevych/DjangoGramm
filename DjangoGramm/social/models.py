from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Profile(models.Model):
    """
    Represents a user profile, containing personal information and an avatar.
    Each profile is associated with a User.
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", default=settings.DEFAULT_AVATAR_PATH)

    def __str__(self):
        return f"{self.first_name} {self.last_name}'s Profile"


class Post(models.Model):
    """
    Represents a post created by a user. Contains a title, description,
    and many-to-many relationships with likes and tags.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)  # Added title field
    description = models.TextField(blank=True)  # Added description field
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)  # Many-to-many relationship with tags

    def __str__(self):
        return f"Post titled '{self.title}' by {self.user.username}"


class Comment(models.Model):
    """
    Represents a comment on a post. Each comment is authored by a user
    and is associated with a specific post.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"


class Image(models.Model):
    """
    Represents an image uploaded for a specific post.
    Each image is associated with one post.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image_file = models.ImageField(upload_to="post_images/")

    def __str__(self):
        return f"Image for post '{self.post.title}'"


class Like(models.Model):
    """
    Represents a 'like' from a user on a specific post.
    A post can have many likes, and a user can like many posts.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'Like by {self.user.username} on post "{self.post.title}"'


class Tag(models.Model):
    """
    Represents a tag that can be associated with posts.
    Tags help to categorize and organize posts.
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
