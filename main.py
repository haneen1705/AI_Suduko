import tkinter as tk
from tkinter import ttk


SAMPLE_PUZZLE = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

COLORS = {
    "bg": "#15343a",
    "bg_dark": "#0d2227",
    "scanline": "#1c464c",
    "panel": "#e7d49b",
    "panel_light": "#f4e7b8",
    "panel_dark": "#9a7b45",
    "ink": "#1f2424",
    "muted": "#5c604f",
    "grid": "#151a19",
    "grid_heavy": "#050807",
    "cell": "#f8edc1",
    "cell_alt": "#eedca5",
    "given": "#b9a36b",
    "given_fg": "#172222",
    "hover": "#fff6d2",
    "focus": "#ffb347",
    "ai": "#8fdc8a",
    "ai_glow": "#e7ffd8",
    "green": "#4f9a59",
    "green_dark": "#2d6136",
    "orange": "#d87328",
    "orange_dark": "#8a411d",
    "danger": "#b54538",
    "cream": "#fff8d8",
}

FONT_TITLE = ("Courier New", 24, "bold")
FONT_SECTION = ("Courier New", 12, "bold")
FONT_UI = ("Courier New", 10, "bold")
FONT_SMALL = ("Courier New", 9)
FONT_CELL = ("Courier New", 24, "bold")


class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, _event=None):
        if self.tip:
            return
        x = self.widget.winfo_rootx() + 16
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 8
        self.tip = tk.Toplevel(self.widget)
        self.tip.overrideredirect(True)
        self.tip.configure(bg=COLORS["grid_heavy"])
        self.tip.geometry(f"+{x}+{y}")
        tk.Label(
            self.tip,
            text=self.text,
            bg=COLORS["grid_heavy"],
            fg=COLORS["cream"],
            font=FONT_SMALL,
            padx=10,
            pady=7,
        ).pack()

    def hide(self, _event=None):
        if self.tip:
            self.tip.destroy()
            self.tip = None


class RetroButton(tk.Button):
    def __init__(self, master, variant="secondary", **kwargs):
        palette = {
            "primary": (COLORS["green"], "white", COLORS["green_dark"]),
            "secondary": (COLORS["orange"], "white", COLORS["orange_dark"]),
            "tertiary": (COLORS["panel_light"], COLORS["ink"], COLORS["panel_dark"]),
            "danger": (COLORS["danger"], "white", "#772c25"),
        }
        bg, fg, active = palette[variant]
        super().__init__(
            master,
            bg=bg,
            fg=fg,
            activebackground=active,
            activeforeground=fg,
            relief="raised",
            bd=3,
            overrelief="sunken",
            cursor="hand2",
            font=FONT_UI,
            highlightthickness=1,
            highlightbackground=COLORS["grid_heavy"],
            padx=12,
            pady=9,
            **kwargs,
        )
        self.default_bg = bg
        self.active_bg = active
        self.bind("<Enter>", self._hover)
        self.bind("<Leave>", self._leave)
        self.bind("<ButtonPress-1>", self._press)
        self.bind("<ButtonRelease-1>", self._release)

    def _hover(self, _event=None):
        self.configure(bg=self.active_bg)

    def _leave(self, _event=None):
        self.configure(bg=self.default_bg, relief="raised")

    def _press(self, _event=None):
        self.configure(relief="sunken")

    def _release(self, _event=None):
        self.configure(relief="raised")


class SudokuUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Sudoku Solver")
        self.geometry("1180x760")
        self.minsize(1040, 680)
        self.configure(bg=COLORS["bg"])

        self.cells = []
        self.cell_kind = [["empty" for _ in range(9)] for _ in range(9)]
        self.selected_cell = None
        self.hover_cell = None
        self.algorithm = tk.StringVar(value="Backtracking + MRV")
        self.speed = tk.StringVar(value="Normal")
        self.status = tk.StringVar(value="UI preview only")
        self.assignments = tk.StringVar(value="120")
        self.backtracks = tk.StringVar(value="8")
        self.elapsed = tk.StringVar(value="0.23s")
        self.progress = tk.IntVar(value=64)

        self._configure_styles()
        self._build_layout()
        self._load_puzzle(SAMPLE_PUZZLE)

    def _configure_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "Retro.TCombobox",
            fieldbackground=COLORS["panel_light"],
            background=COLORS["panel"],
            foreground=COLORS["ink"],
            arrowcolor=COLORS["ink"],
            bordercolor=COLORS["grid_heavy"],
            lightcolor=COLORS["panel_light"],
            darkcolor=COLORS["panel_dark"],
            padding=8,
        )
        style.configure(
            "Retro.Horizontal.TProgressbar",
            background=COLORS["green"],
            troughcolor=COLORS["panel_light"],
            bordercolor=COLORS["grid_heavy"],
            lightcolor=COLORS["green"],
            darkcolor=COLORS["green_dark"],
        )

    def _build_layout(self):
        self._build_header()

        body = tk.Frame(self, bg=COLORS["bg"])
        body.pack(fill="both", expand=True, padx=24, pady=22)
        body.columnconfigure(0, weight=7, uniform="layout")
        body.columnconfigure(1, weight=3, uniform="layout")
        body.rowconfigure(0, weight=1)

        self._build_board_area(body)
        self._build_control_panel(body)

    def _build_header(self):
        header = tk.Frame(self, bg=COLORS["bg_dark"], height=78, highlightthickness=2, highlightbackground=COLORS["grid_heavy"])
        header.pack(fill="x")
        header.pack_propagate(False)

        left = tk.Frame(header, bg=COLORS["bg_dark"])
        left.pack(side="left", fill="y", padx=24)
        tk.Label(left, text="AI SUDOKU SOLVER", bg=COLORS["bg_dark"], fg=COLORS["cream"], font=FONT_TITLE).pack(anchor="w", pady=(13, 0))
        tk.Label(left, text="CSP TERMINAL // BACKTRACKING // MRV // FORWARD CHECKING", bg=COLORS["bg_dark"], fg="#9bc7bd", font=FONT_SMALL).pack(anchor="w")

        signal = tk.Frame(header, bg=COLORS["bg_dark"])
        signal.pack(side="right", padx=24)
        tk.Label(signal, text="READY", bg=COLORS["green"], fg="white", font=FONT_UI, padx=14, pady=8, relief="sunken", bd=2).pack(pady=18)

    def _build_board_area(self, parent):
        area = tk.Frame(parent, bg=COLORS["bg"])
        area.grid(row=0, column=0, sticky="nsew", padx=(0, 22))
        area.rowconfigure(1, weight=1)
        area.columnconfigure(0, weight=1)

        top = tk.Frame(area, bg=COLORS["bg"])
        top.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        tk.Label(top, text="PUZZLE GRID", bg=COLORS["bg"], fg=COLORS["cream"], font=FONT_SECTION).pack(side="left")
        tk.Label(top, textvariable=self.status, bg=COLORS["bg"], fg="#9bc7bd", font=FONT_SMALL).pack(side="right")

        board_panel = self._panel(area, COLORS["panel"], pad=16)
        board_panel.grid(row=1, column=0, sticky="nsew")
        board_panel.rowconfigure(0, weight=1)
        board_panel.columnconfigure(0, weight=1)

        board_wrap = tk.Frame(board_panel, bg=COLORS["grid_heavy"], bd=0)
        board_wrap.grid(row=0, column=0, sticky="nsew")
        for i in range(9):
            board_wrap.rowconfigure(i, weight=1, uniform="sudoku")
            board_wrap.columnconfigure(i, weight=1, uniform="sudoku")

        for row in range(9):
            row_cells = []
            for col in range(9):
                cell = tk.Entry(
                    board_wrap,
                    justify="center",
                    font=FONT_CELL,
                    bg=self._base_bg(row, col),
                    fg=COLORS["ink"],
                    insertbackground=COLORS["orange"],
                    relief="flat",
                    bd=0,
                    highlightthickness=2,
                    highlightbackground=COLORS["grid"],
                    highlightcolor=COLORS["focus"],
                    width=2,
                    disabledforeground=COLORS["given_fg"],
                )
                xpad = (3 if col % 3 == 0 else 1, 3 if col == 8 else 1)
                ypad = (3 if row % 3 == 0 else 1, 3 if row == 8 else 1)
                cell.grid(row=row, column=col, sticky="nsew", padx=xpad, pady=ypad)
                cell.bind("<FocusIn>", lambda _event, r=row, c=col: self._select_cell(r, c))
                cell.bind("<Enter>", lambda _event, r=row, c=col: self._hover_grid(r, c))
                cell.bind("<Leave>", lambda _event: self._clear_hover())
                cell.bind("<KeyPress>", lambda _event: "break")
                row_cells.append(cell)
            self.cells.append(row_cells)

    def _build_control_panel(self, parent):
        panel = tk.Frame(parent, bg=COLORS["bg"])
        panel.grid(row=0, column=1, sticky="nsew")
        panel.columnconfigure(0, weight=1)

        self._solver_section(panel).grid(row=0, column=0, sticky="ew", pady=(0, 16))
        self._controls_section(panel).grid(row=1, column=0, sticky="ew", pady=(0, 16))
        self._speed_section(panel).grid(row=2, column=0, sticky="ew", pady=(0, 16))
        self._stats_section(panel).grid(row=3, column=0, sticky="ew")

    def _solver_section(self, parent):
        section = self._section(parent, "1. SOLVER MODE")
        combo = ttk.Combobox(
            section,
            textvariable=self.algorithm,
            values=[
                "Backtracking",
                "Backtracking + MRV",
                "Forward Checking",
                "Constraint Propagation",
                "MRV + Degree Heuristic",
            ],
            state="readonly",
            style="Retro.TCombobox",
            font=FONT_UI,
        )
        combo.pack(fill="x", padx=16, pady=(2, 14))

        hint = tk.Label(section, text="?", bg=COLORS["orange"], fg="white", font=FONT_UI, width=3, relief="raised", bd=2, cursor="question_arrow")
        hint.place(relx=1.0, x=-50, y=12)
        Tooltip(hint, "Backtracking + MRV chooses constrained cells first for faster solving.")
        return section

    def _controls_section(self, parent):
        section = self._section(parent, "2. CONTROLS")
        buttons = tk.Frame(section, bg=COLORS["panel"])
        buttons.pack(fill="x", padx=16, pady=(0, 16))
        buttons.columnconfigure((0, 1), weight=1)

        RetroButton(buttons, text="[>] SOLVE", variant="primary", command=self._noop).grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        RetroButton(buttons, text="[|] STEP", variant="secondary", command=self._noop).grid(row=1, column=0, sticky="ew", padx=(0, 6), pady=(0, 10))
        RetroButton(buttons, text="[R] LOAD", variant="tertiary", command=self._noop).grid(row=1, column=1, sticky="ew", padx=(6, 0), pady=(0, 10))
        RetroButton(buttons, text="[X] CLEAR", variant="danger", command=self._noop).grid(row=2, column=0, columnspan=2, sticky="ew")
        return section

    def _speed_section(self, parent):
        section = self._section(parent, "3. SPEED")
        options = tk.Frame(section, bg=COLORS["panel"])
        options.pack(fill="x", padx=16, pady=(0, 16))
        options.columnconfigure((0, 1, 2), weight=1)
        for col, label in enumerate(("Slow", "Normal", "Fast")):
            rb = tk.Radiobutton(
                options,
                text=label.upper(),
                value=label,
                variable=self.speed,
                indicatoron=False,
                bg=COLORS["panel_light"],
                fg=COLORS["ink"],
                selectcolor=COLORS["orange"],
                activebackground=COLORS["orange"],
                activeforeground="white",
                font=FONT_SMALL,
                relief="raised",
                bd=2,
                padx=8,
                pady=8,
            )
            rb.grid(row=0, column=col, sticky="ew", padx=(0 if col == 0 else 6, 0))
        return section

    def _stats_section(self, parent):
        section = self._section(parent, "4. AGENT STATS")
        stats = [
            ("Assignments", self.assignments),
            ("Backtracks", self.backtracks),
            ("Time", self.elapsed),
        ]
        for label, variable in stats:
            row = tk.Frame(section, bg=COLORS["panel"])
            row.pack(fill="x", padx=16, pady=(0, 8))
            tk.Label(row, text=label.upper(), bg=COLORS["panel"], fg=COLORS["muted"], font=FONT_SMALL).pack(side="left")
            tk.Label(row, textvariable=variable, bg=COLORS["panel"], fg=COLORS["ink"], font=("Courier New", 14, "bold")).pack(side="right")

        ttk.Progressbar(section, maximum=100, variable=self.progress, style="Retro.Horizontal.TProgressbar").pack(fill="x", padx=16, pady=(4, 16), ipady=3)
        return section

    def _section(self, parent, title):
        frame = self._panel(parent, COLORS["panel"], pad=0)
        tk.Label(frame, text=title, bg=COLORS["panel"], fg=COLORS["ink"], font=FONT_SECTION).pack(anchor="w", padx=16, pady=(14, 12))
        return frame

    def _panel(self, parent, bg, pad=16):
        frame = tk.Frame(
            parent,
            bg=bg,
            highlightthickness=2,
            highlightbackground=COLORS["grid_heavy"],
            highlightcolor=COLORS["grid_heavy"],
            padx=pad,
            pady=pad,
        )
        return frame

    def _base_bg(self, row, col):
        return COLORS["cell_alt"] if (row // 3 + col // 3) % 2 else COLORS["cell"]

    def _load_puzzle(self, puzzle):
        for row in range(9):
            for col in range(9):
                value = puzzle[row][col]
                cell = self.cells[row][col]
                cell.configure(state="normal")
                cell.delete(0, tk.END)
                if value:
                    cell.insert(0, str(value))
                    self.cell_kind[row][col] = "given"
                    cell.configure(bg=COLORS["given"], fg=COLORS["given_fg"], readonlybackground=COLORS["given"], state="readonly")
                else:
                    self.cell_kind[row][col] = "empty"
                    cell.configure(bg=self._base_bg(row, col), fg=COLORS["ink"], state="normal")
        self.status.set("UI preview only")

    def _clear_board(self):
        self._noop()

    def _select_cell(self, row, col):
        self.selected_cell = (row, col)
        self._paint_grid()

    def _hover_grid(self, row, col):
        self.hover_cell = (row, col)
        self._paint_grid()

    def _clear_hover(self):
        self.hover_cell = None
        self._paint_grid()

    def _paint_grid(self):
        active = self.selected_cell
        hover = self.hover_cell
        for row in range(9):
            for col in range(9):
                cell = self.cells[row][col]
                kind = self.cell_kind[row][col]
                if kind == "given":
                    bg = COLORS["given"]
                elif kind == "ai":
                    bg = COLORS["ai_glow"]
                else:
                    bg = self._base_bg(row, col)

                if hover and (row == hover[0] or col == hover[1]) and kind != "given":
                    bg = COLORS["hover"]
                if active == (row, col):
                    bg = COLORS["focus"] if kind != "given" else COLORS["given"]
                cell.configure(bg=bg)

    def _noop(self):
        return None


if __name__ == "__main__":
    app = SudokuUI()
    app.mainloop()
