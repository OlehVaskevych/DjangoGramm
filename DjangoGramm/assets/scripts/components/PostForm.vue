<template>
    <div class="form-container">
        <h1 class="form-title">Create post</h1>
        <form @submit.prevent="submitForm" enctype="multipart/form-data" class="styled-form">
            <div class="form-group" v-for="field in fields" :key="field.id">
                <label :for="field.id">{{ field.label }}</label>
                <input
                    v-bind="field.attrs"
                    :id="field.id"
                    v-model="field.value"
                />
                <small v-if="field.helpText" class="form-text">{{ field.helpText }}</small>
                <p v-for="error in field.errors" :key="error" class="form-error">
                    {{ error }}
                </p>
            </div>
            <div class="form-group">
                <label for="images">Upload photos:</label>
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
            <div v-if="previews.length" class="image-previews">
                <label>Uploaded photos:</label>
                <div v-for="(src, index) in previews" :key="index" class="preview">
                    <img :src="src" alt="Preview" class="preview-img" />
                </div>
            </div>
            <button type="submit" class="submit-button">Create</button>
        </form>
    </div>
</template>

<script>
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export default {
    data() {
        return {
            previews: [],
        };
    },
    methods: {
        async submitForm() {
            const csrfToken = getCookie('csrftoken');

            const formData = new FormData();

            // Додаємо дані полів у formData
            this.fields.forEach((field) => {
                formData.append(field.id, field.value);
            });

            // Додаємо файли у formData
            const files = this.$refs.fileInput.files;
            for (let i = 0; i < files.length; i++) {
                formData.append('images', files[i]);
            }

            try {
                // Відправляємо POST-запит із CSRF-токеном
                const response = await fetch('/post/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Accept': 'application/json',
                    },
                    body: formData,
                });

                if (!response.ok) {
                    const errorText = await response.json();
                    console.error('Server error:', errorText);
                    alert('Error creating post. Check console for details.');
                    return;
                }

                // Перевіряємо, чи сервер виконав редірект
                const locationHeader = response.headers.get('Location');
                if (locationHeader) {
                    // Якщо є заголовок Location, виконуємо редірект
                    window.location.href = locationHeader;
                } else {
                    alert('Post created successfully!');
                }
            } catch (error) {
                console.error('Error submitting form:', error);
            }
        },

        handleFileUpload(event) {
            // Звільняємо попередні об’єкти URL
            if (this.previews.length) {
                this.previews.forEach((src) => URL.revokeObjectURL(src));
            }
            const files = event.target.files;
            this.previews = Array.from(files).map((file) =>
                URL.createObjectURL(file)
            );
        },
    },
    props: {
        csrfToken: {
            type: String,
            default: () => document.querySelector('meta[name="csrf-token"]').getAttribute('content'),
        },
        fields: {
            type: Array,
            required: true,
        },
    },
};
</script>


<style scoped>
.image-previews {
    margin-top: 15px;
    margin-bottom: 15px;
}

.preview-img {
    width: 100px;
    height: 100px;
    object-fit: cover;
    border: 1px solid var(--border-color);
    border-radius: 5px;
}

.preview {
    display: inline-block;
    width: calc(33.333% - 10px);
    margin-right: 10px;
    margin-bottom: 10px;
}
</style>
