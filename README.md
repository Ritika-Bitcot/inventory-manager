# 🧠 Inventory Manager – Learn Python Fundamentals & SOLID Principles

This repository is a beginner-to-intermediate friendly Python learning project. It helps you **master Python basics** and **apply clean coding practices** like the **Single Responsibility Principle (SRP)** through real-world, hands-on examples.

Whether you're new to Python or want to structure your learning with best practices, this project is for you!

---

## 📚 What You Will Learn

- ✅ Python fundamentals: variables, loops, conditionals, data types, file handling
- ✅ Clean code and modular design
- ✅ Exception handling & data validation with `try...except` and `pydantic`
- ✅ Applying **SOLID Principles** — especially **Single Responsibility Principle (SRP)**
- ✅ Working with real CSV files
- ✅ Using Git and `.gitignore`
- ✅ Writing reusable, maintainable code


---

## 📁 Folder Structure

```
inventory-manager/
├── tests/
│   ├── conftest.py
│   ├── test_core.py
│   ├── test_main.py
│   ├── test_models_using_fixtures.py
│   ├── test_models.py
│   └── test_requirements.txt

├── Week1&2/
│   ├── Control_Flow/
│   │   ├── conditional.py
│   │   └── loops.py
│   │
│   ├── csv_modules/
│   │   ├── contacts.csv
│   │   ├── people.csv
│   │   ├── program1.py
│   │   └── program2.py
│   │
│   ├── Datatypes/
│   │   ├── dictionary/
│   │   │   ├── basics.py
│   │   │   ├── methods.py
│   │   │   └── programs.py
│   │   ├── list/
│   │   │   ├── basics.py
│   │   │   ├── methods.py
│   │   │   └── programs.py
│   │   ├── set/
│   │   │   ├── basics.py
│   │   │   └── programs.py
│   │   ├── strings/
│   │   │   ├── basics.py
│   │   │   ├── methods.py
│   │   │   └── programs.py
│   │   └── tuple/
│   │       ├── basics.py
│   │       └── programs.py
│   │
│   ├── exception_handling/
│   │   ├── data_processing.py
│   │   ├── data_processing_using_pydantic.py
│   │   └── data.csv
│   │
│   ├── file_handling/
│   │   ├── binaryfile_program.py
│   │   ├── binaryfile.bin
│   │   ├── test_textfile.txt
│   │   └── txtfile_program.py
│   │
│   ├── Git_Commands/
│   │   └── commands.txt
│   │
│   ├── primitive_data_type/
│   │   ├── operators_and_fstring.py
│   │   └── variable_and_assignment.py
│   │
│   ├── process_data_inventory/
│   │   ├── inventory.csv
│   │   ├── low_stock_report.txt
│   │   ├── process_inventory.py
│   │   └── errors.log
│   │
│   ├── SRP_Solid_Principle/
│   │   ├── calc_area.py
│   │   ├── even.py
│   │   ├── log.txt
│   │   ├── place_order.py
│   │   ├── student_score.py
│   │   └── user_authentication.py
│   │
│   ├── list_comprehension.py
│   ├── equality_and_identity.py
│   ├── hello.py
│   └── zen.py
│
├── Week3/
│   ├──data
│   |   ├──products.csv
|   ├──__init__.py
│   ├── core.py
│   ├── errors.log
│   ├── low_stock_report.txt
│   ├── main.py
│   ├── models.py
│   ├── utils.py
|
├──.pre-commit-config.yaml
├── pyproject.toml
├── setup.cfg
├── README.md
├── .gitignore
├── venv/
└── requirements.txt

```

---
# 🔍 Notable Module Highlights
## 📦 process_data_inventory/ (Week2)
Real-world inventory data processing with validation.

Reads from inventory.csv.

### Uses:

pydantic for schema validation

try-except blocks for graceful error handling

### Outputs:

🧾 low_stock_report.txt — lists products below stock threshold

🐞 errors.log — logs rows with validation or type errors

🧱 SRP_Solid_Principle/ (Week2)
Practical, beginner-friendly implementations of the Single Responsibility Principle (SRP). Each file focuses on a single job or responsibility.

```
| File                     | Responsibility Description                         |
| ------------------------ | -------------------------------------------------- |
| `calc_area.py`           | Calculates area of different shapes                |
| `even.py`                | Filters and prints even numbers from a list        |
| `place_order.py`         | Handles order placement and basic record-keeping   |
| `student_score.py`       | Computes average scores and generates reports      |
| `user_authentication.py` | Manages user login and password verification logic |
```

🔎 Each file demonstrates the SRP by limiting itself to one clear purpose, promoting modularity and testability.

### 🧩 Week3/ – Modular Inventory Manager (SRP in Practice)
This folder restructures the Week2 inventory processor into a clean, modular Python package.
```
| File                   | Responsibility                                 |
| ---------------------- | ---------------------------------------------- |
| `main.py`              | Acts as the entry point to run the app         |
| `core.py`              | Contains core logic to process and filter data |
| `models.py`            | Defines Pydantic models for product validation |
| `utils.py`             | Logging helpers and reusable utilities         |
| `data/`                | CSV files used by the app                      |
| `low_stock_report.txt` | Report generated from processed data           |
| `errors.log`           | Error log capturing invalid records            |

```

🧱 This folder showcases SRP at the module level, where each file has a single, well-defined responsibility.


## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Git (for version control)


---

## 🔧 How to Set Up the Project (Step-by-Step)

### 1. ✅ Clone the Repository

