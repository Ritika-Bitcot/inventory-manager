# Testing Setup
To run automated tests and check code quality, follow these steps:

## 1. Install Test Dependencies
```
pip install -r tests/test_requirements.txt
```

This installs:
pytest — Unit testing framework
pytest-cov — Coverage plugin for pytest

## 2. Running Tests
Run all tests:

```
pytest
```

## Run a specific test file:

```
pytest tests/test_core.py
```

Run tests with detailed output:
```
pytest -v
```
Show print/log output while testing:

```
pytest -s
```

## 3. Checking Code Coverage
Terminal coverage report showing missed lines:

```
pytest --cov=Week3 --cov-report=term-missing
```

Generate HTML coverage report:

```
pytest --cov=Week3 --cov-report=html
```

Open htmlcov/index.html in your browser to view the report.

## Testing Setup Summary

| Step                       | Command/Instruction                            |
| -------------------------- | ---------------------------------------------- |
| Install test dependencies  | `pip install -r tests/test_requirements.txt`   |
| Run all tests              | `pytest`                                       |
| Run specific test          | `pytest tests/test_core.py`                    |
| Coverage report (terminal) | `pytest --cov=Week3 --cov-report=term-missing` |
| Coverage report (HTML)     | `pytest --cov=Week3 --cov-report=html`         |


## Notes
-Always activate your virtual environment before running development or test commands.

-Use deactivate to exit the virtual environment.

-Make sure you run commands from the project root directory.

---