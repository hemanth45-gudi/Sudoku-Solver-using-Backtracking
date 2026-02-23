# 🧩 Sudoku Solver — Production Edition (DSA Project)

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Status](https://img.shields.io/badge/Status-Production-success)
![DSA](https://img.shields.io/badge/DSA-Backtracking-orange)
![License](https://img.shields.io/badge/License-MIT-green)

A **production-level Sudoku Solver** built using the **Backtracking algorithm** with step-by-step visualization, performance analysis, and interactive GUI.

This project demonstrates core **Data Structures and Algorithms (DSA)** concepts including recursion, constraint satisfaction, and efficient search space exploration with a modern user interface and professional software architecture.

---

## ⭐ Key Features

* 🔄 Step-by-step solving visualization
* ⚡ Backtracking + DLX algorithm support
* 📊 Performance metrics (steps, time, backtracks)
* ✏️ Custom puzzle input
* 🎨 Modern production UI with theme support
* 🔍 Constraint validation (row, column, subgrid)
* 🧪 Unit testing support
* 🌐 FastAPI backend support
* 🐳 Docker deployment ready

---

## 📌 Project Overview

This project implements a Sudoku Solver that automatically solves a given 9×9 puzzle while satisfying all Sudoku constraints.

The solver demonstrates:

* Recursion and backtracking techniques
* Constraint satisfaction problem solving
* Algorithm visualization
* Performance measurement
* Interactive user experience

It combines algorithmic concepts with real-world application design.

---

## 🚀 Quick Start

### Clone Repository

```
git clone <your-repo-url>
cd sudoku-solver
```

### Install Dependencies

```
pip install -r requirements.txt
```

### Run Application

```
python main.py
```

---

## 📸 Demo

### Solver Interface

![Sudoku-solver-using-Backtracking](assets/p1-project.png)
![Sudoku-solver-using-Backtracking](assets/p2-project.png)
![Sudoku-solver-using-Backtracking](assets/p3-project.png)


```
assets/images/solver.png
```

### Custom Puzzle Input

![Sudoku-solver-using-Backtracking](assets/p4-project.png)
![Sudoku-solver-using-Backtracking](assets/p5-project.png)
![Sudoku-solver-using-Backtracking](assets/p6-project.png)
![Sudoku-solver-using-Backtracking](assets/p7-project.png)
![Sudoku-solver-using-Backtracking](assets/p8-project.png)
![Sudoku-solver-using-Backtracking](assets/p9-project.png)
![Sudoku-solver-using-Backtracking](assets/p10-project.png)


```
assets/images/input.png
```

---

## ⚙️ Technologies Used

* Python
* Backtracking Algorithm
* Dancing Links (DLX)
* Recursion
* Pygame (GUI)
* FastAPI (API Support)
* Pytest (Testing)
* Docker (Deployment)
* Logging & Configuration Management
* Matrix / 2D Array Operations

---

## 🧠 Algorithm — Backtracking

Backtracking is a recursive problem-solving technique that explores all possible solutions and eliminates invalid ones.

Sudoku is a **constraint satisfaction problem** where each solution must satisfy:

* Row constraint
* Column constraint
* 3×3 subgrid constraint

### Working Steps

1. Find an empty cell in the grid.
2. Try values from 1–9.
3. Check if the value satisfies Sudoku rules.
4. Place value if valid.
5. Recursively solve remaining cells.
6. If no solution exists, backtrack and try another value.

---

## 🧠 Data Structures Used

* **2D Matrix** → Sudoku grid representation
* **Recursion Stack** → Function calls during solving
* **Constraint Checking Functions** → Rule validation

---

## ⭐ Features in Detail

### 🔄 Visualization

* Highlights current cell
* Shows number placement
* Displays backtracking process
* Adjustable solving speed

### 📊 Performance Metrics

* Counts recursive calls
* Tracks backtracking steps
* Measures execution time
* Displays solving statistics

### ✏️ Custom Puzzle Input

* Manual puzzle entry
* Accepts values 1–9
* Empty cells represented as 0
* Input validation with error detection

### 🔍 Constraint Validation

* Row validation
* Column validation
* 3×3 subgrid validation

---

## 📝 Input Format

* Sudoku represented as 9×9 grid
* Empty cells represented using `0`
* Solver fills all empty cells while maintaining constraints

---

## 📊 Time & Space Complexity

### Time Complexity

Worst case: **O(9^(n²))** for an n×n grid.

Backtracking explores possible values but prunes invalid paths early.

### Space Complexity

**O(n²)** due to board storage and recursion stack.

---

## 📂 Project Structure

```
Sudoku-Solver/
│
├── src/
│   ├── api/           # FastAPI backend
│   ├── solver/        # Solver algorithms
│   ├── gui/           # GUI implementation
│   └── utils/         # Helper functions & configs
│
├── tests/             # Unit tests
├── assets/            # Images and icons
├── docs/              # Documentation
├── main.py            # Entry point
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🌍 Applications

* Puzzle solving systems
* Constraint satisfaction problems
* AI problem solving
* Game development
* Scheduling and optimization systems

---

## ⚠️ Limitations

* Designed primarily for 9×9 Sudoku
* Performance varies with puzzle difficulty

---

## 🚀 Future Improvements

* Support for different grid sizes
* Advanced heuristics (MRV, forward checking)
* Web-based Sudoku interface
* Performance comparison across algorithms

---

## 👨‍💻 Author

**Hemanth Gudi**

---
