# Quick Serve

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
| `is_active` | `Boolean` | Default True; stores the service state |
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

## Current Status

The database models are defined but needs modifications like location track inside User table and other. Other modules are pending to be completed.