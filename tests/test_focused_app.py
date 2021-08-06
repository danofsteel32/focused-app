import pytest

from focused_app import __version__
from focused_app import linux, models, browsers, get_focused_app, get_focused_context

def test_version():
    assert __version__ == '0.1.0'


@pytest.fixture
def mock_chromium_focused() -> models.LinuxWindow:
    window = {
            "class": "Chromium-browser",
            "title": "danofsteel32/focused-app - Chromium",
            "focused": True,
            "pid": 32,
            "sandboxed_id": "org.chromium.Chromium",
            "role": "browser"
        }
    return linux.create_linux_window(window)


def test_get_desktop():
    assert linux.get_desktop("gnome") == models.LinuxDesktop.GNOME


def test_unsupported_desktop():
    with pytest.raises(ValueError):
        linux.get_desktop("kde")


def test_get_display_server():
    assert isinstance(linux.get_display_server(), models.LinuxDisplayServer)


def test_get_all_windows():
    linux.get_all_windows()


def test_get_focused_app():
    get_focused_app()


def test_chromium_context(mock_chromium_focused):
    print(get_focused_context(mock_chromium_focused))

