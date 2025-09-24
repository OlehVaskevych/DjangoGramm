<template>
  <div class="settings-container">
      <h1 class="settings-title">Settings</h1>

      <div class="d-grid gap-2">
          <a href="{% url 'profile_update' user.username %}" class="btn custom-button me-5 ms-5">
                  Edit Profile
                  <span class="fa fa-edit"></span>
          </a>
          <a href="{% url 'logout' %}" class="btn custom-button me-5 ms-5">
                  Logout
                  <span class="fa fa-sign-out"></span>
          </a>
      </div>
  </div>
</template>

<style scoped>

</style>