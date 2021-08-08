import pytest
from pathlib import Path

from focused_app import get_focused_app, get_focused_context

import focused_app.linux.lib as lib
import focused_app.linux.models as models
import focused_app.linux.browsers as browsers


TEST_CHROME_SESSION = Path("tests/data/Session_13272895883855165")
TEST_SPACES_IMAGE = "tests/data/Screenshot from 2021-08-08 07-24-32.png"


def test_get_desktop():
    assert lib.get_desktop("gnome") == models.Desktop.GNOME


def test_unsupported_desktop():
    with pytest.raises(ValueError):
        lib.get_desktop("OpenBSD")


def test_get_display_server():
    assert isinstance(lib.get_display_server(), models.DisplayServer)


def test_get_all_windows():
    assert len(lib.get_all_windows()) > 0


def test_get_focused_app():
    assert get_focused_app() is not None


def test_get_focused_context():
    get_focused_context()


def test_filepath_with_spaces():
    test_string = (
            "imv - [1/1] [1920x1080] [66%] "
            "/home/dan/code/focused-app/tests/data/"
            "Screenshot from 2021-08-08 07-24-32.png "
            "[scale to fit]")
    filepath = lib.get_filepath_from_title(test_string, {"png"})
    assert filepath == Path.cwd() / TEST_SPACES_IMAGE


def test_chrome_active_tab():
    active_tab = browsers.get_chrome_active_tab(TEST_CHROME_SESSION)
    assert active_tab == "https://github.com/danofsteel32/focused-app"
