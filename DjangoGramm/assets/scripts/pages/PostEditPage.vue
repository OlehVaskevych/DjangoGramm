<template>
  <div class="form-container">
    <h1 class="form-title">Post Edit</h1>

    <form @submit.prevent="submitForm('PUT')" enctype="multipart/form-data" class="styled-form">
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <div class="form-group" v-for="field in fields" :key="field.id">
        <label :for="field.id">{{ field.label }}</label>
        <input
          :id="field.id"
          v-model="field.value"
          :type="field.attrs.type"
          :name="field.id"
          :required="field.attrs.required"
        >
        <small v-if="field.helpText" class="form-text">{{ field.helpText }}</small>
        <p v-for="error in field.errors" :key="error" class="form-error">{{ error }}</p>
      </div>

      <!-- Save button -->
      <button type="submit" class="submit-button btn-form" :disabled="isSubmitting">
        <span v-if="!isSubmitting">Save Changes</span>
        <span v-else class="spinner-border" role="status">
          <span class="sr-only">Loading...</span>
        </span>
      </button>

      <!-- Delete button -->
      <button
        type="button"
        class="danger-button btn-form"
        :disabled="isSubmitting"
        @click="submitForm('DELETE')"
      >
        <span v-if="!isSubmitting">Delete Post</span>
        <span v-else class="spinner-border" role="status">
          <span class="sr-only">Loading...</span>
        </span>
      </button>
    </form>
  </div>
</template>

<script>
import { getCookie } from "../csrf.js";

export default {
  data() {
    return {
      fields: [
        { id: 'title', label: 'Title', value: '', attrs: { type: 'text', required: true }, errors: [] },
        { id: 'description', label: 'Description', value: '', attrs: { type: 'text', required: false }, errors: [] },
      ],
      errorMessage: '',
      isSubmitting: false,
      postId: null,
    };
  },
  async mounted() {
    await this.loadInitData();
  },
  methods: {
    async loadInitData() {
      try {
        const postId = this.$route.params.id;
        const res = await fetch(`/api/post/${postId}/update/`);
        const data = await res.json();
        this.fields.find(f => f.id === 'title').value = data.title;
        this.fields.find(f => f.id === 'description').value = data.description;
        this.postId = postId;
      } catch (err) {
        console.error("Failed to load post data:", err);
      }
    },
    async submitForm(method = 'PUT') {
      this.isSubmitting = true;
      this.clearErrors();

      const formData = new FormData();
      this.fields.forEach(field => formData.append(field.id, field.value));
      formData.append('_method', method);

      try {
        const response = await fetch(`/api/post/${this.postId}/update/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': getCookie('csrftoken'),
          },
          body: formData,
        });

        const data = await response.json();

        if (data.status === 'success') {
          if (method === 'DELETE') {
            this.$router.push(`/}`); // повернення до списку після видалення
          } else {
            this.$router.push(`/posts/${this.postId}`); // після збереження
          }
        } else {
          this.errorMessage = data.error_message || 'Operation failed';
        }
      } catch (error) {
        console.error('Error submitting form:', error);
        this.errorMessage = 'Unexpected error. Try again.';
      } finally {
        this.isSubmitting = false;
      }
    },
    clearErrors() {
      this.errorMessage = '';
      this.fields.forEach(field => {
        field.errors = [];
      });
    },
  },
};
</script>
