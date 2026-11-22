import logging
import os
from tkinter import messagebox

logger = logging.getLogger(__name__)


def show_error(message: str) -> None:
    """Display an error message in a message box."""
    logger.error(message)
    messagebox.showerror("NightWatch - Error", message)


def show_info(message: str) -> None:
    """Display info message in a message box."""
    logger.info(message)
    messagebox.showinfo("NightWatch - Info", message)


def resource_path(relative_path: str) -> str:
    """Get absolute path to resource (works for dev and bin)"""
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "resources", relative_path
    )
