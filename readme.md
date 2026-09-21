# Quick Serve Database Schema

This project uses Django ORM models in `backend/models.py` to represent users, service providers, services, and orders. The configured database engine is SQLite, using the `db.sqlite3` file in the project root.

## Schema Implementation

### `User`

Represents a person who can act as a client or a service provider.

| Field | Type | Details |
| --- | --- | --- |
| `id` | AutoField | Django-generated primary key |
| `first_name` | `CharField` | Required; maximum 100 characters |
| `last_name` | `CharField` | Required; maximum 100 characters |
| `email` | `EmailField` | Required; validated as an email address |
| `created_at` | `DateTimeField` | Automatically set when the record is created |

### `ServiceProfile`

Represents a service offered by a user.

| Field | Type | Details |
| --- | --- | --- |
| `id` | AutoField | Django-generated primary key |
| `service_provider_id` | Foreign key | References `User`; required |
| `service_name` | `CharField` | Required; maximum 100 characters |
| `description` | `TextField` | Required; stores the service description |
| `created_at` | `DateTimeField` | Automatically set when the record is created |

The `service_provider` relationship uses `on_delete=models.CASCADE`. Deleting a user therefore deletes that user's service profiles.

### `Order`

Represents a client ordering a service.

| Field | Type | Details |
| --- | --- | --- |
| `id` | AutoField | Django-generated primary key |
| `client_id` | Foreign key | References `User`; required |
| `service_id` | Foreign key | References `ServiceProfile`; required |
| `created_at` | `DateTimeField` | Automatically set when the record is created |

Both foreign keys use `on_delete=models.CASCADE`:

- Deleting a client deletes orders belonging to that client.
- Deleting a service profile deletes orders for that service.
- Deleting a service provider deletes their service profiles and the related orders through the cascading relationships.

## Relationship Overview

```text
User 1 ---- * ServiceProfile
User 1 ---- * Order
ServiceProfile 1 ---- * Order
```

The same `User` model can be referenced by `ServiceProfile.service_provider` and `Order.client`. Django also creates reverse relationships using its default names (`serviceprofile_set` and `order_set`).

## Database Setup Procedure

1. Add the app to `INSTALLED_APPS` in `quick_serve/settings.py`:

   ```python
   INSTALLED_APPS = [
       # ... existing Django apps ...
       'backend',
   ]
   ```

   `'backend.apps.BackendConfig'` may be used instead.

2. From the directory containing `manage.py`, create migrations for the models:

   ```bash
   python manage.py makemigrations backend
   ```

3. Apply the migrations to the SQLite database:

   ```bash
   python manage.py migrate
   ```

4. Confirm the generated migration and database state:

   ```bash
   python manage.py showmigrations backend
   python manage.py check
   ```

5. Optionally create records through the Django shell:

   ```bash
   python manage.py shell
   ```

   ```python
   from backend.models import Order, ServiceProfile, User

   provider = User.objects.create(
       first_name='Ava', last_name='Stone', email='ava@example.com'
   )
   client = User.objects.create(
       first_name='Noah', last_name='Reed', email='noah@example.com'
   )
   service = ServiceProfile.objects.create(
       service_provider=provider,
       service_name='Home Cleaning',
       description='Residential cleaning service',
   )
   order = Order.objects.create(client=client, service=service)
   ```

## Current Status

The database models are defined, but the app registration and initial migration still need to be completed. Other modules are pending to be completed.