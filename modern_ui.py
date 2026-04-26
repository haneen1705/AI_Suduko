import tkinter as tk
from tkinter import ttk


PUZZLE = [
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
    "background": "#0F172A",
    "surface": "#111827",
    "card": "#1E293B",
    "card_light": "#243247",
    "primary": "#6366F1",
    "primary_hover": "#7477FF",
    "success": "#22C55E",
    "success_soft": "#123829",
    "warning": "#FACC15",
    "warning_soft": "#3D3211",
    "danger": "#EF4444",
    "danger_soft": "#3A1D25",
    "text": "#F8FAFC",
    "muted": "#94A3B8",
    "grid": "#334155",
    "grid_heavy": "#64748B",
    "input": "#0B1220",
    "input_hover": "#111C2F",
    "given": "#263449",
}

FONT_TITLE = ("Segoe UI", 26, "bold")
FONT_SUBTITLE = ("Segoe UI", 11)
FONT_SECTION = ("Segoe UI", 15, "bold")
FONT_BODY = ("Segoe UI", 11)
FONT_SMALL = ("Segoe UI", 10)
FONT_CELL = ("Segoe UI", 24, "bold")


def rounded_rect(canvas, x1, y1, x2, y2, radius, **kwargs):
    """Draw a rounded rectangle on a Tk canvas."""
    points = [
        x1 + radius,
        y1,
        x2 - radius,
        y1,
        x2,
        y1,
        x2,
        y1 + radius,
        x2,
        y2 - radius,
        x2,
        y2,
        x2 - radius,
        y2,
        x1 + radius,
        y2,
        x1,
        y2,
        x1,
        y2 - radius,
        x1,
        y1 + radius,
        x1,
        y1,
    ]
    return canvas.create_polygon(points, smooth=True, splinesteps=24, **kwargs)


class Card(tk.Frame):
    """Rounded dark surface with subtle shadow."""

    def __init__(self, parent, bg=COLORS["card"], radius=18, padding=22, **kwargs):
        requested_width = kwargs.pop("width", 0)
        requested_height = kwargs.pop("height", 0)
        super().__init__(parent, bg=COLORS["background"], **kwargs)
        self.bg_color = bg
        self.radius = radius
        self.padding = padding
        canvas_options = {"bg": COLORS["background"], "highlightthickness": 0, "bd": 0}
        if requested_width:
            canvas_options["width"] = requested_width
        if requested_height:
            canvas_options["height"] = requested_height
        self.canvas = tk.Canvas(self, **canvas_options)
        self.canvas.pack(fill="both", expand=True)
        self.content = tk.Frame(self.canvas, bg=bg)
        self.window = self.canvas.create_window(padding, padding, anchor="nw", window=self.content)
        self.canvas.bind("<Configure>", self._draw)

    def _draw(self, event):
        self.canvas.delete("shape")
        width = event.width
        height = event.height
        rounded_rect(
            self.canvas,
            4,
            6,
            width - 2,
            height - 1,
            self.radius,
            fill="#080D18",
            outline="",
            tags="shape",
        )
        rounded_rect(
            self.canvas,
            1,
            1,
            width - 5,
            height - 6,
            self.radius,
            fill=self.bg_color,
            outline="#263449",
            width=1,
            tags="shape",
        )
        self.canvas.tag_lower("shape")
        self.canvas.coords(self.window, self.padding, self.padding)
        self.canvas.itemconfigure(
            self.window,
            width=max(1, width - self.padding * 2 - 6),
            height=max(1, height - self.padding * 2 - 8),
        )


