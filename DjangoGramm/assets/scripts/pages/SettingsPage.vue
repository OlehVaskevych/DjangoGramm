<template>
  <div class="settings-container">
      <h1 class="settings-title">Settings</h1>

      <div class="d-grid gap-2 styled-form">
          <a href="{% url 'profile_update' user.username %}" class="btn custom-button">
                  Edit Profile
                  <span class="fa fa-edit"></span>
          </a>
          <router-link
            to="/auth/logout/"
            class="btn custom-button"
          >
            Logout
            <span class="fa fa-sign-out"></span>
          </router-link>
      </div>
  </div>
</template>

<style scoped>

</style>

<script setup lang="ts">

</script>