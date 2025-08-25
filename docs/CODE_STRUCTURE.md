# Project Folder Structure

```
inventory-manager/
├── Week1&2/
│ ├── Control_Flow/
│ ├── csv_modules/
│ ├── Datatypes/
│ ├── exception_handling/
│ ├── file_handling/
│ ├── Git_Commands/
│ ├── primitive_data_type/
│ ├── process_data_inventory/
│ ├── SRP_Solid_Principle/
│ ├── list_comprehension.py
│ ├── equality_and_identity.py
│ ├── hello.py
│ └── zen.py
|
├── Week3/
│ ├── data/
│ ├── core.py
│ ├── main.py
│ ├── models.py
│ ├── utils.py
│ ├── errors.log
│ ├── low_stock_report.txt
│ └── init.py
|
├── Week4/
│ ├── conftest.py
│ ├── test_core.py
│ ├── test_main.py
│ ├── test_models_using_fixtures.py
│ ├── test_models.py
│ └── test_requirements.txt
|
├── Week5/
├── api/
│ ├── routes/
│ │   └── inventory.py  
│ ├── __init__.py
│ ├── app.py
├── Day1/
│ ├── hello.py
├── tests/
│ ├── __init__.py
│ ├── conftest.py
| ├── test_inventory.py
|
├── Week6&7/
│   ├── data/
│   │   ├── products.csv
│   ├── api/
│   │   ├── __init__.py
│   │   ├── app.py
│   │   ├── config.py
│   │   ├── models.py
│   |   ├── seed.py
│   |   ├── db.py
|   │   ├── schemas/ 
│   │   |   ├── __init__.py
│   |   |   ├── request.py
│   │   |   └── response.py
│   │   │   └── user.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   └── products.py
│   │   │   └── auth.py            
│   ├── tests/ 
│   │   |   ├── __init__.py
│   |   |   ├── conftest.py
│   │   |   └── test_models.py
│   │   |   └── test_products_api.py
│   │   |   └── test_seeds.py
│   └── migrations/
│   └── .env.example
│   └── README.md
|
├── .pre-commit-config.yaml
├── pyproject.toml
├── setup.cfg
├── README.md
├── .gitignore
├── venv/
└── requirements.txt
```

---

## Notable Module Highlights

### Week1&2 – process_data_inventory/

- Real-world inventory data processing with validation.
- Reads `inventory.csv`.
- Uses `pydantic` for schema validation.
- Uses `try-except` blocks for error handling.
- Outputs:  
  - `low_stock_report.txt` — lists products below stock threshold  
  - `errors.log` — logs rows with validation or type errors  

---

### Week1&2 – SRP_Solid_Principle/

Practical beginner-friendly implementations of the Single Responsibility Principle (SRP). Each file focuses on one responsibility:

| File                     | Responsibility Description                         |
|--------------------------|--------------------------------------------------|
| `calc_area.py`           | Calculates area of different shapes                |
| `even.py`                | Filters and prints even numbers from a list        |
| `place_order.py`         | Handles order placement and record-keeping         |
| `student_score.py`       | Computes average scores and generates reports      |
| `user_authentication.py` | Manages user login and password verification       |

---

### Week3 – Modular Inventory Manager

| File                   | Responsibility                                 |
|------------------------|-----------------------------------------------|
| `main.py`              | Entry point to run the app                     |
| `core.py`              | Core logic for processing and filtering data  |
| `models.py`            | Pydantic models for product validation         |
| `utils.py`             | Logging helpers and reusable utilities         |
| `data/`                | CSV files used by the app                       |
| `low_stock_report.txt` | Report generated from processed data           |
| `errors.log`           | Error log capturing invalid records            |

---

## Tests Folder (`tests/`)

The `tests/` directory contains test suites covering Week3 modules:

| Test File                   | Tests Coverage                          |
|-----------------------------|---------------------------------------|
| `test_core.py`              | Unit tests for `Week3/core.py`         |
| `test_models.py`            | Unit tests for `Week3/models.py`       |
| `test_main.py`              | Tests for application entrypoint `main.py` |
| `test_models_using_fixtures.py` | Extended tests for `models.py` using pytest fixtures |
| `conftest.py`               | pytest fixtures shared among tests     |

---
