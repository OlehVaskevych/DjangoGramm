<template>
  <div>
    <PostDetail
      v-for="post in posts"
      :key="post.id"
      :post="post"
      :currentUser="currentUser"
      :userIsAuthenticated="userIsAuthenticated"
      @update-post="handlePostUpdate"
      @update-post-comments="handleCommentsUpdate"
    />

    <div v-if="loading" class="text-center my-3">
      Loading...
    </div>

    <div v-if="!loading && posts.length === 0" class="text-center mt-5">
      <p>No news yet. Follow users to see their posts.</p>
    </div>
  </div>
</template>

<script>
import PostDetail from '../components/PostDetail.vue';

export default {
  components: { PostDetail },
  data() {
    return {
      posts: [],
      page: 1,
      limit: 10,
      loading: false,
      hasNext: true,
      currentUser: window.currentUser,
      userIsAuthenticated: window.userIsAuthenticated,
    };
  },
  methods: {
    async loadPosts() {
      if (this.loading || !this.hasNext) return;
      this.loading = true;
      try {
        // 🔹 Головна відмінність від HomePage.vue:
        const res = await fetch(`/api/posts/?page=${this.page}&limit=${this.limit}&feed=news`);
        const { data } = await res.json();

        this.posts.push(...data.posts);
        this.hasNext = data.has_next;
        this.page += 1;
      } catch (err) {
        console.error("Failed to load news feed:", err);
      } finally {
        this.loading = false;
      }
    },

    handleScroll() {
      const bottom = window.innerHeight + window.scrollY >= document.body.offsetHeight - 300;
      if (bottom) {
        this.loadPosts();
      }
    },

    handlePostUpdate(update) {
      const postIndex = this.posts.findIndex(p => p.id === update.id);
      if (postIndex !== -1) {
        if (update.field === 'likes.count') {
          this.posts[postIndex].likes.count = update.value;
        }
      }
    },

    handleCommentsUpdate(update) {
      const postIndex = this.posts.findIndex(p => p.id === update.id);
      if (postIndex !== -1) {
        const post = this.posts[postIndex];

        if (update.action === 'send') {
          post.comments.push(update.comment);
        } else if (update.action === 'delete') {
          const index = post.comments.findIndex(c => c.id === update.comment.id);
          if (index !== -1) post.comments.splice(index, 1);
        }
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
