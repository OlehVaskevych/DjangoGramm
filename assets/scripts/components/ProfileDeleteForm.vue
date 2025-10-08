<template>
  <form @submit.prevent="deleteProfileConfirmation" enctype="multipart/form-data" class="delete-form">
    <button type="submit" class="btn btn-outline-danger btn-form" :disabled="isSubmitting">
      <span v-if="!isSubmitting">Delete profile</span>
        <span v-else class="spinner-border" role="status">
          <span class="sr-only">Loading...</span>
        </span>
    </button>
  </form>
</template>

<script>
  export default {
    data () {
      return {
        userId: initialData.id,
        username: initialData.username,
        isSubmitting: false,
      };
    },
    methods: {
      async submitForm() {
        this.isSubmitting = true;

        const formData = new FormData();
        formData.append('_method', 'DELETE');

        const url = `/api/profile/${this.username}/update`;

        try {
          const response = await fetch(url, {
            method: 'POST',
            headers: {
              'X-CSRFToken': this.getCookie('csrftoken'),
            },
            body: formData,
          });

          const data = await response.json();

          if (response.ok) {
            window.location.href = data.redirect_url;
          }
        } catch (error) {
          console.error('Error submitting form:', error);
        } finally {
          this.isSubmitting = false;
        }
      },

      deleteProfileConfirmation() {
        const isConfirmed = window.confirm('Are you sure want delete your profile?');
        if (isConfirmed) {
          this.submitForm();
        }
      },

      getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
          const cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + '=') {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
            }
          }
        }
        return cookieValue;
      },
    },
  };
</script>