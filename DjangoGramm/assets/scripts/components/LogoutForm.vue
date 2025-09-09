<template>
  <div class="form-container">
    <h1 class="form-title">Confirm Logout?</h1>
    <form @submit.prevent="submitForm" class="styled-form">
      <div class="button-container">
        <button class="submit-button" type="submit">Confirm</button>
        <button class="submit-button" type="button" @click="goBack">Cancel</button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  methods: {
    async submitForm() {
      try {
        const response = await fetch(`/auth/logout/`, {
            method: 'POST',
            headers: {
              'X-CSRFToken': this.getCookie('csrftoken'),
            },
        });

        const data = await response.json()
        console.log(data);

        if (response.ok) {
          window.location.href = data.redirect_url;
        } else {
            if (data.status === 'error') {
              this.errorMessage = data.error_message || 'An error occurred while saving changes.';
              if (data.errors) {
                this.updateFieldErrors(data.errors);
              }
            }
          }
      } catch (error) {
        console.error('Error submitting form:', error);
        this.errorMessage = 'An unexpected error occurred. Please try again.';
      } finally {
        this.isSubmitting = false;
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
    goBack() {
      window.history.back();
    },
  },
};
</script>