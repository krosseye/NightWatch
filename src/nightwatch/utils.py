import logging
import os
import platform
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
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "resources", relative_path
    )
