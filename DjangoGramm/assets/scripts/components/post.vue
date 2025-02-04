<template>
    <div v-if="posts.length">
        <div v-for="post in posts" :key="post.id" class="card mt-3 card-color">
            <div class="card-header d-flex align-items-center mt-2 mb-2">
                <img :src="post.user.profile.avatar.url" alt="Avatar" class="card-header-image">
                <a :href="'/profile/' + post.user.username" class="text-decoration-none user-href">
                    <span class="ms-3 fw-bolder fs-4">{{ post.user.username }}</span>
                </a>

                <a v-if=" userIsAuthenticated && post.user.username === currentUser.username" :href="'/post/' + post.id + '/update'" class="edit-icon">
                    <span class="fa fa-edit"></span>
                </a>
            </div>
            <div v-if="post.images.length" class="carousel slide">
                <div class="carousel-inner">
                    <div v-for="(image, index) in post.images" :key="image.id" :class="{'carousel-item': true, 'active': index === 0}">
                        <img :src="image.image_file.url" class="card-img-top" alt="Post image">
                    </div>
                </div>
                <button v-if="post.images.length > 1" class="carousel-control-prev" type="button" :data-bs-target="'#carousel-' + post.id" data-bs-slide="prev">
                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Previous</span>
                </button>
                <button v-if="post.images.length > 1" class="carousel-control-next" type="button" :data-bs-target="'#carousel-' + post.id" data-bs-slide="next">
                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Next</span>
                </button>
            </div>

            <div class="card-body">
                <h3 class="card-title card-text-color">{{ post.title }}</h3>
                <p class="card-text card-text-color">{{ post.description }}</p>
                <p class="card-muted-text-color">Likes: {{ post.likes.count }}</p>

                <div class="like-comment-container">
                    <LikeAddForm
                        v-if="userIsAuthenticated"
                        :postId="post.id"
                        :isLiked="post.likes.all.some(like => like.username === currentUser.username)"
                        @like-updated="updateLikes(post.id, $event)"
                    />
                    <a v-else :href="'/auth/login/'" class="custom-btn-like">
                        <i style="font-size:24px" class="fa-regular fa-heart"></i>
                    </a>

                    <button @click="toggleComments(post.id)" class="custom-btn-comment">
                        <i style="font-size:24px" class="fa-regular fa-comment"></i>
                    </button>
                </div>

                <div class="mt-3 ms-2 me-2" :id="'comments-' + post.id" style="display: none">
                    <h5 class="card-title card-text-color">Comments</h5>
                    <ul class="list-group">
                        <li v-for="comment in post.comments" :key="comment.id" class="list-group-item card-color comment-text">
                            <strong class="card-title">{{ comment.author.username }}:</strong> {{ comment.text }}
                            <br>
                            <small class="card-muted-text-color">{{ comment.created_at }}</small>
                            <p>comment - {{ comment.id }} post - {{ post.id }}</p>
                            <CommentDeleteForm
                              v-if="comment.id && post.id && comment.author.username === currentUser.username"
                              class="comment-delete-container"
                              :post-id="Number(post.id)"
                              :comment-id="Number(comment.id)"
                              @delete-comment="updateComments(post.id, 'delete', $event)"
                            />
                        </li>
                    </ul>
                    <CommentSendForm
                        :is-authenticated="userIsAuthenticated"
                        :post-id="post.id"
                        @add-comment="updateComments(post.id, 'send', $event)"
                    />
                </div>
            </div>
        </div>
    </div>
    <div v-else class="alert alert-warning text-center" role="alert">
        No posts yet.
    </div>
</template>

<script>
import LikeAddForm from './LikeAddForm.vue'
import CommentSendForm from "./CommentSendForm.vue";
import CommentDeleteForm from "./CommentDeleteForm.vue";

export default {
    data() {
        console.log('Posts:', posts);
        return {
            posts,
            currentUser: currentUser,
            userIsAuthenticated,
        };
    },
    components: {
      LikeAddForm,
      CommentSendForm,
      CommentDeleteForm
    },
    methods: {
        toggleComments(postId) {
            const commentsSection = document.getElementById('comments-' + postId);
            if (commentsSection) {
                commentsSection.style.display = commentsSection.style.display === 'none' ? 'block' : 'none';
            } else {
                console.error('Comments section not found for post', postId);
            }
        },

        // Update the like count and likes array when the like is toggled
        updateLikes(postId, newLikes) {
            const post = this.posts.find(p => p.id === postId);
            if (post) {
                post.likes.count = newLikes;
            }
        },

        updateComments(postId, action, comment) {
            const post = this.posts.find(post => post.id === postId);
            if (post) {
                if (action === 'send') {
                    post.comments.push(comment);
                } else if (action === 'delete') {
                    const index = post.comments.findIndex(comment => comment.id === comment.id);
                    console.log(comment);
                    if (index !== -1) {
                        post.comments.splice(index, 1);
                    }
                }
            }
        }
    }
}
</script>
