  <template>
    <nav class="navigation">
      <ul>
        <li
          v-for="item in navItems"
          :key="item.name"
          :class="{ active: isActive(item) }"
          @click="setActive(item)"
        >
          <router-link :to="item.url">
            <span class="icon">
              <i :class="item.icon"></i>
            </span>
            <span class="text">{{ item.label }}</span>
          </router-link>
        </li>
        <div class="indicator"></div>
      </ul>
    </nav>
  </template>

  <script>
  export default {
    name: "Navigationbar",
    props: {
      isAuthenticated: {
        type: Boolean,
        default: false,
      },
      currentPath: {
        type: String,
        required: true,
      },
      username: {
        type: String,
        default: "",
      },
    },
    data() {
      return {
        activeItem: null,
      };
    },
    computed: {
      navItems() {
        if (this.isAuthenticated) {
          return [
            { name: "main", url: "/", label: "Home", icon: "fa-solid fa-house" },
            { name: "profile", url: `/profile/${this.username}/`, label: "Profile", icon: "fa-solid fa-user" },
            { name: "news", url: `/news/`, label: "News", icon: "fa-solid fa-newspaper" },
            { name: "post", url: `/post/`, label: "Create post", icon: "fa-solid fa-plus" },
            { name: "settings", url: `/settings/`, label: "Settings", icon: "fa-solid fa-gear" },
          ];
        }
        return [
          { name: "main", url: "/", label: "Home", icon: "fa-solid fa-house" },
          { name: "login", url: "/auth/login/", label: "Sign in", icon: "fa-solid fa-sign-in" },
        ];
      },
    },
    methods: {
      isActive(item) {
        if (this.activeItem) {
          return this.activeItem === item.name;
        }
        return this.currentPath.startsWith(item.url);
      },
      setActive(item) {
        this.activeItem = item.name;
      },
    },
  };
  </script>