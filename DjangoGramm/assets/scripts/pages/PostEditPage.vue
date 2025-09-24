<template>
  <div class="form-container">
    <h1 class="form-title">Post Edit</h1>

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
          :name="field.id"
          :required="field.attrs.required"
        >
        <small v-if="field.helpText" class="form-text">{{ field.helpText }}</small>
        <p v-for="error in field.errors" :key="error" class="form-error">{{ error }}</p>
      </div>

      <button type="submit" class="submit-button btn-form" :disabled="isSubmitting">
        <span v-if="!isSubmitting">Save Changes</span>
        <span v-else class="spinner-border" role="status">
          <span class="sr-only">Loading...</span>
        </span>
      </button>
    </form>
  </div>
</template>

<script>
export default {
  props: {

  },
  data() {
    return {
      fields: [
        { id: 'title', label: 'Title', value: '', attrs: { type: 'text', required: true }, errors: [] },
        { id: 'description', label: 'Description', value: '', attrs: { type: 'text', required: false }, errors: [] },
      ],
      errorMessage: '',
      isSubmitting: false,
      loading: false,
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
        console.log(data);
        console.log(this.fields);
      } catch (err) {
        console.error("Failed to load post data:", err);
      }
    },
    async submitForm() {
      this.isSubmitting = true;
      this.clearErrors();

      const formData = new FormData();
      this.fields.forEach(field => formData.append(field.id, field.value));

      try {
        const response = await fetch(`/api/post/${this.postId}/update/`, {
          method: 'POST',
          body: formData,
        });
        const data = await response.json();

        if (response.ok && data.status === 'ok') {
          this.$router.push(`/post/${this.postId}/`);
        } else {
          this.errorMessage = data.error_message || 'Failed to update post';
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
