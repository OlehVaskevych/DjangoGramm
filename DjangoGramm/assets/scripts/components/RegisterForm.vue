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
        <p>If you already have account <a href="/auth/login/">login here</a></p>
      </div>
    </form>
  </div>
</template>

<script>
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
        const response = await fetch(`/auth/register/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken'),
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