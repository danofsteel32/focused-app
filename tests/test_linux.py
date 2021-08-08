import pytest


from focused_app.common.models import Window
from focused_app.linux import get_focused_app, get_focused_context
import focused_app.linux.lib as lib
import focused_app.linux.models as models


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


@pytest.fixture
def mock_chromium_focused() -> Window:
    return lib.mock_focused_app(models.Browser.CHROMIUM)


def test_chromium_context(mock_chromium_focused):
    assert mock_chromium_focused
    print(get_focused_context(mock_chromium_focused))


@pytest.fixture
def mock_evince_focused() -> Window:
    return lib.mock_focused_app(models.Reader.EVINCE)


def test_evince_focused(mock_evince_focused):
    assert mock_evince_focused
    print(get_focused_context(mock_evince_focused))


@pytest.fixture
def mock_imv_focused() -> Window:
    return lib.mock_focused_app(models.ImageViewer.IMV)


def test_imv_focused(mock_imv_focused):
    assert mock_imv_focused
    print(get_focused_context(mock_imv_focused))
