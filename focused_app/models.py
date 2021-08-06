from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Union


class Platform(str, Enum):
    """Will raise ValueError if not supported platform"""
    LINUX = "Linux"
    # DARWIN = "Darwin"
    # WINDOWS = "Windows"


@dataclass
class LinuxWindow:
    app: str
    title: str
    focused: bool
    pid: int
    sandboxed: bool
    role: Optional[str]


class LinuxDisplayServer(str, Enum):
    WAYLAND = "WAYLAND"
    X11 = "X11"


class LinuxDesktop(str, Enum):
    GNOME = "GNOME"


class AppRole(str, Enum):
    BROWSER = "browser"
    CODE_EDITOR = "code_editor"
    E_READER = "e_reader"
    IMAGE_VIEWER = "image_viewer"
    TERMINAL = "terminal"


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
            "imv",
            "feh"
            },
        "terminal": {
            "foot",
            "gnome-terminal-server"
            }
        }


class LinuxBrowser(str, Enum):
    CHROMIUM = "chromium-browser"
    GOOGLE_CHROME = "google-chrome"
    QUTEBROWSER = "org.qutebrowser.qutebrowser"
    FIREFOX = "firefox"


class LinuxReader(str, Enum):
    EVINCE = "evince"
    OKULAR = "okular"
    ZATHURA = "org.pwmt.zathura"
