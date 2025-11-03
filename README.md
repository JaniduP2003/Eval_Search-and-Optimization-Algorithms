# Eval: Search and Optimization Algorithms

Author: Janidu Pabasara

University ID: IT23294998


## Overview

This repository contains implementations and evaluation utilities for classic search and optimization algorithms used in coursework and assignments. It includes student-facing implementations (skeletons and reference tests) for breadth-first search (BFS), iterative deepening search (IDS), A* search, simulated annealing (SA), and dynamic programming / linear programming examples.

Key files:
- `runner.py` — main evaluation runner that generates a grid, imports student modules, runs grading tests, and writes `results.json` and `problem.json`.
- `student_bfs.py`, `student_astar.py`, `student_ids.py`, `student_sa.py`, `student_lp_dp.py` — student implementations to complete/modify.
- `heuristics.py` — heuristic functions used by A* and evaluated by the runner.
- `common.py` — shared helpers.
- `problem.json`, `results.json` — sample outputs written by the runner.
- `results/` — directory with previous run artifacts.


## Requirements

- Python 3.8+ (tested with Python 3.11)
- No external packages are strictly required for the provided scripts. If you add dependencies, add a `requirements.txt` and use `pip install -r requirements.txt`.


## How to run (PowerShell on Windows)

Open PowerShell in the repository root (`c:\Users\ADMIN\Documents\GitHub\Eval_Search-and-Optimization-Algorithms`) and follow these steps.

Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

Run the evaluation runner (basic):

```powershell
python .\runner.py --student_id "IT23294998"
```

This will generate two files in the repository root:
- `problem.json` — the generated grid problem (rows, cols, start/goal, obstacles, seed)
- `results.json` — the detailed grading output for BFS, A*, IDS, SA, LP/DP and hidden checks

Run with optional arguments:

```powershell
# specify a seed, grid size, obstacle density, or layout
python .\runner.py --student_id "IT23294998" --seed "myseed" --rows 8 --cols 8 --density 0.25 --layout checkerboard
```

Available `--layout` options: `random` (default), `checkerboard`, `none` (no obstacles).


## How to test your implementations

1. Implement or modify the functions in the `student_*.py` files and `heuristics.py`.
2. Run the `runner.py` command above. The runner imports the `student_*` modules and executes grading functions.
3. Inspect `results.json` to see per-component outputs and scores.


## Notes and tips

- If you modify module names or move files, update `runner.py` import statements.
- For SA (simulated annealing), the runner calls `student_sa.simulated_annealing(...)` and expects either a path or a `(path, history)` tuple.
- For A*, BFS, and IDS the runner expects functions `astar`, `bfs`, and `ids` respectively with signatures matching the calls inside `runner.py` (see `grade_*` functions for exact expectations).


## Contact

Author: Janidu Pabasara

University ID: IT23294998

