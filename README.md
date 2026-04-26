# A modern, visually polished desktop interface for a Sudoku solver built using Python.

````markdown
## 🧾 Code Explanation for Beginners

This project is built with **Python** using a built-in library called **Tkinter**.

Tkinter is used to create desktop applications with windows, buttons, labels, dropdowns, sliders, and custom drawings.

---

## 1. Importing Tkinter

```python
import tkinter as tk
from tkinter import ttk
````

These lines import the tools needed to build the interface.

* `tkinter` is the main UI library.
* `ttk` gives access to styled widgets like dropdowns and sliders.

---

## 2. Puzzle Data

```python
PUZZLE = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    ...
]
```

This is the sample Sudoku puzzle.

Each row is a list of 9 numbers.

* Numbers from `1` to `9` are fixed puzzle values.
* `0` means the cell is empty.

---

## 3. Colors

```python
COLORS = {
    "background": "#0F172A",
    "primary": "#6366F1",
    ...
}
```

This dictionary stores all colors used in the interface.

Instead of writing color codes everywhere, the code gives each color a name.
This makes the UI easier to edit later.

Example:

```python
COLORS["primary"]
```

means the main accent color.

---

## 4. Fonts

```python
FONT_TITLE = ("Segoe UI", 26, "bold")
FONT_CELL = ("Segoe UI", 24, "bold")
```

These variables define the font styles used across the app.

This keeps typography consistent.

---

## 5. Rounded Rectangle Function

```python
def rounded_rect(canvas, x1, y1, x2, y2, radius, **kwargs):
```

Tkinter does not support rounded rectangles by default, so this function draws them manually.

It is used for:

* Cards
* Buttons
* UI elements

---

## 6. Card Component

```python
class Card(tk.Frame):
```

This creates reusable UI containers (cards).

Each card has:

* Rounded corners
* Background color
* Padding
* Shadow effect

Used for:

* Sudoku board
* Controls panel
* Stats section

---

## 7. Modern Button Component

```python
class ModernButton(tk.Canvas):
```

This creates custom buttons instead of using default Tkinter buttons.

Why?
To achieve:

* Rounded corners
* Hover effects
* Press animations
* Modern look

Button types:

* `primary` → main action (Solve)
* `secondary` → secondary action (Step)
* `ghost` → minimal action (Load)
* `danger` → destructive action (Clear)

---

## 8. Sudoku Board

```python
class SudokuBoard(tk.Canvas):
```

This draws the Sudoku grid using a canvas.

It renders:

* 9×9 cells
* Grid lines (thicker every 3 cells)
* Numbers inside cells

It also shows example UI states:

* Selected cell
* AI candidate cell
* Recently filled cell

These are **visual only**, not functional.

---

## 9. Main Application

```python
class ModernSudokuUI(tk.Tk):
```

This is the main app window.

It controls:

* Layout
* Sections
* UI structure

---

## 10. Header

```python
def _build_header(self):
```

Top section of the app:

* App title
* Subtitle
* Status indicator (Idle)

---

## 11. Main Layout

```python
def _build_main(self):
```

Creates a 2-column layout:

```
Left → Sudoku Board
Right → Controls + Stats
```

The board is larger because it's the main focus.

---

## 12. Board Section

```python
def _build_board_card(self, parent):
```

Contains:

* Section title
* Description
* Sudoku grid

---

## 13. Side Panel

```python
def _build_side_panel(self, parent):
```

Right side of the UI.

Includes stacked cards:

* Solver Configuration
* Controls
* Agent Stats
* Cell Legend

---

## 14. Solver Configuration

```python
def _solver_card(self, parent):
```

Includes:

* Algorithm dropdown
* Speed slider

UI only — no logic yet.

---

## 15. Controls

```python
def _controls_card(self, parent):
```

Buttons:

* Solve
* Step
* Load Puzzle
* Clear

These are placeholders (no functionality).

---

## 16. Agent Stats

```python
def _stats_card(self, parent):
```

Displays sample data:

* Assignments
* Backtracks
* Execution Time
* Status

Used to show how results would appear.

---

## 17. Cell Legend

```python
def _legend_card(self, parent):
```

Explains grid colors:

* Given value
* Empty cell
* AI candidate
* Selected cell
* Recently filled

---

## 18. Running the App

```python
if __name__ == "__main__":
    app = ModernSudokuUI()
    app.mainloop()
```

This starts the application.

* Creates the window
* Keeps it running
