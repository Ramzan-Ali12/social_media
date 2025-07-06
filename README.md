# Social Media API

A simple social media REST API built with Django and Django REST Framework.  
Features user registration, authentication, post creation, and liking/unliking posts.

## Features

- User registration and login (token-based authentication)
- Create, update, delete, and list posts
- Like/unlike posts
- API documentation with Swagger and Redoc

## Tech Stack

- Python 3.12+
- Django 5.1+
- Django REST Framework
- PostgreSQL
- drf-yasg (Swagger/OpenAPI docs)

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Ramzan-Ali12/social_media.git
cd social-media
```

### 2. Install dependencies

Using [Poetry](https://python-poetry.org/):

```bash
poetry install
```

Or with pip:

```bash
pip install -r requirements.txt
```

### 3. Configure environment

Create a `.env` file in the project root:

```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 4. Database setup

Ensure PostgreSQL is running and create a database:

```sql
CREATE DATABASE social_media;
```

Update `DATABASES` in `core/settings.py` if needed.

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

## API Endpoints

### Auth

- `POST /api/v1/auth/register/` — Register a new user
- `POST /api/v1/auth/login/` — Obtain auth token
- `POST /api/v1/auth/logout/` — Logout (invalidate token)

### Posts

- `GET /api/v1/posts/` — List all posts
- `POST /api/v1/posts/` — Create a post (auth required)
- `GET /api/v1/posts/{id}/` — Retrieve a post
- `PUT/PATCH /api/v1/posts/{id}/` — Update a post (owner only)
- `DELETE /api/v1/posts/{id}/` — Delete a post (owner only)
- `POST /api/v1/posts/{id}/like/` — Like/unlike a post (toggle, auth required)

### Documentation

- Swagger UI: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- Redoc: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

## Project Structure

```
social_media/
├── core/           # Django project settings
├── posts/          # Posts app (models, views, serializers)
├── users/          # Users app (registration, login, serializers)
├── manage.py
├── requirements.txt
├── pyproject.toml
└── README.md
```

## License

BSD License

---

**Author:** Muhammad-Ramzan12  
**Contact:** mramzanali258@gmail.com
