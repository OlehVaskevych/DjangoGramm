"""
Django models for the social network application.

This module defines the core data models including User profiles, Posts,
Comments, Images, Likes, Tags, and Follow relationships.
"""

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Profile(models.Model):
    """
    User profile model containing personal information and avatar.

    Each profile is linked to a Django User via a one-to-one relationship.
    Stores additional user information like name, bio, and profile picture.

    :param first_name: User's first name
    :type first_name: str
    :param last_name: User's last name
    :type last_name: str
    :param user: Associated Django User instance
    :type user: User
    :param bio: User's biography/description
    :type bio: str
    :param avatar: Profile picture image file
    :type avatar: ImageField
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", default=settings.DEFAULT_AVATAR_PATH)

    def __str__(self):
        """
        String representation of the Profile.

        :return: Formatted string with user's full name
        :rtype: str
        """
        return f"{self.first_name} {self.last_name}'s Profile"


class Post(models.Model):
    """
    Post model representing user-generated content.

    Contains post content (title and description), metadata (creation time),
    and relationships with users (author, likes) and tags.

    :param user: Post author
    :type user: User
    :param title: Post title
    :type title: str
    :param description: Post content/description
    :type description: str
    :param likes: Users who liked this post
    :type likes: ManyToManyField
    :param created_at: Timestamp when post was created
    :type created_at: datetime
    :param tags: Tags associated with this post
    :type tags: ManyToManyField
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)

    def __str__(self):
        """
        String representation of the Post.

        :return: Formatted string with post title and author
        :rtype: str
        """
        return f"Post titled '{self.title}' by {self.user.username}"


class Comment(models.Model):
    """
    Comment model for user comments on posts.

    Represents a comment made by a user on a specific post.
    Includes the comment text, author, and creation timestamp.

    :param post: Post this comment belongs to
    :type post: Post
    :param author: User who wrote the comment
    :type author: User
    :param text: Comment content
    :type text: str
    :param created_at: Timestamp when comment was created
    :type created_at: datetime
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String representation of the Comment.

        :return: Formatted string with author and post title
        :rtype: str
        """
        return f"Comment by {self.author.username} on {self.post.title}"


class Image(models.Model):
    """
    Image model for post attachments.

    Represents an image file uploaded and attached to a post.
    Multiple images can be associated with a single post.

    :param post: Post this image belongs to
    :type post: Post
    :param image_file: Uploaded image file
    :type image_file: ImageField
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image_file = models.ImageField(upload_to="post_images/")

    def __str__(self):
        """
        String representation of the Image.

        :return: Formatted string with associated post title
        :rtype: str
        """
        return f"Image for post '{self.post.title}'"


class Like(models.Model):
    """
    Like model representing user likes on posts.

    Tracks which users have liked which posts. Creates a many-to-many
    relationship between users and posts through explicit model.

    :param user: User who liked the post
    :type user: User
    :param post: Post that was liked
    :type post: Post
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        """
        String representation of the Like.

        :return: Formatted string with user and post title
        :rtype: str
        """
        return f'Like by {self.user.username} on post "{self.post.title}"'


class Tag(models.Model):
    """
    Tag model for categorizing posts.

    Represents a hashtag or category that can be associated with posts.
    Tags help organize and filter content.

    :param name: Tag name (unique)
    :type name: str
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        """
        String representation of the Tag.

        :return: Tag name
        :rtype: str
        """
        return self.name


class Follow(models.Model):
    """
    Follow model representing user follow relationships.

    Creates a many-to-many relationship between users where one user
    (follower) follows another user (following). Ensures unique
    follow relationships through Meta.unique_together.

    :param follower: User who is following
    :type follower: User
    :param following: User being followed
    :type following: User
    """
    follower = models.ForeignKey(User, related_name='followings', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        """
        Meta options for Follow model.

        Ensures that a user cannot follow the same user multiple times.
        """
        unique_together = (('follower', 'following'),)

    def __str__(self):
        """
        String representation of the Follow relationship.

        :return: Formatted string showing follower and following usernames
        :rtype: str
        """
        return f"{self.follower.username} follows {self.following.username}"
