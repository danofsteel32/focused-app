# This is a temporary workaround till Poetry supports scripts, see
# https://github.com/sdispater/poetry/issues/241.
from subprocess import check_call


def lint() -> None:
    check_call(["flake8", "focused_app/", "tests/"])
    check_call(["mypy", "focused_app/", "tests/"])


def test() -> None:
    check_call(["pytest", "-rP", "tests/unit/"])


def integration_test() -> None:
    check_call(["pytest", "-rP", "tests/integration/"])
