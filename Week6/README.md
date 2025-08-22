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
DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password
DB_HOST=your_db_host
DB_PORT=your_db_port
DB_NAME=your_database_name

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

## 7. Seed the Database with Sample Products

After running migrations and creating tables, you can populate the database from the CSV file.

1. Set the FLASK_APP to the seed module:

```
export FLASK_APP=api.seed       # Linux/macOS
$env:FLASK_APP="api.seed"       # Windows PowerShell
```
Run the seed command:

```
flask seed-db
```
You should see output like:
```
Database seeded successfully.
```
Verify data:

```
flask shell
>>> from api.models import Product, FoodProduct, ElectronicProduct, BookProduct
>>> Product.query.all()
```

## 8. Testing

The project uses pytest for automated testing.

**Run all tests**:
```
pytest
```

**Run a specific test file**:
```
pytest tests/test_models.py -vv
```

**Run a single test function**:
```
pytest tests/test_models.py::test_product_total_value_and_serialize -vv
```

**Run tests with coverage report**:
```
pytest --cov=api --cov-report=term-missing
```

**Test Database**

By default, tests use an in-memory SQLite database (sqlite:///:memory:) for speed and isolation.

PostgreSQL can also be used for integration testing by setting the environment variable:

export TEST_DB_URI=postgresql://user:pass@localhost/test_db


This allows switching between lightweight unit tests and real DB integration tests.

### Notes
Alembic script.py.mako is ignored in Git via .gitignore.

The project uses Blueprints for modular routing.

Models must be imported in migrations/env.py to detect schema changes during migration.

For any database changes, always run flask db migrate and flask db upgrade.

The CSV file should be located at Week6/data/products.csv.

Make sure PostgreSQL is running and your database URI in .env is correct.
