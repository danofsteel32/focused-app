__version__ = '0.1.0'

from platform import system

from .linux import get_gnome_all_windows
from .browsers import get_active_tab


def get_focused_app():
    platform = models.Platform(system)
    return


def get_focused_context():
    return
