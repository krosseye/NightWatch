import logging
import os
import platform
import sys
from tkinter import messagebox


def show_error(message):
    """Display an error message in a message box."""
    logging.error(str(message))
    messagebox.showinfo("NightWatch - Error", str(message), icon="error")


def show_info(message):
    """Display info message in a message box."""
    logging.info(str(message))
    messagebox.showinfo("NightWatch - Info", str(message), icon="info")


def show_warning(message):
    """Display a warning message in a message box."""
    logging.warning(str(message))
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
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
        base_path = os.path.join(sys._MEIPASS, "resources")
    except Exception:
        current_dir = os.path.dirname(os.path.realpath(__file__))
        base_path = os.path.join(current_dir, "resources")
    return os.path.join(base_path, relative_path)
