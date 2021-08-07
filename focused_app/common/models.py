from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional, Union


class Platform(str, Enum):
    """Will raise ValueError if not supported platform"""
    LINUX = "Linux"
    # DARWIN = "Darwin"
    # WINDOWS = "Windows"


@dataclass
class Window:
    app: str
    title: str
    focused: bool
    pid: int
    sandboxed: bool
    role: Optional[str]


class AppRole(str, Enum):
    BROWSER = "browser"
    CODE_EDITOR = "code_editor"
    E_READER = "e_reader"
    IMAGE_VIEWER = "image_viewer"
    TERMINAL = "terminal"


Context = Union[Path, str, None]  # file path or a url
