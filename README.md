# Social Media API

A scalable Social Media REST API built with **Django** and **Django REST Framework**.  
This project provides the core backend functionalities of a social networking platform, including user authentication, posts, comments, likes, and notifications.

---

## Features

- User Authentication
- Create, Update, Delete Posts
- Like System
- Comment System
- Notification System
- Image Upload Support
- RESTful API Design
- Modular Django Apps Architecture

---

## Tech Stack

- Python 3.12+
- Django 5
- Django REST Framework
- PostgreSQL
- JWT Authentication
- Pillow
- drf-spectacular (Swagger/OpenAPI)

---

## Project Structure

```
Social-Media/
│
├── apps/
│   ├── users/
│   ├── post/
│   ├── comment/
│   ├── like/
│   └── notification/
│
├── config/
│
├── media/
├── manage.py
└── requirements.txt
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/ManiNaseri/Social-Media.git
cd Social-Media
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Configure your database and secret keys inside the `.env` file.

Example:

```env
SECRET_KEY=your_secret_key

DEBUG=True

DB_NAME=social_media_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost or etc..
DB_PORT=5432
```

---

## Database

Run migrations:

```bash
python manage.py migrate
```

Create a superuser:

```bash
python manage.py createsuperuser
```

---

## Run the Project

```bash
python manage.py runserver
```

Server:

```
http://127.0.0.1:8000/
```

---

## API Modules

| Module | Description |
|---------|-------------|
| Users | Authentication & User Management |
| Posts | CRUD operations for posts |
| Comments | Create and manage comments |
| Likes | Like/Unlike functionality |
| Notifications | User notification system |

---

## 📖 API Documentation

If drf-spectacular is enabled, Swagger/OpenAPI documentation can be accessed via:

```
/api/schema/
/api/docs/
```

---

## Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature/new-feature
```

3. Commit your changes

```bash
git commit -m "Add new feature"
```

4. Push your branch

```bash
git push origin feature/new-feature
```

5. Open a Pull Request

---

## License

This project is available under the MIT License.

---

## Author

Tina Mirdar Soltani

tiGitHub:
https://github.com/ManiNaseri
