import tkinter as tk


class FretboardView:
    def __init__(self, parent,fretboard):
        # Canvas initialization with dark background
        self.canvas = tk.Canvas(parent, bg="#121212", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Configuration
        self.fretboard = fretboard
        self.strings = fretboard.num_strings
        self.frets = fretboard.num_frets
        self.string_order = list(range(1,self.strings+1))

        self.margin_x = 60
        self.margin_y = 50
        self.cell_width = 0
        self.cell_height = 0

        self.full_path = []
        self.current_step = 0

        # Redraw when window is resized
        self.canvas.bind("<Configure>", lambda e: self.draw_fretboard())

    def draw_fretboard(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        usable_w = w - (self.margin_x * 2)
        usable_h = h - (self.margin_y * 2)

        self.cell_width = usable_w / self.frets
        self.cell_height = usable_h / (self.strings - 1)

        # Draw Fretboard Wood Background
        self.canvas.create_rectangle(
            self.margin_x, self.margin_y,
            self.margin_x + usable_w, self.margin_y + usable_h,
            fill="#2a2a2a", outline="#444", width=2
        )

        # Draw Frets (Vertical Lines)
        for f in range(self.frets + 1):
            x = self.margin_x + (f * self.cell_width)
            # Nut (Fret 0) is thicker and golden
            color = "#f1c40f" if f == 0 else "#888"
            width = 4 if f == 0 else 2
            self.canvas.create_line(x, self.margin_y, x, self.margin_y + usable_h, fill=color, width=width)

            # Fret Numbers
            if f > 0:
                self.canvas.create_text(x - (self.cell_width / 2), self.margin_y - 20,
                                        text=str(f), fill="#666", font=("Arial", 10))

        # Draw Strings (Horizontal Lines)
        for i, s_num in enumerate(self.string_order):
            y = self.margin_y + (i * self.cell_height)
            # Higher strings are thinner visually
            thickness = 1 + (i * 0.5)
            self.canvas.create_line(self.margin_x, y, self.margin_x + usable_w, y, fill="#d1d1d1", width=thickness)

            # String Labels on the left
            string_names = {1: "E", 2: "B", 3: "G", 4: "D", 5: "A", 6: "E"}
            self.canvas.create_text(self.margin_x - 30, y, text=string_names[s_num], fill="#888",
                                    font=("Arial", 12, "bold"))

        # Redraw path if it exists
        if self.full_path:
            self.draw_single_step(self.current_step)

    def load_path(self, path):
        self.full_path = path
        self.current_step = 0

    def show_full_path(self):
        self.current_step = len(self.full_path)
        self.draw_single_step(self.current_step)

    def next_step(self):
        if self.current_step < len(self.full_path):
            self.current_step += 1
            self.draw_single_step(self.current_step)

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.draw_single_step(self.current_step)

    def draw_single_step(self, step_count):
        self.canvas.delete("path_element")
        if self.cell_width <= 0 or step_count == 0:
            return

        prev_coords = None
        # Track overlapping notes to offset them slightly
        coord_counts = {}

        for step, (s_num, fret) in enumerate(self.full_path[:step_count], 1):
            row_index = self.string_order.index(s_num)

            if not self.fretboard.is_valid_position(s_num, fret):
                continue

            # Calculate X (Handle open strings at fret 0)
            if fret == 0:
                base_x = self.margin_x - 15
            else:
                base_x = self.margin_x + (fret * self.cell_width) - (self.cell_width / 2)

            base_y = self.margin_y + (row_index * self.cell_height)

            # Offset logic for same-position notes
            coord_counts[(s_num, fret)] = coord_counts.get((s_num, fret), 0) + 1
            offset = (coord_counts[(s_num, fret)] - 1) * 5
            x, y = base_x + offset, base_y + offset

            # Draw Connection Line (Arrow)
            if prev_coords:
                self.canvas.create_line(
                    prev_coords[0], prev_coords[1], x, y,
                    fill="#ff0077", width=2, arrow=tk.LAST,
                    dash=(4, 2), tags="path_element"
                )

            # Draw Note Circle
            self.canvas.create_oval(
                x - 14, y - 14, x + 14, y + 14,
                fill="#ff0077", outline="white", width=2, tags="path_element"
            )

            # Draw Step Number
            self.canvas.create_text(
                x, y, text=str(step), fill="white",
                font=("Arial", 11, "bold"), tags="path_element"
            )

            prev_coords = (x, y)