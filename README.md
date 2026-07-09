# Backend - Task and Image Annotation API

This is the backend for the **Task and Image Annotation** project.

It is built with **Django**, **Django REST Framework**, **JWT authentication**, and **SQLite database**.


## Villains I Faced

During this backend, I faced some strong villains.

The first villain was **JWT token handling**. Sometimes old or expired tokens caused login and API errors. I solved it by checking protected routes properly and clearing invalid tokens from the frontend.

The second villain was **image batching**. At first, all images were saved separately. But I needed one upload group to stay inside one batch. I defeated this villain by creating an `AnnotationBatch` model and linking every uploaded image to a batch.

The third villain was **time format in Django admin**. The time looked confusing because Django was using UTC. I fixed it by setting the timezone to `Asia/Dhaka`.

The final villain was **database ID numbers**. Even after deleting old batches, new batches started from higher IDs. I learned that databases do not reuse old IDs. I solved it in the frontend by showing serial batch numbers instead of database IDs.

I overcame these problems with Django documentation, error messages, debugging, and help from AI.


## Features

* User registration and login
* JWT based authentication
* Task management API
* Kanban task status update
* Image upload
* Image batch/group upload
* Polygon annotation save
* Polygon update and delete
* Swagger API documentation

## Tech Stack

* Python 3.13
* Django 6.0.7
* Django REST Framework 3.17.1
* Simple JWT 5.5.1
* drf-spectacular 0.30.0
* Pillow 12.3.0
* SQLite database


## Requirements

Install these packages:

```txt
asgiref==3.11.1
attrs==26.1.0
Django==6.0.7
django-cors-headers==4.9.0
djangorestframework==3.17.1
djangorestframework_simplejwt==5.5.1
drf-spectacular==0.30.0
inflection==0.5.1
jsonschema==4.26.0
jsonschema-specifications==2025.9.1
pillow==12.3.0
PyJWT==2.13.0
PyYAML==6.0.3
referencing==0.37.0
rpds-py==2026.6.3
sqlparse==0.5.5
tzdata==2026.2
uritemplate==4.2.0
```

## How to Run

Go to the folder:

Activate the virtual environment:


Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create a superuser:

```bash
python manage.py createsuperuser
```

Run the server:

```bash
python manage.py runserver
```

Backend will run here:

```txt
http://127.0.0.1:8000/
```

## API Documentation

Swagger documentation:

```txt
http://127.0.0.1:8000/api/docs/
```

Schema:

```txt
http://127.0.0.1:8000/api/schema/
```

Redoc:

```txt
http://127.0.0.1:8000/api/redoc/
```

## Important API Routes

### Authentication

```txt
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/refresh/
GET  /api/auth/me/
```

### Tasks

```txt
GET    /api/tasks/
POST   /api/tasks/
PATCH  /api/tasks/<id>/
DELETE /api/tasks/<id>/
PATCH  /api/tasks/<id>/move/
```

### Annotations

```txt
GET    /api/annotations/batches/
POST   /api/annotations/batches/
DELETE /api/annotations/batches/<id>/

GET    /api/annotations/images/
POST   /api/annotations/images/
GET    /api/annotations/images/<id>/
DELETE /api/annotations/images/<id>/

GET    /api/annotations/images/<image_id>/polygons/
POST   /api/annotations/images/<image_id>/polygons/
PATCH  /api/annotations/polygons/<id>/
DELETE /api/annotations/polygons/<id>/
```

 