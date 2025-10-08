<template>
  <div class="form-container">
    <h1 class="form-title">Реєстрація</h1>
    <form @submit.prevent="submitForm" enctype="multipart/form-data" class="styled-form">
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
      <div class="form-group" v-for="field in fields" :key="field.id">
        <label :for="field.id">{{ field.label }}</label>
        <input
          :id="field.id"
          v-model="field.value"
          :type="field.attrs.type"
          :name="field.name"
          :required="field.attrs.required"
        >
        <small v-if="field.helpText" class="form-text">{{ field.helpText }}</small>
        <p v-for="error in field.errors" :key="error" class="form-error">
          {{ error }}
        </p>
      </div>
      <div class="button-container">
        <button type="submit" class="submit-button btn-form" :disabled="isSubmitting">
          <span v-if="!isSubmitting">Register</span>
          <span v-else class="spiner-border" role="status">
            <span class="sr-only">Loading...</span>
          </span>
        </button>

        <!-- Social Login Section -->
        <div class="social-login">
          <button @click="redirectToOAuth('google')" type="button" class="gsi-material-button">
            <div class="gsi-material-button-content-wrapper">
              <div class="gsi-material-button-icon">
                <svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" xmlns:xlink="http://www.w3.org/1999/xlink" style="display: block;">
                  <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"></path>
                  <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"></path>
                  <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"></path>
                  <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"></path>
                  <path fill="none" d="M0 0h48v48H0z"></path>
                </svg>
              </div>
            </div>
          </button>
          <button @click="redirectToOAuth('github')" type="button" class="gsi-material-button github-button">
            <div class="gsi-material-button-content-wrapper">
              <div class="gsi-material-button-icon">
                <svg viewBox="0 0 24 24" class="github-icon">
                  <path fill="currentColor" d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.44 9.8 8.21 11.39.6.11.82-.26.82-.58 0-.29-.01-1.26-.02-2.28-3.34.72-4.05-1.61-4.05-1.61-.54-1.36-1.32-1.72-1.32-1.72-1.08-.74.08-.73.08-.73 1.2.08 1.83 1.23 1.83 1.23 1.06 1.81 2.79 1.29 3.47.99.11-.77.42-1.29.76-1.58-2.67-.3-5.47-1.34-5.47-5.96 0-1.32.47-2.39 1.23-3.23-.12-.3-.54-1.52.12-3.16 0 0 1.01-.32 3.3 1.23.96-.27 1.98-.41 3-.41s2.04.14 3 .41c2.29-1.55 3.3-1.23 3.3-1.23.66 1.64.24 2.86.12 3.16.76.84 1.23 1.91 1.23 3.23 0 4.63-2.81 5.65-5.49 5.96.43.37.81 1.1.81 2.22 0 1.6-.01 2.89-.01 3.28 0 .32.22.7.83.58C20.56 21.8 24 17.3 24 12 24 5.37 18.63 0 12 0z"/>
                </svg>
              </div>
            </div>
          </button>
        </div>

        <p>If you already have account <router-link to="/auth/login/">login here</router-link></p>
      </div>
    </form>
  </div>
</template>

<script>
import { getCookie } from '../csrf.js';

export default {
  data() {
    return {
      fields: [
        { id: 'id_username', label: 'Username:', name: 'username', value: '', attrs: { type: 'text', required: true }, errors: [], helpText: 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.' },
        { id: 'id_password1', label: 'Password:', name: 'password1', value: '', attrs: { type: 'password', required: true }, errors: [] },
        { id: 'id_password2', label: 'Password Confirmation:', name: 'password2', value: '', attrs: { type: 'password', required: true }, errors: [], helpText: 'Enter the same password as before, for verification.\n'  },
      ],
      errorMessage: '',
      isSubmitting: false
    };
  },
  methods: {
    async submitForm() {
      this.isSubmitting = true;
      this.clearErrors();

      const formData = new FormData();
      this.fields.forEach((field) => {
        formData.append(field.name, field.value);
      });

      try {
        const response = await fetch(`/api/auth/register/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': getCookie('csrftoken'),
          },
          body: formData,
        });

        const data = await response.json();

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
    clearErrors() {
      this.errorMessage = '';
      this.fields.forEach((field) => {
        field.errors = [];
      });
    },
    updateFieldErrors(errors) {
      Object.entries(errors).forEach(([fieldName, fieldErrors]) => {
        const field = this.fields.find(f => f.id === fieldName);
        if (field) {
          field.errors = Array.isArray(fieldErrors) ? fieldErrors : [fieldErrors];
        }
      });
    },
    redirectToOAuth(provider) {
      if (window.oauthUrls[provider]) {
        window.location.href = window.oauthUrls[provider];
      } else {
        console.error("Unknown OAuth provider");
      }
    },
  },
};
</script>