```
git clone https://github.com/your-username/inventory-manager.git
cd inventory-manager
```

### 2. ✅ Create & Activate a Virtual Environment

```
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate      # On Linux/macOS
venv\Scripts\activate         # On Windows
```
### 3. ✅ Install Required Packages

```
pip install -r requirements.txt
```

## ▶️ How to Run the Programs
You can run any python3 filename.py file using Python from your terminal.


## 🗂️ Move Between Folders (Navigation Commands)

| Command                    | What It Does                              |
| -------------------------- | ----------------------------------------- |
| `ls` or `dir`              | Lists files in current folder             |
| `cd folder_name/`          | Moves into the folder                     |
| `cd ..`                    | Moves one level up                        |
| `pwd`                      | Shows your current location (Linux/macOS) |
| `cd Week1&2/Control_Flow/` | Go directly into nested folders           |
| `cd ../../`                | Move up 2 levels                          |

### ✅ Example 1: Run a Simple File from Week1&2
Example: Run the condition check script

```
cd Week1&2/Control_Flow/
python conditional.py
```

### ✅ Example 2: Run Inventory Processor (Week2 – Real-World Example)
```
cd ../../process_data_inventory/
python process_inventory.py
It processes inventory data and generates:

low_stock_report.txt

errors.log

```

### ✅ Example 3: Run the Modular Inventory App (Week3)

```
cd ../../../Week3/
python main.py
It uses modular design and separates logic across multiple files.
```

## 🧪 Testing
This project includes unit tests to ensure code reliability and correctness.

### Tests Added
tests/test_models.py: Contains test cases for validating product models and related logic.

### tests/test_requirements.txt: 
Lists dependencies required to run the tests separately.

Running Tests
### Install test dependencies:

```
pip install -r tests/test_requirements.txt
```
### Run tests using pytest:

```
pytest tests/test_models.py
```


### 🧰 Setup for Testing (Step-by-Step)
1. ✅ Switch to the appropriate branch
```
git checkout week4_day1
```
2. ✅ Activate your virtual environment
```
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```
3. ✅ Install test dependencies
```
pip install -r tests/test_requirements.txt
```
This installs:

pytest – Unit testing framework

pytest-cov – Code coverage plugin for pytest

### ▶️ How to Run Tests
✅ Run all tests
```
pytest
```
✅ Run a specific test file

```
pytest tests/test_core.py
```

✅ Run tests with detailed output
```
pytest -v
```
✅ Show print/log output while testing
```
pytest -s
```
### 🧩 Using Fixtures (conftest.py)
Fixtures are reusable setups shared between tests. They're defined in tests/conftest.py.

You can use them like this:

```
def test_product_model_valid(valid_product_data):
    product = ProductModel(**valid_product_data)
    assert product.name == "Pen"
You don’t need to import fixtures – pytest discovers and injects them automatically based on parameter names.
```

### 📊 Checking Code Coverage
You can verify how much of your code is covered by the tests using pytest-cov.

✅ Run with coverage
```
pytest --cov=Week3
```
✅ Show missing lines in terminal
```
pytest --cov=Week3 --cov-report=term-missing
```
✅ Generate HTML coverage report
```
pytest --cov=Week3 --cov-report=html
```
Then open this in your browser:

```
htmlcov/index.html
```
✅ Example Output
```
==================== test session starts ====================
collected 10 items

tests/test_core.py ....................              [100%]

---------- coverage: platform linux, Python 3.10 ----------
Name               Stmts   Miss  Cover   Missing
----------------------------------------------
Week3/core.py         45      0   100%
Week3/models.py       12      0   100%
Week3/main.py         10      0   100%
----------------------------------------------
TOTAL                 67      0   100%

================ 10 passed in 0.45s ==========================
```

### 🔁 Test Workflow Summary

# Activate virtual environment
```
source venv/bin/activate
```
# Install test dependencies
```
pip install -r tests/test_requirements.txt
```
# Run all tests
```
pytest
```
# Optional: Check test coverage
```
pytest --cov=Week3 --cov-report=term-missing
```

# 🛠️ Common Issues & Fixes
### Problem	Solution
**ModuleNotFoundError**	Make sure you're in the root project directory, or use python -m pytest
Coverage not shown	Make sure you're passing --cov=Week3
**ImportError** from Week3	Ensure __init__.py exists in Week3/

# 🧑‍💻 Who Should Run Tests?
✅ Everyone using this project should run the tests — especially when:

You modify or add features

You want to verify things didn’t break

You're learning testing with clean code and SRP



# 🧑‍💻 Who Is This For?
Beginners who want practical Python skills

Anyone interested in learning clean code practices

Students preparing for interviews or building foundational projects

Developers transitioning to more structured Python

# 💡 Learning Tips
✅ Start from Week1&2/ for fundamentals

🧪 Use print() and try editing inputs to explore effects

📝 Observe logs and output files to track program behavior

🚀 Revisit and refactor your code using SRP and other principles

# 🛠️ Tools Used
Python 3.10+

pydantic for validation

Git & GitHub

File I/O and CSV handling

# 🔗 Useful Commands

### Run a file
```
python path/to/file.py
```
### Install packages
```
pip install package-name
```
## Activate venv
```
source venv/bin/activate     # macOS/Linux
venv\Scripts\activate        # Windows
```
## Deactivate venv
```
deactivate
```

# 📩 Feedback
If you spot any bugs or want to suggest improvements, feel free to open an issue or submit a pull request.

Happy coding! 🚀