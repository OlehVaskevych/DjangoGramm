# 📸 DjangoGramm

DjangoGramm is a social media web application inspired by Instagram.  
It provides user authentication, profile management, photo sharing, likes, comments, and follows.  
The project also includes centralized logging, error handling, and Docker support 🚀.

---

## ✨ Features

- 👤 User registration & authentication  
- 🔑 Login & logout
- 📝 Create, edit, and delete posts (images + captions)  
- ❤️ Like & 💬 comment on posts  
- 👥 Follow/unfollow other users  
- 🧑‍💻 Profile update (name, bio, avatar)  
- 🔎 Explore other users & their posts

---

## 🛠️ Tech Stack

- Python 3.12  
- Django & Django REST Framework  
- PostgreSQL  
- Pillow (image handling)  

---

## 🚀 Getting Started

### Running Locally (without Docker)

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   .venv\Scripts\activate      # Windows
   ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run PostgreSQL (Docker):

    ```bash
    docker run --name djangogramm-db \
    -e POSTGRES_DB=DjangoGramm \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=mysecretpassword \
    -p 5432:5432 -d postgres:latest
    ```
   
4. Apply migrations:

    ```bash
   python manage.py migrate
    ```
   
5. Run the Django server:

    ```bash
    python manage.py runserver
    ```
   
6. Open link 👉 http://localhost:8000/

---

## 📚 Endpoints

| Method | Endpoint                                 | Description                    |
|--------|------------------------------------------|--------------------------------|
| POST   | `/auth/register/`                        | Register a new user            |
| POST   | `/auth/login/`                           | Login                          |
| POST   | `/auth/logout/`                          | Logout                         |
| GET    | `/settings/`                             | Settings page for edit profile |
| POST   | `/psot/`                                 | Create a new post              |
| GET    | `/psot/{post_id}/`                       | View a specific post           |
| POST   | `/post/{post_id}/likes/`                 | Like a post                    |
| POST   | `/posts/{post_id}/comments/`             | Comment on a post              |
| POST   | `/posts/{post_id}/comments/{comment_id}` | Delete the specified comment   |
| GET    | `/posts/{post_id}/update`                | Render post edit page          |
| PUT    | `/posts/{post_id}/update`                | Edit Post request              |
| DELETE | `/posts/{post_id}/update`                | Delete post request            |
| GET    | `/profile/{username}/`                   | View a specified profile       |
| GET    | `/profile/{username}/update`             | Render profile edit page       |
| PUT    | `/profile/{username}/update`             | Profile edit request           |
| DELETE | `/profile/{username}/update`             | Profile delete request         |
| POST   | `/profile/{username}/follows`            | Follow for specified user      |

## ⚙️ Configuration

All important settings (secret key, database URL, Redis URL, token expiration times) are stored in .env file.

Example .env:

```dotenv
DJANGO_SECRET_KEY=your-secret-key
DEFAULT_AVATAR_PATH="avatars/default_avatar.jpg"
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=your-database-host
DB_PORT=5432
```

## 🧪 Testing

Run tests using:

```bash
pytest
```

## 👨‍💻 Author

Created by Oleh Vaskevych

## 📜 License

This project is licensed under the MIT License.
