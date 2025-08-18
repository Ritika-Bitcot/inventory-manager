# Week6 - Inventory Manager API

This folder contains the Week6 version of the Inventory Manager API built using **Flask**, **SQLAlchemy**, and **PostgreSQL**. The project demonstrates proper database integration and migration handling with **Flask-Migrate (Alembic)**.

---

## Features

- RESTful API with Flask
- PostgreSQL database integration via SQLAlchemy
- Alembic migrations for schema management
- Blueprint-based modular structure
- Environment-based configuration

---

---

## Setup

1. **Clone the repository** (if not already done):

```
git clone <repo-url>
cd inventory-manager/Week6
```

2. **Create a virtual environment and activate it**:

```
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**:

```
pip install -r requirements.txt
```

4. **Set environment variables**:

Create a .env file with:

```
DB_USER=postgres
DB_PASSWORD=root
DB_HOST=localhost
DB_PORT=5432
DB_NAME=inventory_db

DATABASE_URL=postgresql+psycopg2://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}

FLASK_APP=api.app
FLASK_ENV=development
```
Make sure PostgreSQL is running and the user/password/database exist.

5. **Database Setup**
Create database manually (if not exists):

```
CREATE DATABASE inventory_db;
```

Run migrations to create tables:

```
flask db init      # only if migrations folder is missing
flask db migrate -m "Initial migration"
flask db upgrade
```

Tables will also be created automatically if not exist when running flask db upgrade.

6. **Running the Application**
```
flask run
or
cd Week6/
python -m api.app
```

The API will be available at:

```
http://127.0.0.1:5000
Products API: http://127.0.0.1:5000/products
```

### Notes
Alembic script.py.mako is ignored in Git via .gitignore.

The project uses Blueprints for modular routing.

Models must be imported in migrations/env.py to detect schema changes during migration.

For any database changes, always run flask db migrate and flask db upgrade.
