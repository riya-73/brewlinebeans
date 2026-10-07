# Database migrations

The application currently initializes tables for a zero-configuration demo. Production deployments should use Alembic migrations.

The repository now includes `alembic.ini` and the migration dependency. Generate and apply migrations with:

```bash
alembic init migrations
alembic revision --autogenerate -m 'initial Brewline schema'
alembic upgrade head
```

The schema additions in this phase are backward-compatible for fresh databases and include users, sales, sale lines and audit logs. Do not use `create_all` as the deployment migration strategy once a shared PostgreSQL database contains real data.
