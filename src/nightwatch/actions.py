"""
This script handles the actions to perform at end of the countdown timer.
"""

import ctypes
import logging
import os
import shutil
import sys

from nightwatch.utils import show_error, show_info

logger = logging.getLogger(__name__)

VK_MEDIA_STOP = 0xB2
KEYEVENTF_KEYUP = 0x2


def _run_command(command):
    """Executes an OS-specific command. Returns whether it succeeded."""
    logger.info("Executing command: %s", command)
    exit_code = os.system(command)
    if exit_code != 0:
        show_error(f"Failed to execute command: {command}\n\nExit code: {exit_code}")
    return exit_code == 0


def pause_media():
    """Pauses media playback, without resuming media that is already paused."""
    if sys.platform == "win32":
        ctypes.windll.user32.keybd_event(VK_MEDIA_STOP, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_MEDIA_STOP, 0, KEYEVENTF_KEYUP, 0)
    elif sys.platform == "linux":
        if not shutil.which("playerctl"):
            show_error("Pausing media on Linux requires playerctl to be installed.")
            return
        if not _run_command("playerctl --all-players pause"):
            return
    else:
        show_error("Pausing media is not supported on this operating system yet.")
        return
    show_info("Media has been paused.")


def sleep_system():
    """Puts the system to sleep based on the operating system."""
    logger.info("Going to sleep...")
    if sys.platform == "win32":
        if not ctypes.windll.powrprof.SetSuspendState(False, False, False):
            show_error("Failed to put the system to sleep.")
    elif sys.platform == "darwin":
        _run_command("pmset sleepnow")
    elif sys.platform == "linux":
        _run_command("systemctl suspend")
    else:
        show_error("Unable to suspend, unknown operating system.")


def shutdown_system():
    """Shuts down the system based on the operating system."""
    logger.info("Shutting down...")
    if sys.platform == "win32":
        _run_command("shutdown /s /t 0")
    elif sys.platform == "darwin":
        _run_command("osascript -e 'tell app \"System Events\" to shut down'")
    elif sys.platform == "linux":
        _run_command("systemctl poweroff")
    else:
        show_error("Unable to shutdown, unknown operating system.")
