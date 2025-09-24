<template>
  <div class="container mt-5">
    <div class="header">
      <!--   Avatar   -->
      <div class="avatar-container">
        <img :src="profile.avatar" :alt="`${user.username}'s Avatar`" class="img-fluid rounded-circle" />
      </div>

      <!--   Main Info   -->
      <div class="profile-main-info">
        <div class="username-and-actions">
          <h2 class="username">{{ user.username }}</h2>
          <div class="actions">
            <button
              v-if="isOwner"
              @click="$emit('edit-profile', user.username)"
              class="btn btn-warning btn-sm"
            >
              Edit Profile
            </button>
            <button
              v-else
              @click="toogleFollow"
              :class="isFollowing ? 'btn btn-danger btn-sm' : 'btn btn-success btn-sm'"
            >
              {{ isFollowing ? 'Unfollow' : 'Follow' }}
            </button>
          </div>
        </div>

        <!--    Stats    `-->
        <div class="stats">
          <div>
            <h3>{{ posts.length }}</h3>
            <span>Posts</span>
          </div>

          <div>
            <h3>{{ followers }}</h3>
            <span>Posts</span>
          </div>

          <div>
            <h3>{{ followings }}</h3>
            <span>Posts</span>
          </div>
        </div>
      </div>

      <!--   Profile Info   -->
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

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'

// Route params
const route = useRoute()
const username = route.params.username

// State
const user = ref({})
const profile = ref({})
const posts = ref([])
const followers = ref(0)
const followings = ref(0)
const isFollowing = ref(false)
const currentUser = ref(null)

// Computed
const isOwner = computed(() => currentUser.value?.username === user.value?.username)

// Methods
function toggleFollow() {
  isFollowing.value = !isFollowing.value
}

// Load profile data
onMounted(async () => {
  try {
    const res = await fetch(`/api/profile/${username}/`)
    const data = await res.json()

    user.value = data.user
    profile.value = data.profile
    posts.value = data.posts
    followers.value = data.followers
    followings.value = data.followings
    isFollowing.value = data.is_following
    currentUser.value = data.current_user
  } catch (err) {
    console.error('Failed to load profile: ', err)
  }
})
</script>