<template>
  <h1 class="form-title">Edit {{ username }}'s profile</h1>
  <form @submit.prevent="submitForm" enctype="multipart/form-data" class="styled-form">
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
    <div class="form-group" v-for="field in fields" :key="field.id">
      <label :for="field.id">{{ field.label }}</label>

      <!-- Прев'ю аватара -->
      <div v-if="field.id === 'avatar'" class="avatar-preview-wrapper">
        <div class="avatar-container">
          <img
            v-if="field.preview"
            :src="field.preview"
            alt="Avatar preview"
            class="img-fluid rounded-circle avatar-preview"
          >
          <input
            v-if="!field.preview"
            type="file"
            :id="field.id"
            @change="handleFileChange($event, field)"
            class="file-input"
          >
          <button type="button" class="remove-button" @click="removeAvatarWithConfirmation(field)" v-if="field.preview"></button>
        </div>
      </div>

      <!-- Інші поля -->
      <input
        v-else
        :id="field.id"
        v-model="field.value"
        :type="field.attrs.type"
        :name="field.id"
        :required="field.attrs.required"
        :class="field.class"
      >
      <!-- Помилки -->
      <p v-for="error in field.errors" :key="error" class="form-error">
        {{ error }}
      </p>
    </div>

    <button type="submit" class="submit-button btn-form" :disabled="isSubmitting">
      <span v-if="!isSubmitting">Save Changes</span>
      <span v-else class="spinner-border" role="status">
        <span class="sr-only">Loading...</span>
      </span>
    </button>
  </form>
</template>

<script>
export default {
  data() {
    return {
      isAvatarRemoved: false,
      errorMessage: '',
      isSubmitting: false,
      username: initialData.username,
      fields: [
        { id: 'first_name', label: 'First Name:', value: initialData.first_name, attrs: { type: 'text', required: false }, errors: [] },
        { id: 'last_name', label: 'Last Name:', value: initialData.last_name, attrs: { type: 'text', required: false }, errors: [] },
        { id: 'bio', label: 'BIO:', value: initialData.bio, attrs: { type: 'text', required: false }, errors: [] },
        {
          id: 'avatar',
          label: 'Upload avatar:',
          value: null,
          preview: initialData.avatar || null,
          class: 'file-input',
          attrs: { type: 'file', required: false },
          errors: [],
        },
      ],
    };
  },
  methods: {
    async submitForm() {
      this.isSubmitting = true;
      this.clearErrors();

      const formData = new FormData();

      this.fields.forEach((field) => {
        if (field.id === 'avatar' && field.value) {
          formData.append(field.id, field.value);
        } else if (field.id !== 'avatar') {
          formData.append(field.id, field.value);
        }
      });

      if (this.isAvatarRemoved) {
        formData.append('remove_avatar', true);
      }

      formData.append('_method', 'PUT');

      const url = `/profile/${this.username}/upadate`;

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

    // Метод для підтвердження видалення аватарки
    removeAvatarWithConfirmation(field) {
      const confirmed = window.confirm("Are you sure you want to reset your avatar to the default?");
      if (confirmed) {
        this.removeAvatar(field);
      }
    },


    handleFileChange(event, field) {
      const file = event.target.files[0];
      if (file) {
        field.value = file;
        field.preview = URL.createObjectURL(file); // Оновлення прев'ю
        this.isAvatarRemoved = false; // Скидаємо прапорець видалення
      }
    },

    removeAvatar(field) {
      this.isAvatarRemoved = true;
      field.value = null;
      field.preview = null;
    },

    clearErrors() {
      this.errorMessage = '';
      this.fields.forEach((field) => {
        field.errors = [];
      });
    },

    updateFieldErrors(errors) {
      Object.entries(errors).forEach(([fieldName, fieldErrors]) => {
        const field = this.fields.find((f) => f.id === fieldName);
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


<style scoped>
.avatar-preview-wrapper {
  margin-top: 10px;
}

.avatar-preview {
  width: 150px;
  height: 150px;
  object-fit: cover;
  border-radius: 50%;
}

.avatar-container {
  position: relative; /* Make this the positioned ancestor */
}

.remove-button {
  position: absolute;
  top: -10px;  /* Піднімемо кнопку трохи вище */
  right: -10px; /* Перемістимо праворуч для точнішого вирівнювання */
  background-color: var(--primary-color); /* Трошки прозорий фон для елегантності */
  border: none;
  border-radius: 50%;
  width: 30px; /* Встановлюємо розмір кнопки */
  height: 30px; /* Встановлюємо розмір кнопки */
  display: flex;
  align-items: center;  /* Центруємо хрестик */
  justify-content: center; /* Центруємо хрестик */
  cursor: pointer;
  font-size: 18px; /* Розмір шрифту для хрестика */
  color: var(--text-color); /* Колір хрестика */
  transition: background-color 0.3s ease; /* Додаємо ефект зміни кольору фону */
}

.remove-button:hover {
  background-color: rgba(26, 255, 0, 0.3); /* Колір фону при наведенні */
}

.remove-button:focus {
  outline: none; /* Прибираємо обводку при фокусі */
}

/* Для самого хрестика */
.remove-button::before {
  content: '×'; /* Символ хрестика */
  font-size: 20px;  /* Розмір хрестика */
  font-weight: bold;
}


</style>
