"""
NightWatch helps create a sleep-friendly environment by managing your devices during bedtime.

This script sets up the UI and handles the countdown timer.
"""

import logging
import math
import sys
import time
import tkinter as tk
from collections.abc import Callable
from tkinter import ttk

import sv_ttk

from nightwatch.actions import pause_media, shutdown_system, sleep_system
from nightwatch.utils import resource_path, show_error

logger = logging.getLogger(__name__)

ACTIONS: dict[str, Callable[[], None]] = {
    "Pause": pause_media,
    "Sleep": sleep_system,
    "Shutdown": shutdown_system,
}


class NightWatch(tk.Tk):
    """
    Main application class (subclass of tk.Tk)

    This class initializes and sets up the main application window and its components.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setup_window()

        self.lbf_action = ttk.LabelFrame(self, text="Select Action", padding=5)
        self.cmb_actions = ttk.Combobox(
            self.lbf_action, values=list(ACTIONS), state="readonly"
        )
        self.hour_string = tk.StringVar(value="00")
        self.minute_string = tk.StringVar(value="00")
        self.second_string = tk.StringVar(value="00")
        self.lbf_input_time = ttk.LabelFrame(self, text="Enter Time", padding=5)
        self.lbl_hours = ttk.Label(self.lbf_input_time, text="Hours")
        self.lbl_minutes = ttk.Label(self.lbf_input_time, text="Minutes")
        self.lbl_seconds = ttk.Label(self.lbf_input_time, text="Seconds")
        self.txt_hours = self.create_time_entry(
            self.lbf_input_time, self.hour_string, 0
        )
        self.txt_minutes = self.create_time_entry(
            self.lbf_input_time, self.minute_string, 1
        )
        self.txt_seconds = self.create_time_entry(
            self.lbf_input_time, self.second_string, 2
        )
        self.prg_time_left = ttk.Progressbar(self.lbf_input_time)
        self.btn_start_timer = ttk.Button(
            self, text="Start Timer", command=self.run_timer, padding=5
        )

        self.setup_ui()
        self.deadline = 0.0
        self.tick_id: str | None = None

    def setup_window(self) -> None:
        """Set up the main application window."""
        self.title("NightWatch")
        self.resizable(height=False, width=False)
        self.iconphoto(True, tk.PhotoImage(file=resource_path("icon.png")))

        width, height = 252, 275
        screen_width, screen_height = (
            self.winfo_screenwidth(),
            self.winfo_screenheight(),
        )
        x, y = (screen_width / 2) - (width / 2), (screen_height / 2) - (height / 2)
        self.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

        if len(sys.argv) > 1 and sys.argv[1].lower() in [
            "--light-theme",
            "--light-mode",
        ]:
            sv_ttk.set_theme("light")
        else:
            sv_ttk.set_theme("dark")

    def setup_ui(self) -> None:
        """Set up the user interface elements."""
        self.lbf_action.grid(row=0, columnspan=3, padx=10, pady=5, sticky="ew")
        self.cmb_actions.current(0)
        self.cmb_actions.bind(
            "<<ComboboxSelected>>", lambda _: self.cmb_actions.selection_clear()
        )
        self.cmb_actions.grid(row=0, padx=6, pady=10, sticky="ew")

        self.lbf_input_time.grid(row=1, columnspan=3, padx=10, pady=0, sticky="ew")
        self.lbl_hours.grid(column=0, row=0, padx=10, pady=5)
        self.lbl_minutes.grid(column=1, row=0, padx=10, pady=5)
        self.lbl_seconds.grid(column=2, row=0, padx=10, pady=5)
        self.prg_time_left.grid(row=5, columnspan=3, padx=10, pady=10, sticky="ew")

        self.btn_start_timer.grid(row=6, columnspan=3, padx=10, pady=10, sticky="ew")

    def create_time_entry(
        self, parent: tk.Misc, string_var: tk.StringVar, column: int
    ) -> ttk.Entry:
        """Create a time entry widget."""
        entry = ttk.Entry(parent, width=3, textvariable=string_var, justify="center")
        entry.bind("<FocusIn>", lambda event: event.widget.select_range(0, "end"))
        entry.grid(column=column, row=1, padx=15, pady=5)
        return entry

    def run_timer(self) -> None:
        """Start the timer based on user input."""
        hours_text = self.hour_string.get()
        minutes_text = self.minute_string.get()
        seconds_text = self.second_string.get()
        try:
            hours = int(hours_text)
            minutes = int(minutes_text)
            seconds = int(seconds_text)
        except ValueError:
            show_error(f"Invalid value: {hours_text}h {minutes_text}m {seconds_text}s")
            self.reset_timer()
            return

        total = hours * 3600 + minutes * 60 + seconds
        if min(hours, minutes, seconds) < 0 or total <= 0:
            show_error(
                f"A positive duration is required: {hours}h {minutes}m {seconds}s"
            )
            self.reset_timer()
            return

        self.deadline = time.monotonic() + total
        self.prg_time_left.configure(maximum=total)
        self.btn_start_timer.config(text="Cancel", command=self.reset_timer)
        self.tick()

    def tick(self) -> None:
        """Show the time left, and run the action once it reaches zero."""
        remaining = max(0, math.ceil(self.deadline - time.monotonic()))
        hours, rest = divmod(remaining, 3600)
        minutes, seconds = divmod(rest, 60)
        self.hour_string.set(f"{hours:02d}")
        self.minute_string.set(f"{minutes:02d}")
        self.second_string.set(f"{seconds:02d}")
        self.prg_time_left.configure(value=remaining)

        if remaining:
            self.tick_id = self.after(200, self.tick)
        else:
            self.tick_id = None
            self.execute_action()

    def reset_timer(self) -> None:
        """Reset the timer to its initial state."""
        if self.tick_id:
            self.after_cancel(self.tick_id)
            self.tick_id = None

        self.hour_string.set("00")
        self.minute_string.set("00")
        self.second_string.set("00")
        self.prg_time_left.configure(value=0)
        logger.info("Timer has been reset")
        self.btn_start_timer.config(text="Start Timer", command=self.run_timer)

    def execute_action(self) -> None:
        """Execute the selected action after the countdown ends."""
        ACTIONS[self.cmb_actions.get()]()
        self.btn_start_timer.config(text="Start Timer", command=self.run_timer)


def main() -> None:
    """Launch NightWatch."""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    NightWatch().mainloop()
