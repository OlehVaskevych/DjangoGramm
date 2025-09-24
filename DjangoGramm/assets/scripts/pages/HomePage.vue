<template>
  <div>
    <PostCard
      v-for="post in posts"
      :key="post.id"
      :post="post"
      :currentUser="currentUser"
      :userIsAuthenticated="userIsAuthenticated"
    />

    <div v-if="loading" class="text-center my-3">
      Loading...
    </div>
  </div>
</template>

<script>
import PostCard from '../components/PostCard.vue';

export default {
  components: { PostCard },
  data() {
    return {
      posts: [],
      page: 1,
      limit: 10,
      loading: false,
      hasNext: true,
      currentUser: window.currentUser, // якщо передаєш з бекенду
      userIsAuthenticated: window.userIsAuthenticated,
    };
  },
  methods: {
    async loadPosts() {
      if (this.loading || !this.hasNext) return;
      this.loading = true;
      try {
        const res = await fetch(`/api/posts/?page=${this.page}&limit=${this.limit}`);
        const data = await res.json();

        this.posts.push(...data.posts);
        this.hasNext = data.has_next;
        this.page += 1;
      } catch (err) {
        console.error("Failed to load posts:", err);
      } finally {
        this.loading = false;
      }
    },
    handleScroll() {
      const bottom = window.innerHeight + window.scrollY >= document.body.offsetHeight - 300;
      if (bottom) {
        this.loadPosts();
      }
    }
  },
  mounted() {
    this.loadPosts();
    window.addEventListener("scroll", this.handleScroll);
  },
  beforeUnmount() {
    window.removeEventListener("scroll", this.handleScroll);
  }
};
</script>
