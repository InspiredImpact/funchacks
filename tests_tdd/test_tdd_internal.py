import pytest

from funchacks.internal import ZipGeneric
from tests_tdd._tools import testlogger


@pytest.mark.usefixtures("testlogger")
def test_generics() -> None:
    assert issubclass(ZipGeneric, zip)
