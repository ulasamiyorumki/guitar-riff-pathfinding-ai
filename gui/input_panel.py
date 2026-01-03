import tkinter as tk


class InputPanel:
    def __init__(self, parent, solve_cb, next_cb, prev_cb, full_cb):
        # Main container with increased padding
        self.frame = tk.Frame(parent, bg="#1e1e1e", padx=30, pady=20)
        self.frame.pack(fill=tk.X)

        # Left side for user inputs and controls
        self.left_side = tk.Frame(self.frame, bg="#1e1e1e")
        self.left_side.pack(side=tk.LEFT, fill=tk.Y)

        # --- Row 1: Riff Input (Large) ---
        self.top_row = tk.Frame(self.left_side, bg="#1e1e1e")
        self.top_row.pack(fill=tk.X, pady=(0, 15))

        tk.Label(self.top_row, text="RIFF:", fg="#00ffcc", bg="#1e1e1e",
                 font=("Arial", 16, "bold")).pack(side=tk.LEFT)

        # Large entry field for notes
        self.riff_entry = tk.Entry(self.top_row, width=35, font=("Consolas", 18),
                                   bg="#2d2d2d", fg="white", relief=tk.FLAT, insertbackground="white")
        self.riff_entry.pack(side=tk.LEFT, padx=15)

        # Large Calculate button
        self.calc_btn = tk.Button(self.top_row, text="CALCULATE", bg="#00ffcc", fg="black",
                                  command=lambda: solve_cb(self.riff_entry.get()),
                                  font=("Arial", 12, "bold"), padx=25, pady=8)
        self.calc_btn.pack(side=tk.LEFT)

        # --- Row 2: Media Controls (Large) ---
        self.ctrl_row = tk.Frame(self.left_side, bg="#1e1e1e")
        self.ctrl_row.pack(fill=tk.X)

        btn_style = {"bg": "#d1d1d1", "fg": "black", "relief": tk.FLAT,
                     "font": ("Arial", 12, "bold"), "padx": 20, "pady": 10}

        tk.Button(self.ctrl_row, text="PREV", command=prev_cb, **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(self.ctrl_row, text="NEXT", command=next_cb, **btn_opt if 'btn_opt' in locals() else btn_style).pack(
            side=tk.LEFT, padx=5)

        tk.Button(self.ctrl_row, text="SHOW FULL PATH", command=full_cb,
                  bg="#ff0077", fg="black", font=("Arial", 12, "bold"),
                  padx=25, pady=10, relief=tk.FLAT).pack(side=tk.LEFT, padx=30)

        # Status Message area
        self.log_label = tk.Label(self.left_side, text="Ready", fg="#888", bg="#1e1e1e",
                                  font=("Arial", 12, "italic"))
        self.log_label.pack(side=tk.BOTTOM, fill=tk.X, pady=(15, 0), anchor="w")

        # --- RIGHT SIDE: ANALYTICS DASHBOARD (High Contrast) ---
        self.stats_frame = tk.Frame(self.frame, bg="#252525", padx=30, pady=20,
                                    highlightbackground="#444", highlightthickness=2)
        self.stats_frame.pack(side=tk.RIGHT, padx=20)

        self.stat_labels = {}
        # Configuration for display labels
        stats_config = [
            ("Stretch Cost", "stretch"),
            ("String Shift", "string"),
            ("Position Shift", "pos"),
            ("TOTAL SCORE", "total")
        ]

        for label_text, key in stats_config:
            f = tk.Frame(self.stats_frame, bg="#252525")
            f.pack(fill=tk.X, pady=8)

            tk.Label(f, text=f"{label_text}:", fg="#aaa", bg="#252525",
                     font=("Arial", 11, "bold")).pack(side=tk.LEFT)

            # Larger fonts for values, specially the Total Score
            val_font = ("Arial", 22, "bold") if key == "total" else ("Arial", 16, "bold")
            val_color = "#ff0077" if key == "total" else "#00ffcc"

            lbl = tk.Label(f, text="0.0", fg=val_color, bg="#252525", font=val_font)
            lbl.pack(side=tk.RIGHT, padx=(25, 0))
            self.stat_labels[key] = lbl

    def set_message(self, message, is_error=False):
        """Displays status or error messages in the log area."""
        color = "#ff4444" if is_error else "#00ffcc"
        self.log_label.config(text=message, fg=color)

    def update_stats(self, data):
        """Updates the dashboard values based on the AI results."""
        for key, value in data.items():
            if key in self.stat_labels:
                self.stat_labels[key].config(text=f"{value:.1f}")