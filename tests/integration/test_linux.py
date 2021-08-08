import pytest
import subprocess
import time
from pathlib import Path

from focused_app.common.models import Window
from focused_app.linux import get_focused_context
import focused_app.linux.lib as lib
import focused_app.linux.models as models

TEST_PDF = "tests/data/10.1.1.132.6973.pdf"
TEST_IMAGE = "tests/data/1232-0.jpeg"


@pytest.fixture
def mock_chromium_focused() -> Window:
    return lib.mock_focused_app(models.Browser.CHROMIUM)


def test_chromium_context(mock_chromium_focused):
    assert mock_chromium_focused
    print(get_focused_context(mock_chromium_focused))


@pytest.fixture
def mock_evince_focused() -> Window:
    proc = subprocess.Popen(["evince", TEST_PDF])
    time.sleep(1)
    yield lib.mock_focused_app(models.Reader.EVINCE)
    proc.kill()


def test_evince_focused(mock_evince_focused):
    assert mock_evince_focused
    test_file = get_focused_context(mock_evince_focused)
    assert test_file == Path.cwd() / TEST_PDF


@pytest.fixture
def mock_imv_focused() -> Window:
    proc = subprocess.Popen(["imv", TEST_IMAGE])
    time.sleep(0.5)
    yield lib.mock_focused_app(models.ImageViewer.IMV)
    proc.kill()


def test_imv_focused(mock_imv_focused):
    assert mock_imv_focused
    test_file = get_focused_context(mock_imv_focused)
    assert test_file == Path.cwd() / TEST_IMAGE
