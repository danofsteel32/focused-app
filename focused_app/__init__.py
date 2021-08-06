__version__ = '0.1.0'

from platform import system

from . import linux
from . import browsers
from . import models


def get_focused_app():
    platform = models.Platform(system())
    if platform is models.Platform.LINUX:
        windows = linux.get_all_windows()
    return next(w for w in windows if w.focused)


def get_focused_context(focused_app: models.LinuxWindow = None):
    while not focused_app:
        focused_app = get_focused_app()
    if not focused_app:
        raise ValueError
    if focused_app.role is models.AppRole.BROWSER:
        browser = models.LinuxBrowser(focused_app.app)
        return browsers.get_active_tab(browser, focused_app.sandboxed)
    elif focused_app.role is models.AppRole.E_READER:
        return
    return
