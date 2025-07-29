# 🧠 Inventory Manager – Python Fundamentals & SOLID Principle Practice

This project is a well-structured Python learning repository designed to help beginners and intermediate developers master **core Python concepts** and apply **SOLID design principles** in real-world coding scenarios.

It includes categorized examples on control flow, data types, exception handling, file I/O, and a dedicated module for applying the **Single Responsibility Principle (SRP)** at the function and module level.

---

## 📚 Key Learning Objectives

- Grasp core Python syntax and features through hands-on examples.
- Apply clean code practices and modular design.
- Master the **Single Responsibility Principle** with real use cases.
- Learn error handling, file operations, and Git workflow.

---

## 📁 Folder Structure

```
inventory-manager/
├── Control_Flow/ # Conditional logic and loop examples
│ ├── conditional.py
│ └── loops.py
│
├── Datatypes/ # Built-in data types and operations
│ ├── list/
│ ├── set/
│ ├── tuple/
│ ├── dictionary/
│ └── strings/
│
├── SRP_Solid_Principle/ # Real-world use cases of SRP (Single Responsibility Principle)
│ ├── calc_area.py
│ ├── even.py
│ ├── place_order.py
│ ├── student_score.py
│ └── user_authentication.py
│
├── file_handling/ # Read/write examples for text and binary files
│ ├── binaryfile_program.py
│ ├── txtfile_program.py
│ ├── binaryfile.bin
│ └── test_textfile.txt
│
├── exception_handling/ # Error handling patterns and examples
│
├── primitive_data_type/ # Examples of fundamental Python types
│
├── GIt_Commands/ # Useful Git commands (commands.txt)
│
├── data_processing.py # Small data transformation example
├── data.csv # Sample CSV for practice
├── equality_and_identity.py # Comparison using == vs is
├── list_comprehension/ # Examples of list comprehension
├── hello.py # First Python test script
├── zen.py # The Zen of Python (PEP 20)
├── readme.md # Project documentation (this file)
├── .gitignore # Git ignore rules
└── venv/ # Python virtual environment (excluded from Git)
```


---

## 🔎 Highlights of SRP Implementations

| File                  | Responsibility Description                            |
|-----------------------|--------------------------------------------------------|
| `calc_area.py`        | Calculates area of different shapes                    |
| `place_order.py`      | Places customer orders (isolated from payment logic)   |
| `student_score.py`    | Manages student scoring and report generation          |
| `user_authentication.py` | Handles login and user verification                  |
| `even.py`             | Checks and prints even numbers from a list             |

Each file follows SRP by **doing only one thing** and doing it well — improving modularity and maintainability.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Git (for version control)

### Setup Instructions

1. **Clone the Repository**

```
git clone https://github.com/your-username/inventory-manager.git
cd inventory-manager
```

### Create & Activate Virtual Environment

```
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

## Run Any Python File
```
python3 Control_Flow/conditional.py
```
