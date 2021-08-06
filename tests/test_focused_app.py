import pytest

from focused_app import __version__
from focused_app import linux, models, browsers


def test_version():
    assert __version__ == '0.1.0'


def test_get_desktop():
    assert linux.get_desktop("gnome") == models.LinuxDesktop.GNOME


def test_unsupported_desktop():
    with pytest.raises(ValueError):
        linux.get_desktop("kde")


def test_get_display_server():
    assert isinstance(linux.get_display_server(), models.LinuxDisplayServer)


def test_get_all_windows():
    linux.get_all_windows()
