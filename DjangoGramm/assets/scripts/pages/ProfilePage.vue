<template>
  <div class="container mt-5">
    <div class="header">
      <div class="avatar-container">
        <img :src="profile.avatar" :alt="`${user.username}'s Avatar`" class="img-fluid rounded-circle" />
      </div>

      <div class="profile-main-info">
        <div class="username-and-actions">
          <h2 class="username">{{ user.username }}</h2>
          <div class="actions">
            <router-link
                v-if="isOwner"
                :to="'/profile/' + user.username + '/update/'"
                class="btn btn-warning btn-sm">
              Edit Profile
            </router-link>
            <button
              v-else
              @click="toggleFollow"
              :class="isFollowing ? 'btn btn-danger btn-sm' : 'btn btn-success btn-sm'"
            >
              {{ isFollowing ? 'Unfollow' : 'Follow' }}
            </button>
          </div>
        </div>

        <div class="stats">
          <div>
            <h3>{{ posts.length }}</h3>
            <span>Posts</span>
          </div>

          <div>
            <h3>{{ followers }}</h3>
            <span>Followers</span>
          </div>

          <div>
            <h3>{{ followings }}</h3>
            <span>Following</span>
          </div>
        </div>
      </div>

      <section id="posts">
        <h2 class="mb-3">Posts</h2>
        <div v-if="posts.length" class="posts-grid">
          <div v-for="post in posts" :key="post.id" class="post-item">
            <router-link :to="`/posts/${post.id}`">
              <img
                  v-if="post.images.length > 0"
                  :src="post.images[0].image_file"
                  class="post-image"
                  alt=""
              />
              <div class="post-overlay">
                <span>
                  {{ post.likes.length }}
                  <i :class="post.likes.includes(user.id) ? 'fa-solid fa-heart' : 'fa-regular fa-heart'"></i>
                  •
                  {{ post.comments.length }}
                  <i class="fa-regular fa-comment"></i>
                </span>
              </div>
            </router-link>
          </div>
        </div>
        <h4 v-else>No posts yet.</h4>
      </section>
    </div>
  </div>
</template>

<script>
import { useRoute } from 'vue-router'; // 💡 useRoute використовується для доступу до поточного маршруту
import { getCookie } from '../csrf.js';

export default {
  // Використовуємо Vue 3 setup() для отримання useRoute, або робимо це у beforeMount/created,
  // але для простоти і сумісності з Vue 3 Options API ми використаємо його у mounted.
  //
  // Якщо ви використовуєте Vue 2, вам потрібно буде отримати маршрут через this.$route
  // Якщо ви використовуєте Vue 3, ми можемо отримати його в created/mounted.

  data() {
    return {
      user: {},
      profile: {},
      posts: [],
      followers: 0,
      followings: 0,
      isFollowing: false,
      currentUser: null,
      username: '' // Зберігаємо username з маршруту в data
    };
  },

  computed: {
    isOwner() {
      // Порівнюємо username поточного користувача з username власника профілю
      return this.currentUser?.username === this.user?.username;
    }
  },

  methods: {
    async toggleFollow() {
      try {
        const res = await fetch(`/profile/${this.username}/follows/`, {
          method: "POST",
          credentials: "include",
          headers: {
            "X-CSRFToken": getCookie('csrftoken'),
          }
        })
        const data = await res.json()
        if (data.status === 'success') {
          this.followers = this.followers + 1;
          this.isFollowing = !this.isFollowing;
          console.log(data);
        }
        else {
          console.warn("You can Follow to this user!")
        }
      } catch (err) {
        console.error("Error while try to follow: ", err);
      }
    },

    async loadProfileData() {
      const route = useRoute(); // Отримуємо доступ до об'єкта маршруту
      this.username = route.params.username;

      try {
        const res = await fetch(`/api/profile/${this.username}/`);
        const data = await res.json();

        // Оновлюємо стан
        this.user = data.user;
        this.profile = data.profile;
        this.posts = data.posts;
        this.followers = data.followers;
        this.followings = data.followings;
        this.isFollowing = data.is_following;
        this.currentUser = window.currentUser; // Об'єкт поточного користувача
      } catch (err) {
        console.error('Failed to load profile: ', err);
      }
    }
  },

  mounted() {
    // 💡 Викликаємо завантаження даних при монтуванні
    this.loadProfileData();
  }
};
</script>