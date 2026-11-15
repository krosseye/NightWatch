import logging
import os
import platform
import sys
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


def show_warning(message):
    """Display a warning message in a message box."""
    logger.warning(str(message))
    messagebox.showinfo("NightWatch - Warning", str(message), icon="warning")


def get_os():
    """Determines the name of the operating system."""
    os_name = platform.system()
    return os_name


def check_root_privileges():
    """Checks if the script has root privileges."""
    try:
        if os.geteuid() != 0:
            show_warning(
                "This program needs root privileges to sleep or shutdown.\n\nYou can still pause media."
            )
            return
    except AttributeError:
        pass  # On Windows, os.geteuid() is not defined


def resource_path(relative_path):
    """Get absolute path to resource (works for dev and bin)"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.realpath(__file__)))
    return os.path.join(base_path, "resources", relative_path)
