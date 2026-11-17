# Quick Serve

Quick Serve is a Django-based backend for connecting clients with service
providers. The project currently contains the initial data model, database
configuration, and a small REST API for registration, login, and health
checking.

## Technology

- Python
- Django 6.1
- Django REST Framework
- PostgreSQL
- `python-dotenv` for local environment configuration
- Simple JWT configured as the REST Framework authentication backend

## Project structure

```text
quick_serve/
├── backend/
│   ├── api/exceptions.py   # REST Framework exception formatting
│   ├── errors.py           # Shared JSON error responses
│   ├── middleware.py       # JSON responses for unhandled HTTP errors
│   ├── migrations/         # Database migrations
│   ├── models.py           # User, ServiceProfile, and Order models
│   ├── urls.py             # API routes
│   └── views.py            # API views
├── quick_serve/
│   ├── settings.py         # Django and PostgreSQL configuration
│   └── urls.py             # Root URL configuration
├── manage.py
└── readme.md
```

## Setup

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the project dependencies:

```powershell
pip install django djangorestframework djangorestframework-simplejwt python-dotenv psycopg2-binary
```

### 2. Configure PostgreSQL

Create a `.env` file in the project root. Do not commit this file or real
credentials:

```dotenv
DB_NAME=quick_serve
DB_USER=quick_serve
DB_PASSWORD=change-me
DB_HOST=localhost
DB_PORT=5432
```

The application loads these values in
[`quick_serve/settings.py`](quick_serve/settings.py). The database must be
running before applying migrations or starting the development server.

### 3. Apply migrations

```powershell
python manage.py migrate
```

### 4. Start the development server

```powershell
python manage.py runserver
```

The API is available at `http://127.0.0.1:8000/api/`.

## API endpoints

All routes currently use the `/api/` prefix. Trailing slashes are not added
automatically, so use the paths exactly as shown.

### Health check

`GET /api/hello`

```json
{
  "message": "hello_world"
}
```

### Register

`POST /api/register`

Request body:

```json
{
  "first_name": "Aisha",
  "last_name": "Khan",
  "email": "aisha@example.com",
  "password": "change-me"
}
```

The request requires all four fields. A successful response confirms that the
user was registered.

### Login

`POST /api/login`

Request body:

```json
{
  "email": "aisha@example.com",
  "password": "change-me"
}
```

The login route is present and accepts email/password credentials. Token
issuance and production-ready credential validation are still being completed.

## Data model

### `User`

Represents a client or service provider.

| Field | Type | Details |
| --- | --- | --- |
| `id` | AutoField | Django-generated primary key |
| `first_name` | CharField | Maximum 100 characters |
| `last_name` | CharField | Maximum 100 characters |
| `email` | EmailField | User email address |
| `password` | CharField | Stored password value; authentication hardening is pending |
| `created_at` | DateTimeField | Set automatically when the record is created |

### `ServiceProfile`

Represents a service offered by a user.

| Field | Type | Details |
| --- | --- | --- |
| `id` | AutoField | Django-generated primary key |
| `service_provider` | ForeignKey | Required reference to `User` |
| `service_name` | CharField | Maximum 100 characters |
| `description` | TextField | Service description |
| `is_active` | BooleanField | Defaults to `True` |
| `created_at` | DateTimeField | Set automatically when the record is created |

### `Order`

Represents a client ordering a service.

| Field | Type | Details |
| --- | --- | --- |
| `id` | AutoField | Django-generated primary key |
| `client` | ForeignKey | Required reference to `User` |
| `service` | ForeignKey | Required reference to `ServiceProfile` |
| `created_at` | DateTimeField | Set automatically when the record is created |

All model relationships use cascading deletion. Deleting a user removes their
service profiles and related orders; deleting a service profile removes its
related orders.

## Error responses

The middleware and REST Framework exception handler normalize API errors to
JSON. A typical error has this shape:

```json
{
  "success": false,
  "status": 400,
  "error": {
    "message": "Bad request."
  }
}
```

Validation errors may also include an `error.details` object.

## Current status

Implemented:

- Django project and `backend` application
- PostgreSQL configuration loaded from `.env`
- Initial migrations for users, service profiles, orders, and user passwords
- `GET /api/hello`
- `POST /api/register`
- `POST /api/login` route
- Consistent JSON formatting for HTTP and REST Framework errors

Pending or incomplete:

- Secure password hashing and credential validation
- JWT token creation and refresh flow
- Service profile and order API endpoints
- User location fields and location tracking
- Input serializers, duplicate-email handling, and automated API tests
- Production settings, including a non-debug deployment configuration and
  secret management
