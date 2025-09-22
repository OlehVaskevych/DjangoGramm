<template>
  <div>
    <NavigationBar
      :isAuthenticated="isAuthenticated"
      :currentPath="currentPath"
      :username="username"
    />
    <router-view />
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