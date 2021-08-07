""" linux/models.py Linux specific models"""
from enum import Enum


class DisplayServer(str, Enum):
    WAYLAND = "WAYLAND"
    X11 = "X11"


class Desktop(str, Enum):
    GNOME = "GNOME"


class Browser(str, Enum):
    CHROMIUM = "chromium-browser"
    GOOGLE_CHROME = "google-chrome"
    QUTEBROWSER = "org.qutebrowser.qutebrowser"
    FIREFOX = "firefox"


class CodeEditor(str, Enum):
    CODE = "code"


class Reader(str, Enum):
    EVINCE = "evince"
    OKULAR = "okular"
    ZATHURA = "org.pwmt.zathura"


class ImageViewer(str, Enum):
    EYE_OF_GNOME = "eog"
    IMV = "imv"
    FEH = "feh"


class Terminal(str, Enum):
    FOOT = "foot"


role_maps = {
        "browser": {
            "chromium-browser",
            "google-chrome",
            "org.qutebrowser.qutebrowser",
            "firefox"
            },
        "code_editor": {
            "code"
            },
        "e_reader": {
            "evince",
            "org.pwmt.zathura",
            "okular"
            },
        "image_viewer": {
            "eog",
            "imv",
            "feh",
            },
        "terminal": {
            "foot",
            "gnome-terminal-server",
            "konsole"
            }
        }
