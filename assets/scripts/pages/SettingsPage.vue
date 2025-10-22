<template>
  <div class="settings-container">
    <h1 class="settings-title">Settings</h1>

    <div v-if="user" class="d-grid gap-2 styled-form">
      <router-link
        :to="'/profile/' + user.username + '/update/'"
        class="btn custom-button">
        Edit Profile
        <span class="fa fa-edit"></span>
      </router-link>

      <router-link
        to="/auth/logout/"
        class="btn custom-button">
        Logout
        <span class="fa fa-sign-out"></span>
      </router-link>
    </div>

    <div v-else class="text-center mt-3">
      Loading...
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      user: null,
    };
  },
  async mounted() {
    try {
      const res = await fetch("/api/current-user/");
      if (res.ok) {
        this.user = await res.json();
      } else if (res.status === 403) {
        console.warn("Not logged in");
      }
    } catch (err) {
      console.error("Failed to load current user:", err);
    }
  },
};
</script>
