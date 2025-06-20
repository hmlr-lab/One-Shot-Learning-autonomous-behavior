# 🧠 Maze Learning with PyGol

This repository demonstrates how to train an Inductive Logic Programming (ILP) model using [PyGol](https://github.com/danyvarghese/PyGol), to learn movement rules in a grid-based maze. It generates examples from a 2×2 maze, learns using symbolic logic rules, and tests the learned rules on larger grids (5×5, 9×9, 16×16) for pathfinding tasks.

---

## 📂 Project Structure

```
.
├── main.py                 # Main script for example generation, learning, and testing
├── maze_util.py           # Utility functions for grid handling and move generation
├── PyGol_Final_20240718/  # PyGol library (custom ILP implementation)
├── maze_maps/             # Grid files named 1.py to 15.py (for 5×5, 9×9, and 16×16 mazes)
└── README.md              # Project documentation (this file)
```

---

## ⚙️ Requirements

- Python 3.8+
- PyGol (imported locally in this repo)
- `itertools`, `sys`, and standard Python libraries

Install external dependencies if required:
```bash
pip install tqdm
```

---

## 🚀 How to Run

1. **Ensure directory structure** is intact:
    - `maze_util.py` and `PyGol_Final_20240718/` must be available in the parent and grandparent folders respectively.
    - Grid files (e.g., `1.py`, `2.py`, ...) should be accessible via `load_map_data`.

2. **Execute the script**:
```bash
python3 main.py
```

3. **Output**:
    - Displays generated training examples
    - Trains an ILP model to learn grid navigation rules
    - Evaluates the learned model on various grid sizes and prints path statistics

---

## 🧪 Learning Pipeline

- **Example Generation**: Generates one-step and two-step move examples from a 2×2 maze.
- **ILP Model Training**: Uses PyGol to induce movement rules from the examples.
- **Testing**: Applies the learned rules to unseen mazes (5×5, 9×9, 16×16) and measures path efficiency.

---

## 📊 Sample Output

```
------------ Training Stage Starts ------------
...
------------- Learned Rules -------------
  Number of rules: 3
   1 move(X,Y):-up(X,Y).
   2 move(X,Y):-right(X,Y).
   3 move(X,Y):-right(X,Z),up(Z,Y).
...
------------ Testing Stage Starts ------------

     Grid Size: 5
     File Name  Final Path     Total Path (Inc. Back Tracking)
     -------------------------------------------------------
     1.py       7              10
     2.py       6              8
...
```

---

## 📌 Notes

- The model generalizes well from a tiny 2×2 training set to larger unseen mazes.
- Rules are human-readable, enabling symbolic interpretability of decisions.

---

## 📜 License

This project is for research and educational use. For commercial or extended use of PyGol, please refer to [PyGol Licensing](https://github.com/danyvarghese/PyGol#license).

---