class ModernButton(tk.Canvas):
    """Canvas button with rounded corners and hover state. UI only."""

    def __init__(self, parent, text, variant="primary", height=44, **kwargs):
        super().__init__(parent, height=height, bg=COLORS["card"], highlightthickness=0, bd=0, cursor="hand2", **kwargs)
        self.text = text
        self.variant = variant
        self.height = height
        self.hover = False
        self.bind("<Configure>", lambda _event: self._draw())
        self.bind("<Enter>", self._enter)
        self.bind("<Leave>", self._leave)
        self.bind("<ButtonPress-1>", self._press)
        self.bind("<ButtonRelease-1>", self._release)

    def _palette(self):
        if self.variant == "primary":
            return COLORS["primary_hover"] if self.hover else COLORS["primary"], COLORS["text"], ""
        if self.variant == "danger":
            return COLORS["danger_soft"], COLORS["danger"], COLORS["danger"]
        if self.variant == "ghost":
            return COLORS["card_light"] if self.hover else COLORS["card"], COLORS["text"], COLORS["grid"]
        return COLORS["card_light"] if self.hover else COLORS["surface"], COLORS["text"], COLORS["grid"]

    def _draw(self, pressed=False):
        self.delete("all")
        width = max(1, self.winfo_width())
        y_offset = 2 if pressed else 0
        fill, fg, outline = self._palette()
        rounded_rect(self, 1, 1 + y_offset, width - 2, self.height - 2 + y_offset, 12, fill=fill, outline=outline, width=1)
        self.create_text(width / 2, self.height / 2 + y_offset, text=self.text, fill=fg, font=("Segoe UI", 11, "bold"))

    def _enter(self, _event):
        self.hover = True
        self._draw()

    def _leave(self, _event):
        self.hover = False
        self._draw()

    def _press(self, _event):
        self._draw(pressed=True)

    def _release(self, _event):
        self._draw()


class SudokuBoard(tk.Canvas):
    """Static board mockup with sample visual states."""

    def __init__(self, parent):
        super().__init__(parent, bg=COLORS["card"], highlightthickness=0, bd=0)
        self.bind("<Configure>", lambda _event: self.draw())

    def draw(self):
        self.delete("all")
        size = min(self.winfo_width(), self.winfo_height()) - 24
        if size <= 0:
            return

        x0 = (self.winfo_width() - size) / 2
        y0 = (self.winfo_height() - size) / 2
        cell = size / 9

        selected = (0, 2)
        ai_candidate = (2, 4)
        recent_fill = (6, 0)

        rounded_rect(self, x0 - 10, y0 - 10, x0 + size + 10, y0 + size + 10, 18, fill=COLORS["surface"], outline="")

        for row in range(9):
            for col in range(9):
                x1 = x0 + col * cell
                y1 = y0 + row * cell
                x2 = x1 + cell
                y2 = y1 + cell

                value = PUZZLE[row][col]
                fill = COLORS["input"]
                outline = COLORS["grid"]
                width = 1
                text_color = COLORS["text"]

                if value:
                    fill = COLORS["given"]
                    text_color = COLORS["text"]
                if (row, col) == selected:
                    fill = COLORS["input_hover"]
                    outline = COLORS["primary"]
                    width = 3
                if (row, col) == ai_candidate:
                    fill = COLORS["warning_soft"]
                    outline = COLORS["warning"]
                    width = 2
                if (row, col) == recent_fill:
                    fill = COLORS["success_soft"]
                    outline = COLORS["success"]
                    width = 2

                self.create_rectangle(x1, y1, x2, y2, fill=fill, outline=outline, width=width)

                if value:
                    self.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(value), fill=text_color, font=FONT_CELL)
                elif (row, col) == ai_candidate:
                    self.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="4", fill=COLORS["warning"], font=("Segoe UI", 18, "bold"))
                elif (row, col) == recent_fill:
                    self.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="9", fill=COLORS["success"], font=FONT_CELL)

        for index in range(10):
            line_width = 3 if index % 3 == 0 else 1
            color = COLORS["grid_heavy"] if index % 3 == 0 else COLORS["grid"]
            pos = x0 + index * cell
            self.create_line(pos, y0, pos, y0 + size, fill=color, width=line_width)
            pos = y0 + index * cell
            self.create_line(x0, pos, x0 + size, pos, fill=color, width=line_width)


class ModernSudokuUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Sudoku Solver")
        self.geometry("1400x850")
        self.minsize(1180, 760)
        self.configure(bg=COLORS["background"])

        self.solver_mode = tk.StringVar(value="Backtracking + MRV")
        self.speed = tk.DoubleVar(value=55)

        self._configure_styles()
        self._build_header()
        self._build_main()

    def _configure_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "Modern.TCombobox",
            fieldbackground=COLORS["surface"],
            background=COLORS["surface"],
            foreground=COLORS["text"],
            arrowcolor=COLORS["muted"],
            bordercolor=COLORS["grid"],
            lightcolor=COLORS["grid"],
            darkcolor=COLORS["grid"],
            padding=10,
        )
        style.map("Modern.TCombobox", fieldbackground=[("readonly", COLORS["surface"])])
        style.configure(
            "Modern.Horizontal.TScale",
            background=COLORS["card"],
            troughcolor=COLORS["surface"],
            bordercolor=COLORS["grid"],
            lightcolor=COLORS["primary"],
            darkcolor=COLORS["primary"],
        )

    # Header
    def _build_header(self):
        header = tk.Frame(self, bg=COLORS["background"], height=96)
        header.pack(fill="x", padx=36, pady=(28, 12))
        header.pack_propagate(False)

        title_area = tk.Frame(header, bg=COLORS["background"])
        title_area.pack(side="left", fill="y")
        tk.Label(title_area, text="AI Sudoku Solver", bg=COLORS["background"], fg=COLORS["text"], font=FONT_TITLE).pack(anchor="w")
        tk.Label(
            title_area,
            text="Constraint Satisfaction Problem Visualizer",
            bg=COLORS["background"],
            fg=COLORS["muted"],
            font=FONT_SUBTITLE,
        ).pack(anchor="w", pady=(4, 0))

        pill = tk.Frame(header, bg=COLORS["surface"], highlightthickness=1, highlightbackground=COLORS["grid"])
        pill.pack(side="right", pady=18)
        tk.Label(pill, text="Idle", bg=COLORS["surface"], fg=COLORS["success"], font=("Segoe UI", 10, "bold"), padx=18, pady=8).pack()

    # Main two-column layout
    def _build_main(self):
        main = tk.Frame(self, bg=COLORS["background"])
        main.pack(fill="both", expand=True, padx=36, pady=(0, 36))
        main.columnconfigure(0, weight=7, uniform="main")
        main.columnconfigure(1, weight=3, uniform="main")
        main.rowconfigure(0, weight=1)

        self._build_board_card(main)
        self._build_side_panel(main)

    def _build_board_card(self, parent):
        card = Card(parent, bg=COLORS["card"], padding=24)
        card.grid(row=0, column=0, sticky="nsew", padx=(0, 24))
        card.content.rowconfigure(1, weight=1)
        card.content.columnconfigure(0, weight=1)

        top = tk.Frame(card.content, bg=COLORS["card"])
        top.grid(row=0, column=0, sticky="ew", pady=(0, 18))
        tk.Label(top, text="Puzzle Board", bg=COLORS["card"], fg=COLORS["text"], font=("Segoe UI", 18, "bold")).pack(side="left")
        tk.Label(top, text="9x9 standard Sudoku", bg=COLORS["card"], fg=COLORS["muted"], font=FONT_SMALL).pack(side="right")

        board = SudokuBoard(card.content)
        board.grid(row=1, column=0, sticky="nsew")

    def _build_side_panel(self, parent):
        panel_shell = tk.Frame(parent, bg=COLORS["background"])
        panel_shell.grid(row=0, column=1, sticky="nsew")
        panel_shell.rowconfigure(0, weight=1)
        panel_shell.columnconfigure(0, weight=1)

        canvas = tk.Canvas(panel_shell, bg=COLORS["background"], highlightthickness=0, bd=0)
        canvas.grid(row=0, column=0, sticky="nsew")

        panel = tk.Frame(canvas, bg=COLORS["background"])
        panel_window = canvas.create_window((0, 0), window=panel, anchor="nw")

        def update_scroll_region(_event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def fit_panel_width(event):
            canvas.itemconfigure(panel_window, width=event.width)

        panel.bind("<Configure>", update_scroll_region)
        canvas.bind("<Configure>", fit_panel_width)
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))
        panel.columnconfigure(0, weight=1)

        self._solver_card(panel).grid(row=0, column=0, sticky="ew", pady=(0, 18))
        self._controls_card(panel).grid(row=1, column=0, sticky="ew", pady=(0, 18))
        self._stats_card(panel).grid(row=2, column=0, sticky="ew", pady=(0, 18))
        self._legend_card(panel).grid(row=3, column=0, sticky="ew")

    # Right column cards
    def _solver_card(self, parent):
        card = Card(parent, bg=COLORS["card"], padding=20, height=215)
        tk.Label(card.content, text="Solver Configuration", bg=COLORS["card"], fg=COLORS["text"], font=FONT_SECTION).pack(anchor="w")

        combo = ttk.Combobox(
            card.content,
            textvariable=self.solver_mode,
            values=("Backtracking + MRV", "Forward Checking", "Constraint Propagation", "MRV + Degree Heuristic"),
            state="readonly",
            style="Modern.TCombobox",
            font=FONT_BODY,
        )
        combo.pack(fill="x", pady=(16, 16))

        label_row = tk.Frame(card.content, bg=COLORS["card"])
        label_row.pack(fill="x")
        for text, anchor in (("Slow", "w"), ("Normal", "center"), ("Fast", "e")):
            tk.Label(label_row, text=text, bg=COLORS["card"], fg=COLORS["muted"], font=FONT_SMALL).pack(side="left", expand=True, anchor=anchor)

        ttk.Scale(card.content, from_=0, to=100, variable=self.speed, style="Modern.Horizontal.TScale").pack(fill="x", pady=(8, 0))
        return card

    def _controls_card(self, parent):
        card = Card(parent, bg=COLORS["card"], padding=20, height=320)
        tk.Label(card.content, text="Controls", bg=COLORS["card"], fg=COLORS["text"], font=FONT_SECTION).pack(anchor="w")

        ModernButton(card.content, "Solve", variant="primary").pack(fill="x", pady=(16, 10))

        row = tk.Frame(card.content, bg=COLORS["card"])
        row.pack(fill="x")
        row.columnconfigure((0, 1), weight=1)
        ModernButton(row, "Step", variant="secondary").grid(row=0, column=0, sticky="ew", padx=(0, 6))
        ModernButton(row, "Load Puzzle", variant="ghost").grid(row=0, column=1, sticky="ew", padx=(6, 0))

        ModernButton(card.content, "Clear", variant="danger").pack(fill="x", pady=(10, 12))
        tk.Label(
            card.content,
            text="Step through the algorithm to visualize decisions.",
            bg=COLORS["card"],
            fg=COLORS["muted"],
            font=FONT_SMALL,
            wraplength=360,
            justify="left",
        ).pack(anchor="w")
        return card

    def _stats_card(self, parent):
        card = Card(parent, bg=COLORS["card"], padding=20, height=310)
        tk.Label(card.content, text="Agent Stats", bg=COLORS["card"], fg=COLORS["text"], font=FONT_SECTION).pack(anchor="w")

        grid = tk.Frame(card.content, bg=COLORS["card"])
        grid.pack(fill="x", pady=(16, 0))
        grid.columnconfigure((0, 1), weight=1)

        metrics = [
            ("Assignments", "120"),
            ("Backtracks", "8"),
            ("Execution Time", "0.23s"),
            ("Current Status", "Idle"),
        ]
        for index, (label, value) in enumerate(metrics):
            box = tk.Frame(grid, bg=COLORS["surface"], highlightthickness=1, highlightbackground=COLORS["grid"])
            box.grid(row=index // 2, column=index % 2, sticky="ew", padx=(0, 8) if index % 2 == 0 else (8, 0), pady=(0, 14))
            tk.Label(box, text=label, bg=COLORS["surface"], fg=COLORS["muted"], font=FONT_SMALL).pack(anchor="w", padx=12, pady=(9, 2))
            tk.Label(box, text=value, bg=COLORS["surface"], fg=COLORS["text"], font=("Segoe UI", 15, "bold")).pack(anchor="w", padx=12, pady=(0, 9))
        return card

    def _legend_card(self, parent):
        card = Card(parent, bg=COLORS["card"], padding=20, height=285)
        tk.Label(card.content, text="Cell Legend", bg=COLORS["card"], fg=COLORS["text"], font=FONT_SECTION).pack(anchor="w")

        items = [
            ("Given Value", COLORS["given"], COLORS["grid"]),
            ("Empty Cell", COLORS["input"], COLORS["grid"]),
            ("AI Candidate", COLORS["warning_soft"], COLORS["warning"]),
            ("Selected Cell", COLORS["input_hover"], COLORS["primary"]),
            ("Recently Filled", COLORS["success_soft"], COLORS["success"]),
        ]
        for label, fill, outline in items:
            row = tk.Frame(card.content, bg=COLORS["card"])
            row.pack(fill="x", pady=(16 if label == "Given Value" else 10, 0))
            swatch = tk.Canvas(row, width=28, height=28, bg=COLORS["card"], highlightthickness=0)
            swatch.pack(side="left")
            rounded_rect(swatch, 2, 2, 26, 26, 7, fill=fill, outline=outline, width=2)
            tk.Label(row, text=label, bg=COLORS["card"], fg=COLORS["muted"], font=FONT_BODY).pack(side="left", padx=12)
        return card


if __name__ == "__main__":
    app = ModernSudokuUI()
    app.mainloop()
