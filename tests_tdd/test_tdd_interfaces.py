import pytest

from funchacks.interfaces import Representable
from tests_tdd._tools import testlogger


@pytest.mark.usefixtures("testlogger")
def test_collections() -> None:
    assert getattr(Representable, "__abstractmethods__") == {"__repr__"}
