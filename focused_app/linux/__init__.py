""" linux/__init__.py """

from ..common.models import Window, AppRole, Context
from . import models
from . import browsers
from . import lib


def get_focused_app() -> Window:
    open_windows = lib.get_all_windows()
    return next(w for w in open_windows if w.focused)


def get_focused_context(focused_app: Window = None) -> Context:
    if not focused_app:
        focused_app = get_focused_app()
    if not focused_app:
        raise ValueError
    if focused_app.role is AppRole.BROWSER:
        browser = models.Browser(focused_app.app)
        return browsers.get_active_tab(browser, focused_app.sandboxed)
    elif focused_app.role is AppRole.E_READER:
        return lib.get_file_from_window(focused_app)
    elif focused_app.role is AppRole.IMAGE_VIEWER:
        return lib.get_file_from_window(focused_app)
    return
