# Week6 - Inventory Manager API

This folder contains the Week6 version of the Inventory Manager API built using **Flask**, **SQLAlchemy**, and **PostgreSQL**. The project demonstrates proper database integration and migration handling with **Flask-Migrate (Alembic)**.

---

## Features

1. RESTful API with Flask

2. PostgreSQL database integration via SQLAlchemy

3. Alembic migrations for schema management

4. Blueprint-based modular structure

5. Environment-based configuration

6. JWT Authentication with Access & Refresh tokens

---
## API Endpoints
### 📌 Authentication Endpoints
| Method | Endpoint         | Description                              | Payload Example                                    |
| ------ | ---------------- | ---------------------------------------- | -------------------------------------------------- |
| POST   | `/auth/register` | Register a new user                      | `{ "username": "ritika", "password": "pass123" }`  |
| POST   | `/auth/login`    | Login and get access + refresh token     | `{ "username": "ritika", "password": "pass123" }`  |
| POST   | `/auth/refresh`  | Refresh access token using refresh token | *Headers*: `Authorization: Bearer <refresh_token>` |


### 📌 Product Endpoints

| Method | Endpoint         | Description             | Payload Example                                                        |
| ------ | ---------------- | ----------------------- | ---------------------------------------------------------------------- |
| GET    | `/products`      | Get all products        | —                                                                      |
| GET    | `/products/<id>` | Get product by ID       | —                                                                      |
| POST   | `/products`      | Create new product      | `{ "name": "Milk", "category": "food", "quantity": 10, "price": 5.5 }` |
| PUT    | `/products/<id>` | Update existing product | `{ "name": "Milk", "quantity": 15 }`                                   |
| DELETE | `/products/<id>` | Delete product          | —                                                                      |
---

## Setup

1. **Clone the repository** (if not already done):

```
git clone <repo-url>
cd inventory-manager/Week6&7
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

JWT_SECRET_KEY=your_secret_key
JWT_ACCESS_TOKEN_EXPIRES=3600   # 1 hour
JWT_REFRESH_TOKEN_EXPIRES=86400 # 1 day
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

## API Endpoints
### 🔐 Authentication
**Register User**

POST /auth/register
```
{
  "username": "john",
  "password": "mypassword"
}
```

Response:
```
{
  "message": "User registered successfully"
}
```
**Login User**

POST /auth/login
```
{
  "username": "john",
  "password": "mypassword"
}
```

Response:
```
{
  "access_token": "jwt_access_token_here",
  "refresh_token": "jwt_refresh_token_here",
  "token_type": "bearer"
}
```
**Refresh Token**

3. POST /auth/refresh
```
{
  "refresh_token": "jwt_refresh_token_here"
}

```
Response:
```
{
  "access_token": "new_access_token_here",
  "token_type": "bearer"
}
```
## 📦 Products

All product endpoints require Authorization header with a valid Bearer access token.

### 1. Get All Products

**GET /products**

Response:
```
[
  {
    "id": 1,
    "name": "Milk",
    "category": "food",
    "quantity": 10,
    "price": 5.5
  },
  {
    "id": 2,
    "name": "Laptop",
    "category": "electronic",
    "quantity": 2,
    "price": 50000
  }
]
```
### 2. Get Single Product

**GET /products/<id>**

GET /products/1

Create Product

POST /products
```
{
  "name": "Book",
  "category": "book",
  "quantity": 5,
  "price": 299.99
}

```
Response:
```
{
  "id": 3,
  "name": "Book",
  "category": "book",
  "quantity": 5,
  "price": 299.99
}
```
### 3. Update Product

**PUT /products/<id>**
```
{
  "name": "Updated Book",
  "category": "book",
  "quantity": 8,
  "price": 349.99
}
```
### 4. Delete Product

**DELETE /products/<id>**

Response:
```
{
  "message": "Product deleted successfully"
}
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