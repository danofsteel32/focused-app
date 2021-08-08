__version__ = '0.1.0'

from platform import system
from typing import Optional

from . import linux
from . import macos
from . import windows
from .common.models import Window, Platform, Context


def get_focused_app() -> Optional[Window]:
    platform = Platform(system())
    if platform is Platform.LINUX:
        return linux.get_focused_app()
    elif platform is Platform.DARWIN:
        return macos.get_focused_app()
    elif platform is Platform.WINDOWS:
        return windows.get_focused_app()
    return None


def get_focused_context(focused_app: Window = None) -> Context:
    while not focused_app:
        focused_app = get_focused_app()
    if not focused_app:
        raise ValueError("Couldn't get focused app")
    platform = Platform(system())
    if platform is Platform.LINUX:
        return linux.get_focused_context(focused_app)
    elif platform is Platform.DARWIN:
        return macos.get_focused_context()
    elif platform is Platform.WINDOWS:
        return windows.get_focused_context()
