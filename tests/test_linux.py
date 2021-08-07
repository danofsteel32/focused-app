import pytest


from focused_app.common.models import Window
from focused_app.linux import get_focused_app, get_focused_context
import focused_app.linux.lib as lib
import focused_app.linux.models as models


@pytest.fixture
def mock_chromium_focused() -> Window:
    window = {
            "class": "Chromium-browser",
            "title": "danofsteel32/focused-app - Chromium",
            "focused": True,
            "pid": 32,
            "sandboxed_id": None,
            "role": "browser"
        }
    return lib.create_window(window)


@pytest.fixture
def mock_chromium_focused_sandboxed() -> Window:
    window = {
            "class": "Chromium-browser",
            "title": "danofsteel32/focused-app - Chromium",
            "focused": True,
            "pid": 32,
            "sandboxed_id": "org.chromium.Chromium",
            "role": "browser"
        }
    return lib.create_window(window)


def test_get_desktop():
    assert lib.get_desktop("gnome") == models.Desktop.GNOME


def test_unsupported_desktop():
    with pytest.raises(ValueError):
        lib.get_desktop("kde")


def test_get_display_server():
    assert isinstance(lib.get_display_server(), models.DisplayServer)


def test_get_all_windows():
    lib.get_all_windows()


def test_get_focused_app():
    print(get_focused_app())


def test_chromium_context(mock_chromium_focused):
    print(get_focused_context(mock_chromium_focused))
