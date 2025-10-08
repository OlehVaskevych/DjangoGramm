import random
import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings

from DjangoGramm.social.models import Profile, Post, Image, Comment, Like, Tag


class Command(BaseCommand):
    help = 'Generate test data'

    def handle(self, *args, **options):
        User.objects.all().delete()
        Profile.objects.all().delete()
        Image.objects.all().delete()
        Comment.objects.all().delete()
        Like.objects.all().delete()
        Tag.objects.all().delete()

        tag1 = Tag.objects.create(name='Django')
        tag2 = Tag.objects.create(name='Python')
        tag3 = Tag.objects.create(name='Programming')
        tags = [tag1, tag2, tag3]

        image_folder = os.path.join(settings.MEDIA_ROOT, 'post_images')
        image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.png', '.jpeg'))]

        users = []
        posts = []
        for i in range(1, 11):
            user = User.objects.create_user(username=f'user{i}', password=f'password{i}')
            Profile.objects.create(
                user=user,
                first_name=f'First_name{i}',
                last_name=f'Last_name{i}',
                bio=f'This is the bio of user {i}.'
            )
            users.append(user)

            num_posts = random.randint(1, 5)
            for j in range(num_posts):
                post = Post.objects.create(
                    user=user,
                    title=f'Post {j + 1} by {user.username}',
                    description=f'This is a description for post {j + 1} by {user.username}.',
                )
                posts.append(post)
                # Додати випадкові теги до кожного поста
                post.tags.add(*random.sample(tags, k=random.randint(1, 3)))

                num_images = random.randint(1, min(3, 10))  # Ensure it's no more than 10
                for _ in range(num_images):
                    image_file = random.choice(image_files)
                    Image.objects.create(
                        post=post,
                        image_file=f'post_images/{image_file}',
                    )

        for post in posts:
            commenters = [user for user in users if user.username != post.user.username]
            num_comments = random.randint(1, 5)
            for _ in range(num_comments):
                commenter = random.choice(commenters)
                Comment.objects.create(
                    post=post,
                    author=commenter,
                    text=f'This is a comment by {commenter.username}.'
                )

            # Додати випадкову кількість лайків від різних користувачів, крім автора поста
            likers = [user for user in users if user.username != post.user.username]
            num_likes = random.randint(1, len(users))
            for _ in range(num_likes):
                liker = random.choice(likers)
                post.likes.add(liker)

        self.stdout.write(self.style.SUCCESS("10 users with profiles and random posts generated successfully."))

