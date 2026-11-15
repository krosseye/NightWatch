"""Script to build the NightWatch application."""

import os
import platform

import PyInstaller.__main__

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = os.path.join(PROJECT_DIR, "src")
RESOURCE_DIR = os.path.join(SOURCE_DIR, "resources")

PLATFORM = platform.system().lower()
ARCHITECTURE = platform.machine().lower()
ARCHITECTURE = {"amd64": "x86_64", "aarch64": "arm64"}.get(ARCHITECTURE, ARCHITECTURE)
TARGET = f"{PLATFORM}-{ARCHITECTURE}"

BUILD_DIR = os.path.join(PROJECT_DIR, "build")
DIST_DIR = os.path.join(BUILD_DIR, "bin", TARGET)
ARTIFACTS_DIR = os.path.join(BUILD_DIR, "artifacts", TARGET)
ICON_FILE = os.path.join(
    RESOURCE_DIR, "icon.ico" if PLATFORM == "windows" else "icon.png"
)


def main() -> None:
    """Main function to build the NightWatch application."""
    PyInstaller.__main__.run(
        [
            os.path.join(SOURCE_DIR, "main.py"),
            "--name",
            f"NightWatch-{TARGET}",
            "--icon",
            ICON_FILE,
            "--distpath",
            DIST_DIR,
            "--workpath",
            os.path.join(ARTIFACTS_DIR, "work"),
            "--specpath",
            ARTIFACTS_DIR,
            "--add-data",
            f"{RESOURCE_DIR}{os.pathsep}resources",
            "--collect-data",
            "sv_ttk",
            "--onefile",
            "--clean",
            "--noconfirm",
            "--windowed",
            "--uac-admin",
        ]
    )


if __name__ == "__main__":
    main()
