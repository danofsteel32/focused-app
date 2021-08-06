from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Union


PDF_VIEWERS = {"evince", "org.pwmt.zathura", "org.kde.okular"}


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


class LinuxBrowser(str, Enum):
    CHROMIUM = "chromium-browser"
    GOOGLE_CHROME = "google-chrome"
    QUTEBROWSER = "org.qutebrowser.qutebrowser"
    FIREFOX = "firefox"


class LinuxReader(str, Enum):
    EVINCE = "evince"
    OKULAR = "okular"
    ZATHURA = "org.pwmt.zathura"
