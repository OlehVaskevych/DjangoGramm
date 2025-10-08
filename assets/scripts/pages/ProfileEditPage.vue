<template>
  <div class="container mt-5">
    <h1 class="form-title">Edit {{ username }}'s profile</h1>

    <!-- Показуємо спіннер, поки дані завантажуються -->
    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="sr-only">Loading profile data...</span>
      </div>
    </div>

    <form v-else @submit.prevent="submitForm" enctype="multipart/form-data" class="styled-form">
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <!-- 💡 Важливо: використовуємо v-if="!isLoading" для форми -->
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
            <!-- Кнопка видалення аватарки -->
            <button
              type="button"
              class="remove-button"
              @click="removeAvatarWithConfirmation(field)"
              v-if="field.preview"
            >
            </button>
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
  </div>
</template>

<script>
import { getCookie } from '../csrf.js';

export default {
  // 💡 Використовуємо `created` для отримання параметрів маршруту
  created() {
    this.username = this.$route.params.username;
  },

  data() {
    return {
      isLoading: true, // Додаємо прапорець завантаження
      isAvatarRemoved: false,
      errorMessage: '',
      isSubmitting: false,
      username: '', // Буде заповнено в created
      // Ініціалізуємо поля зі значеннями за замовчуванням
      fields: [
        { id: 'first_name', label: 'First Name:', value: '', attrs: { type: 'text', required: false }, errors: [] },
        { id: 'last_name', label: 'Last Name:', value: '', attrs: { type: 'text', required: false }, errors: [] },
        { id: 'bio', label: 'BIO:', value: '', attrs: { type: 'text', required: false }, errors: [] },
        {
          id: 'avatar',
          label: 'Upload avatar:',
          value: null,
          preview: null, // Початкове прев'ю буде завантажено з API
          class: 'file-input',
          attrs: { type: 'file', required: false },
          errors: [],
        },
      ],
    };
  },

  methods: {
    async loadInitialData() {
        this.isLoading = true;
        this.errorMessage = ''; // Очищаємо попередні помилки

        try {
            const url = `/profile/${this.username}/update/`;
            const res = await fetch(url, {
              method: 'GET',
              credentials: 'include', // <--- дуже важливо
              headers: {
                'X-CSRFToken': getCookie('csrftoken'),
              },
            });

            if (!res.ok) {
                // Якщо відповідь сервера не 200 (наприклад, 401, 403, 404),
                // пробуємо прочитати body як JSON, щоб отримати детальну помилку (якщо вона є)
                let errorData;
                try {
                    errorData = await res.json();
                } catch (e) {
                    // Якщо не вдалося прочитати JSON (бо це HTML-сторінка перенаправлення)
                    if (res.status === 403 || res.status === 401 || res.status === 302) {
                        this.errorMessage = `Error ${res.status}: Authorization failed. Are you sure you are logged in and authorized to edit this profile?`;
                    } else {
                        // Інша не-JSON помилка (наприклад, 404)
                        this.errorMessage = `Error ${res.status}: Could not load profile data. Server returned an unexpected format.`;
                    }
                    this.isLoading = false;
                    return;
                }

                // Якщо вдалося прочитати JSON (наприклад, 400 Bad Request від Django)
                this.errorMessage = errorData.error_message || `Could not load profile data (Status ${res.status}).`;
                this.isLoading = false;
                return;
            }

            // Якщо res.ok === true
            const data = await res.json();

            if (data.initial_data) {
                const initialData = data.initial_data;
                // Оновлення значень полів на основі отриманих даних
                this.fields.forEach(field => {
                    if (initialData[field.id] !== undefined && field.id !== 'avatar') {
                        field.value = initialData[field.id] || '';
                    } else if (field.id === 'avatar' && initialData.avatar) {
                        field.preview = initialData.avatar; // Встановлюємо поточний URL аватарки
                    }
                });
            } else {
                this.errorMessage = 'Data loaded successfully, but "initial_data" key is missing.';
            }
        } catch (error) {
            console.error('Error loading initial profile data:', error);
            // Цей блок ловить мережеві помилки або SyntaxError, якщо HTML таки прослизнув
            this.errorMessage = 'An unexpected error occurred during the network request. Check console for details.';
        } finally {
            this.isLoading = false;
        }
    },

    async submitForm() {
      this.isSubmitting = true;
      this.clearErrors();

      const formData = new FormData();

      this.fields.forEach((field) => {
        // Якщо це файл і він вибраний
        if (field.id === 'avatar' && field.value) {
          formData.append(field.id, field.value);
        // Якщо це не аватар
        } else if (field.id !== 'avatar') {
          formData.append(field.id, field.value);
        }
      });

      if (this.isAvatarRemoved) {
        formData.append('remove_avatar', true);
      }

      // 💡 Виправлення: Додаємо _method=PUT, як вимагає Django для обробки PUT через POST
      formData.append('_method', 'PUT');

      // Використовуємо той самий URL, який обробляє POST-запит у Django view
      const url = `/profile/${this.username}/update/`;

      try {
        const response = await fetch(url, {
          method: 'POST', // 💡 Виправлення: Метод повинен бути POST
          headers: {
            // CSRF токен потрібен для POST/PUT/PATCH запитів
            'X-CSRFToken': this.getCookie('csrftoken'),
          },
          body: formData,
        });

        // Django часто повертає дані, навіть якщо відповідь не 200
        // Пробуємо прочитати JSON
        let data;
        try {
            data = await response.json();
        } catch (e) {
            // Не JSON відповідь при відправці форми
             this.errorMessage = `Error ${response.status}: Server returned an unexpected response format during update.`;
             return;
        }

        if (response.ok) {
          // Успішне оновлення, перенаправляємо користувача на сторінку профілю
          this.$router.push(`/profile/${this.username}`);
        } else {
          // Обробка помилок
          this.errorMessage = data.error_message || 'An error occurred while saving changes.';
          if (data.errors) {
            this.updateFieldErrors(data.errors);
          }
        }
      } catch (error) {
        console.error('Error submitting form:', error);
        this.errorMessage = 'An unexpected error occurred. Please try again.';
      } finally {
        this.isSubmitting = false;
      }
    },

    // ... (решта методів залишаються без змін) ...
    removeAvatarWithConfirmation(field) {
      // 💡 Важливо: Замість window.confirm використовуйте власну модалку
      // через обмеження iframe, але для швидкого тестування залишимо confirm
      const confirmed = window.confirm("Are you sure you want to reset your avatar to the default?");
      if (confirmed) {
        this.removeAvatar(field);
      }
    },

    handleFileChange(event, field) {
      const file = event.target.files[0];
      if (file) {
        field.value = file;
        field.preview = URL.createObjectURL(file);
        this.isAvatarRemoved = false;
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
      // Метод отримання CSRF токена
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

  // 💡 Викликаємо завантаження даних при монтуванні компонента
  mounted() {
    this.loadInitialData();
  }
};
</script>
