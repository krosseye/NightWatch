import logging
import os
from tkinter import messagebox

logger = logging.getLogger(__name__)


def show_error(message):
    """Display an error message in a message box."""
    logger.error(str(message))
    messagebox.showinfo("NightWatch - Error", str(message), icon="error")


def show_info(message):
    """Display info message in a message box."""
    logger.info(str(message))
    messagebox.showinfo("NightWatch - Info", str(message), icon="info")


def resource_path(relative_path):
    """Get absolute path to resource (works for dev and bin)"""
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "resources", relative_path
    )
