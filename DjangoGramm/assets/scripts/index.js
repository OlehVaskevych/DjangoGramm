import 'bootstrap'; // Імпорт Bootstrap JS
import 'bootstrap/dist/css/bootstrap.min.css';
import '../styles/styles.css'; // Імпорт вашого CSS
import { initPostForm } from './forms/postForm';
import { initNavigation } from './navigation/navigation';

document.addEventListener('DOMContentLoaded', () => {
    // Ініціалізуємо форму, якщо вона є на сторінці
    const postFormContainer = document.getElementById('create-post-app');
    if (postFormContainer) {
        initPostForm();
    }

    // Ініціалізуємо навігацію
    initNavigation();
});
