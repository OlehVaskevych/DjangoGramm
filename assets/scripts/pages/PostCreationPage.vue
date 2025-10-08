<template>
  <div class="form-container">
    <h1 class="form-title">Create post</h1>
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
        />
        <small v-if="field.helpText" class="form-text">{{ field.helpText }}</small>
        <p v-for="error in field.errors" :key="error" class="form-error">
          {{ error }}
        </p>
      </div>
      <div class="form-group">
        <label for="images">Upload photos (max 10):</label>
        <input
          ref="fileInput"
          type="file"
          id="images"
          name="images"
          multiple
          class="file-input"
          @change="handleFileUpload"
        />
      </div>
      <p v-if="errors.images" v-for="error in errors.images" :key="error" class="form-error">
        {{ error }}
      </p>
      <div v-if="previews.length" class="image-previews">
        <label>Uploaded photos ({{ previews.length }}/10):</label>
        <div v-for="(src, index) in previews" :key="index" class="preview">
          <div class="preview-container">
            <img :src="src" alt="Preview" class="preview-img" />
            <button
              type="button"
              class="remove-button"
              @click="removePreview(index)"
            >
              &#x2715;
            </button>
          </div>
        </div>
      </div>
      <button type="submit" class="submit-button" :disabled="isSubmitting">
        <span v-if="!isSubmitting">Create</span>
        <span v-else class="spinner-border" role="status">
          <span class="sr-only">Loading...</span>
        </span>
      </button>
    </form>
  </div>
</template>

<script>
import { getCookie } from '../csrf.js';

export default {
  data() {
    return {
      fields: [
        { id: 'title', label: 'Title', value: '', attrs: { type: 'text', required: true }, errors: [] },
        { id: 'description', label: 'Description', value: '', attrs: { type: 'text', required: true }, errors: [] },
      ],
      images: [],
      errors: {},
      errorMessage: '',
      isSubmitting: false,
      previews: [],
      removedIndexes: [],
    };
  },
  methods: {
    async submitForm() {
      this.isSubmitting = true;
      this.clearErrors();

      const formData = new FormData();

      // Add form fields to FormData
      this.fields.forEach((field) => {
        formData.append(field.id, field.value);
      });

      // Add files to FormData
      const files = this.$refs.fileInput.files;
      let imageCount = 0;
      for (let i = 0; i < files.length && imageCount < 10; i++) {
        if (!this.removedIndexes.includes(i)) {
          formData.append('images', files[i]);
          imageCount++;
        }
      }

      try {
        const response = await fetch('/api/post/', {
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
            this.errorMessage = data.error_message || 'An error occurred while creating the post.';
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
      this.errors = {};
    },
    updateFieldErrors(errors) {
      Object.entries(errors).forEach(([fieldName, fieldErrors]) => {
        const field = this.fields.find((f) => f.id === fieldName);
        if (field) {
          field.errors = Array.isArray(fieldErrors) ? fieldErrors : [fieldErrors];
        } else if (fieldName === 'images') {
          this.errors.images = Array.isArray(fieldErrors) ? fieldErrors : [fieldErrors];
        }
      });
    },
    handleFileUpload(event) {
      const files = event.target.files;
      if (files.length > 10) {
        this.errorMessage = 'You can only upload up to 10 images.';
        this.$refs.fileInput.value = ''; // Clear the file input
        return;
      }

      // Clear previous previews
      this.destroyPreviews();

      this.previews = Array.from(files).map((file) => URL.createObjectURL(file));
      this.removedIndexes = [];
    },
    removePreview(index) {
      URL.revokeObjectURL(this.previews[index]);
      this.previews.splice(index, 1);

      const dt = new DataTransfer();
      const files = this.$refs.fileInput.files;
      for (let i = 0; i < files.length; i++) {
        if (i !== index) {
          dt.items.add(files[i]);
        }
      }
      this.$refs.fileInput.files = dt.files;

      this.removedIndexes = this.removedIndexes.map((i) => (i > index ? i - 1 : i)).filter((i) => i !== index);
    },
    destroyPreviews() {
      if (this.previews.length) {
        this.previews.forEach((src) => URL.revokeObjectURL(src));
        this.previews = [];
      }
      this.removedIndexes = [];
    },
  },
  beforeDestroy() {
    this.destroyPreviews();
  },
};
</script>
