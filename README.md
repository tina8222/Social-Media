Social Media API

A scalable Social Media REST API built with Django and Django REST Framework.

This project was developed collaboratively as a backend social media platform, providing core features such as user authentication, posts, comments, likes, and notifications.

---

Features

- User Authentication
- Create, Update, and Delete Posts
- Like / Unlike System
- Comment System
- Notification System
- Image Upload Support
- JWT Authentication
- RESTful API Design
- Modular Django Apps Architecture
- API Documentation with Swagger / OpenAPI

---

Tech Stack

- Python 3.12+
- Django 5
- Django REST Framework
- PostgreSQL
- JWT Authentication
- Pillow
- drf-spectacular

---

Project Structure

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
├── media/
├── manage.py
└── requirements.txt

---

Installation

Clone the repository:

git clone https://github.com/tina8222/Social-Media.git
cd Social-Media

Create a virtual environment:

python -m venv .venv

Activate it:

Windows

.venv\Scripts\activate

Linux / macOS

source .venv/bin/activate

Install the dependencies:

pip install -r requirements.txt

---

Environment Variables

Create a ".env" file based on the provided environment example:

cp .env.example .env

Configure your database and secret key inside the ".env" file.

Example:

SECRET_KEY=your_secret_key
DEBUG=True

DB_NAME=social_media_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

---

Database

Run migrations:

python manage.py migrate

Create a superuser:

python manage.py createsuperuser

---

Run the Project

Start the development server:

python manage.py runserver

The API will be available at:

http://127.0.0.1:8000/

---

API Modules

Module| Description
Users| Authentication and user management
Posts| Create, update, delete, and retrieve posts
Comments| Create and manage comments
Likes| Like and unlike posts
Notifications| Manage user notifications

---

API Documentation

API documentation is available through Swagger / OpenAPI using drf-spectacular.

/api/schema/
/api/docs/

---

Project Collaboration

This project was developed collaboratively as part of a backend development project.

The development process included working with Git, GitLab, GitHub, Django REST Framework, and collaborative code review through Merge Requests.

---

Contributors

- Tina Mirdar Soltani — Backend Developer


---

License

This project is available under the MIT License.
