"""
This script handles the actions to perform at end of the countdown timer.
"""

import ctypes
import logging
import os
import shutil
import sys
import time

from nightwatch.utils import show_error, show_info

logger = logging.getLogger(__name__)

VK_MEDIA_STOP = 0xB2
KEYEVENTF_KEYUP = 0x2


def _run_command(command):
    """Executes an OS-specific command. Raises RuntimeError if it fails."""
    logger.info("Executing command: %s", command)
    exit_code = os.system(command)
    if exit_code != 0:
        raise RuntimeError(
            f"Failed to execute command: {command}\n\nExit code: {exit_code}"
        )


def _stop_playback():
    """Stops media playback. Raises RuntimeError if it can't."""
    if sys.platform == "win32":
        ctypes.windll.user32.keybd_event(VK_MEDIA_STOP, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_MEDIA_STOP, 0, KEYEVENTF_KEYUP, 0)
    elif sys.platform == "linux":
        if not shutil.which("playerctl"):
            raise RuntimeError(
                "Pausing media on Linux requires playerctl to be installed."
            )
        _run_command("playerctl --all-players pause")
    else:
        raise RuntimeError(
            "Pausing media is not supported on this operating system yet."
        )


def pause_media():
    """Pauses media playback, without resuming media that is already paused."""
    try:
        _stop_playback()
    except RuntimeError as error:
        show_error(str(error))
    else:
        show_info("Media has been paused.")


def sleep_system():
    """Puts the system to sleep based on the operating system."""
    logger.info("Going to sleep...")
    try:
        _stop_playback()
        time.sleep(0.5)
    except RuntimeError as error:
        logger.warning("Could not stop media before sleep: %s", error)

    try:
        if sys.platform == "win32":
            if not ctypes.windll.powrprof.SetSuspendState(False, False, False):
                raise RuntimeError("Failed to put the system to sleep.")
        elif sys.platform == "darwin":
            _run_command("pmset sleepnow")
        elif sys.platform == "linux":
            _run_command("systemctl suspend")
        else:
            raise RuntimeError("Unable to suspend, unknown operating system.")
    except RuntimeError as error:
        show_error(str(error))


def shutdown_system():
    """Shuts down the system based on the operating system."""
    logger.info("Shutting down...")
    try:
        if sys.platform == "win32":
            _run_command("shutdown /s /t 0")
        elif sys.platform == "darwin":
            _run_command("osascript -e 'tell app \"System Events\" to shut down'")
        elif sys.platform == "linux":
            _run_command("systemctl poweroff")
        else:
            raise RuntimeError("Unable to shutdown, unknown operating system.")
    except RuntimeError as error:
        show_error(str(error))
