<template>
  <div id="app">
    <NavigationBar
      :isAuthenticated="isAuthenticated"
      :currentPath="currentPath"
      :username="username"
    />
    <!-- Added main wrapper with padding for fixed bottom nav -->
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script>
import NavigationBar from './components/NavigationBar.vue';

export default {
  name: 'App',
  props: {
    isAuthenticated: Boolean,
    currentPath: String,
    username: String,
  },
  components: { NavigationBar }
}
</script>

<style lang="scss">
</style>
