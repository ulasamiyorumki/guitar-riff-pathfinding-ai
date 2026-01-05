import tkinter as tk

class InputPanel:
    def __init__(self, parent, solve_cb, next_cb, prev_cb, full_cb, play_cb):
        # Main container
        self.frame = tk.Frame(parent, bg="#1e1e1e", padx=30, pady=20)
        self.frame.pack(fill=tk.X)

        # Left side: Inputs and Controls
        self.left_side = tk.Frame(self.frame, bg="#1e1e1e")
        self.left_side.pack(side=tk.LEFT, fill=tk.Y)

        # --- Row 1: Riff Input, CALCULATE, and GENERATE RANDOM RIFF ---
        self.top_row = tk.Frame(self.left_side, bg="#1e1e1e")
        self.top_row.pack(fill=tk.X, pady=(0, 15))

        tk.Label(self.top_row, text="RIFF:", fg="#00ffcc", bg="#1e1e1e",
                 font=("Arial", 16, "bold")).pack(side=tk.LEFT)

        self.riff_entry = tk.Entry(self.top_row, width=35, font=("Consolas", 18),
                                   bg="#2d2d2d", fg="white", relief=tk.FLAT, insertbackground="white")
        self.riff_entry.pack(side=tk.LEFT, padx=15)

        # CALCULATE Button
        self.calc_btn = tk.Button(self.top_row, text="CALCULATE", bg="#00ffcc", fg="black",
                                  command=lambda: solve_cb(self.riff_entry.get()),
                                  font=("Arial", 12, "bold"), padx=20, pady=8)
        self.calc_btn.pack(side=tk.LEFT, padx=5)

        # GENERATE RANDOM RIFF Button
        self.random_btn = tk.Button(self.top_row, text="GENERATE RANDOM RIFF", bg="#f1c40f", fg="black",
                                    command=lambda: solve_cb("RANDOM_GENERATE"),
                                    font=("Arial", 12, "bold"), padx=15, pady=8)
        self.random_btn.pack(side=tk.LEFT, padx=5)

        # --- Row 2: Navigation and Action Buttons ---
        self.ctrl_row = tk.Frame(self.left_side, bg="#1e1e1e")
        self.ctrl_row.pack(fill=tk.X)

        btn_style = {"bg": "#d1d1d1", "fg": "black", "relief": tk.FLAT,
                     "font": ("Arial", 11, "bold"), "padx": 15, "pady": 10}

        # Navigation Buttons
        tk.Button(self.ctrl_row, text="PREV", command=prev_cb, **btn_style).pack(side=tk.LEFT, padx=2)
        tk.Button(self.ctrl_row, text="NEXT", command=next_cb, **btn_style).pack(side=tk.LEFT, padx=2)

        # SHOW FULL PATH Button (Black text on Pink background)
        tk.Button(self.ctrl_row, text="SHOW FULL PATH", command=full_cb,
                  bg="#ff0077", fg="black", font=("Arial", 11, "bold"),
                  padx=15, pady=10, relief=tk.FLAT).pack(side=tk.LEFT, padx=2)

        # PLAY Button
        tk.Button(self.ctrl_row, text="▶ PLAY", command=play_cb,
                  bg="#1abc9c", fg="black", font=("Arial", 11, "bold"),
                  padx=20, pady=10, relief=tk.FLAT).pack(side=tk.LEFT, padx=2)

        # Status Message (Log)
        self.log_label = tk.Label(self.left_side, text="Ready", fg="#888", bg="#1e1e1e",
                                  font=("Arial", 24, "italic"))
        self.log_label.pack(side=tk.BOTTOM, fill=tk.X, pady=(15, 0), anchor="w")

        # --- RIGHT SIDE: ANALYTICS DASHBOARD ---
        self.stats_frame = tk.Frame(self.frame, bg="#252525", padx=30, pady=20,
                                    highlightbackground="#444", highlightthickness=2)
        self.stats_frame.pack(side=tk.RIGHT, padx=20)

        self.stat_labels = {}
        stats_config = [
            ("Stretch Cost", "stretch"),
            ("String Shift", "string"),
            ("Penalty Count (+15)", "penalty_count"),
            ("TOTAL COST (A*)", "total")
        ]

        for label_text, key in stats_config:
            f = tk.Frame(self.stats_frame, bg="#252525")
            f.pack(fill=tk.X, pady=8)

            tk.Label(f, text=f"{label_text}:", fg="#aaa", bg="#252525",
                     font=("Arial", 18, "bold")).pack(side=tk.LEFT)

            val_font = ("Arial", 24, "bold")
            val_color = "#ff0077" if key == "total" else "#00ffcc"

            lbl = tk.Label(f, text="0.0", fg=val_color, bg="#252525", font=val_font)
            lbl.pack(side=tk.RIGHT, padx=(25, 0))
            self.stat_labels[key] = lbl

    def set_message(self, message, is_error=False):
        """Displays status or error messages in English."""
        color = "#ff4444" if is_error else "#00ffcc"
        self.log_label.config(text=message, fg=color)

    def update_stats(self, data):
        """Updates the dashboard values based on the results."""
        for key, value in data.items():
            if key in self.stat_labels:
                self.stat_labels[key].config(text=f"{value:.1f}")