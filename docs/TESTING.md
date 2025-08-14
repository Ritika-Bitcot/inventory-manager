# Testing Setup
To run automated tests and check code quality, follow these steps:

## 1. Install Test Dependencies
```
pip install -r tests/test_requirements.txt
```

This installs:
pytest — Unit testing framework
pytest-cov — Coverage plugin for pytest
Flask — For API testing

## 2. Running Tests
Run all tests:

```
pytest
```

## Run a specific test file:

```
pytest tests/test_core.py
pytest tests/test_inventory.py  # API tests

```

Run tests with detailed output:
```
pytest -v
```
Show print/log output while testing:

```
pytest -s
```

## 3️⃣ Running API Tests

Your API tests are in tests/test_inventory.py and require the Flask test client (already handled via conftest.py fixtures).

### Run all API tests:
```
pytest tests/test_inventory.py
```

### Run a specific API test (example: test creating a product):
```
pytest tests/test_inventory.py -k "test_create_and_get_product"
```

Run API tests with detailed output:
```
pytest -v tests/test_inventory.py
```

## 4. Checking Code Coverage
Terminal coverage report showing missed lines:

```
pytest --cov=Week3 --cov-report=term-missing
```

Generate HTML coverage report:

```
pytest --cov=Week3 --cov-report=html
```

Open htmlcov/index.html in your browser to view the report.

## 5.Testing Summary Table
| Step                       | Command/Instruction                                            |
| -------------------------- | -------------------------------------------------------------- |
| Install test dependencies  | `pip install -r tests/test_requirements.txt`                   |
| Run all tests              | `pytest`                                                       |
| Run specific test file     | `pytest tests/test_core.py` / `pytest tests/test_inventory.py` |
| Run API tests only         | `pytest tests/test_inventory.py`                               |
| Run tests with verbose log | `pytest -v`                                                    |
| Show print/log output      | `pytest -s`                                                    |
| Coverage report (terminal) | `pytest --cov=Week3 --cov-report=term-missing`                 |
| Coverage report (HTML)     | `pytest --cov=Week3 --cov-report=html`                         |


## Notes
Always activate your virtual environment before running development or test commands.
```
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

Use `deactivate` to exit the virtual environment.

Make sure you run commands from the project root directory.
---