<template>
  <div v-if="post">
    <div class="card mt-3 card-color">
      <div class="card-header d-flex align-items-center mt-2 mb-2">
        <img :src="post.user.profile.avatar.url" alt="Avatar" class="card-header-image">
        <router-link
          :to="'/profile/' + post.user.username"
          class="text-decoration-none user-href"
        >
          <span class="ms-3 fw-bolder fs-4">{{ post.user.username }}</span>
        </router-link>

        <router-link
          :to="'/post/' + post.id + '/update/'"
          class="edit-icon"
        >
          <span class="fa fa-edit"></span>
        </router-link>
      </div>

      <div v-if="post.images.length" :id="'carousel-' + post.id" class="carousel slide">
        <div class="carousel-inner">
          <div v-for="(image, index) in post.images" :key="index" :class="{'carousel-item': true, 'active': index === 0}">
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
            @like-updated="updateLikes($event)"
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
              <p></p>
              <CommentDeleteForm
                v-if="comment.id && currentUser && comment.author.username === currentUser.username"
                class="comment-delete-container"
                :post-id="post.id"
                :comment-id="comment.id"
                @delete-comment="updateComments('delete', $event)"
              />
            </li>
          </ul>
          <CommentSendForm
            :is-authenticated="userIsAuthenticated"
            :post-id="post.id"
            @add-comment="updateComments('send', $event)"
          />
        </div>
      </div>
    </div>
  </div>
  <div v-else class="alert alert-warning text-center">Post not found.</div>
</template>

<script>
import LikeAddForm from '../components/LikeAddForm.vue';
import CommentSendForm from "../components/CommentSendForm.vue";
import CommentDeleteForm from "../components/CommentDeleteForm.vue";

export default {
  data() {
    return {
      post: null,
      currentUser: null,
      userIsAuthenticated: false
    };
  },
  components: {LikeAddForm, CommentSendForm, CommentDeleteForm},
  methods: {
    toggleComments(postId) {
      const section = document.getElementById('comments-' + postId);
      if (section) section.style.display = section.style.display === 'none' ? 'block' : 'none';
    },
    updateLikes(newLikes) {
      if (this.post) this.post.likes.count = newLikes;
    },
    updateComments(action, comment) {
      if (!this.post) return;
      if (action === 'send') this.post.comments.push(comment);
      if (action === 'delete') {
        const i = this.post.comments.findIndex(c => c.id === comment.id);
        if (i !== -1) this.post.comments.splice(i, 1);
      }
    }
  },
  async mounted() {
    try {
      const postId = this.$route.params.id;
      const res = await fetch(`/api/post/${postId}/`);
      const data = await res.json();
      this.post = data.post;
      this.currentUser = data.currentUser;
      this.userIsAuthenticated = data.userIsAuthenticated;
    } catch (err) {
      console.error('Failed to load post:', err);
    }
  }
};
</script>
