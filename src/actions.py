"""
This script handles the actions to perform at end of the countdown timer.
"""

import logging
import os

import pyautogui

from utils import check_root_privileges, get_os, show_error, show_info


def _run_command(command):
    """Executes an OS-specific command."""
    logging.info("Executing command: %s", command)
    exit_code = os.system(command)
    if exit_code != 0:
        show_error(f"Failed to execute command: {command}\n\nExit code: {exit_code}")


def pause_media():
    """Pauses the media playback using pyautogui to simulate the play/pause button press."""
    pyautogui.press("playpause")
    show_info("Media has been paused.")


def sleep_system():
    """Puts the system to sleep based on the operating system."""
    current_os = get_os()
    logging.info("Going to sleep...")
    if current_os == "Windows":
        _run_command("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    elif current_os == "Darwin":
        check_root_privileges()
        _run_command("pmset sleepnow")
    elif current_os == "Linux":
        check_root_privileges()
        _run_command("systemctl suspend")
    else:
        show_error("Unable to suspend, unknown operating system.")


def shutdown_system():
    """Shuts down the system based on the operating system."""
    current_os = get_os()
    logging.info("Shutting down...")
    if current_os == "Windows":
        _run_command("shutdown /s /t 0")
    elif current_os in ["Darwin", "Linux"]:
        check_root_privileges()
        _run_command("sudo shutdown -h now")
    else:
        show_error("Unable to shutdown, unknown operating system.")
